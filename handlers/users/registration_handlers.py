from aiogram import types
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from helpers.calendar import calendar_callback, create_calendar, process_calendar_selection
from helpers.date_functions import day_is_correct, get_date_from_string
from helpers.dialogs import Dialog
from helpers.google_api import find_all_events_for_day, create_new_event
from helpers.menu import menu
from inline_buttons.hours import available_hours_callback
from inline_buttons.hours import return_inline_buttons_for_hours
from loader_model import dp
from states import RegistrationState


# Start handler
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(Dialog.welcome_message)


# Menu handlers
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer(Dialog.opening_menu, reply_markup=menu)


@dp.message_handler(text=Dialog.book_session)
async def open_calendar(message: types.Message):
    await message.answer(Dialog.opening_calendar, reply_markup=ReplyKeyboardRemove())
    await message.answer(Dialog.pick_date, reply_markup=create_calendar())
    await RegistrationState.picking_date.set()


@dp.callback_query_handler(calendar_callback.filter(), state=RegistrationState.picking_date)
async def process_name(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await process_calendar_selection(callback_query, callback_data)
    if selected:
        picked_date = date.strftime("%m/%d/%Y")
        await callback_query.message.answer(f"{Dialog.you_picked_day} {picked_date}")
        # check available time for event
        day_is_ok = day_is_correct(date)
        if not day_is_ok:
            await callback_query.message.answer(Dialog.pick_another_day,
                                                reply_markup=create_calendar())
            return
        available_hours = find_all_events_for_day(date)
        if not available_hours:
            await callback_query.message.answer(Dialog.no_available_date,
                                                reply_markup=create_calendar())
            return
        # proceed if date is correct and there are available hours
        hours_markup = return_inline_buttons_for_hours(available_hours)
        await callback_query.message.answer(Dialog.pick_hour, reply_markup=hours_markup)
        await state.update_data(
            {"date": picked_date}
        )
        await RegistrationState.next()


@dp.callback_query_handler(available_hours_callback.filter(), state=RegistrationState.choosing_hour)
async def handle_available_hours(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    picked_hour = callback_data.get("hour")
    await state.update_data(
        {"hour": str(picked_hour) + ":00"}
    )
    await call.message.answer(f"{Dialog.you_picked_hour} {picked_hour}{Dialog.enter_phone}")
    await call.message.edit_reply_markup(reply_markup=None)
    await RegistrationState.next()


@dp.message_handler(state=RegistrationState.setting_phone_number)
async def ask_phone_number(message: types.Message, state: FSMContext):
    phone = message.text
    await message.answer(text=Dialog.enter_name)
    await state.update_data(
        {"phone": phone}
    )
    await RegistrationState.next()


@dp.message_handler(state=RegistrationState.setting_username)
async def ask_username(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    user_name = message.text
    user_phone = user_data["phone"]
    register_date = get_date_from_string(user_data["date"] + " " + user_data["hour"])
    response = f'{Dialog.name_desc} {user_name}\n' \
               f'{Dialog.phone_desc} {user_phone}\n' \
               f'{Dialog.date_desc} {register_date}'
    await message.answer(response)
    await state.finish()
    await state.reset_state(with_data=True)

    event_created = create_new_event(register_date, user_name, user_phone)
    if event_created:
        await message.answer(Dialog.thanks_for_registration)
