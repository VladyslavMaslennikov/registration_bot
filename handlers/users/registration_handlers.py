from aiogram import types
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery, BotCommand
from data.config import admins
from datetime import datetime
from helpers.calendar import calendar_callback, create_calendar, process_calendar_selection
from helpers.date_functions import day_is_correct, get_date_from_string
from helpers.dialogs import Dialog
from helpers.google_api import find_all_events_for_day, create_new_event
from helpers.menu import menu
from inline_buttons.hours import available_hours_callback
from inline_buttons.hours import return_inline_buttons_for_hours
from loader_model import dp, db
from states import RegistrationState


# Start handler
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(Dialog.welcome_message)
    # set admin command
    user_id = message.chat.id
    if user_id in admins:
        await dp.bot.set_my_commands(commands=[
            BotCommand(command="menu", description=Dialog.menu_inline_description),
            BotCommand(command="statistics", description=Dialog.show_statistics_for_delta)
        ])


@dp.message_handler(Command("statistics"))
async def ask_user_for_delta(message: types.Message, state: FSMContext):
    await message.answer(Dialog.enter_day_number_for_statistics)
    await state.set_state("stats")


@dp.message_handler(state="stats")
async def show_stats(message: types.Message, state: FSMContext):
    delta = message.text
    if delta.isdigit():
        clients = db.get_newly_registered_clients(int(delta))
        if clients:
            await message.answer(f"{Dialog.new_clients_are}\n{clients}")
        else:
            await message.answer(Dialog.no_new_appointments)
        await state.finish()
    else:
        await message.answer(Dialog.enter_integer)


# Menu handlers
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer(Dialog.opening_menu, reply_markup=menu)


@dp.message_handler(text=Dialog.cancel_session)
async def cancel_session(message: types.Message):
    user_id = message.chat.id
    client_has_appointment = db.check_if_user_has_appointment(user_id)
    if client_has_appointment:
        db.delete_the_user(user_id)
        await message.answer(Dialog.cancellation_success)
    else:
        await message.answer(Dialog.no_appointment_for_you)


@dp.message_handler(text=Dialog.book_session)
async def open_calendar(message: types.Message):
    user_id = message.chat.id
    client_has_appointment = db.check_if_user_has_appointment(user_id)
    if client_has_appointment:
        await message.answer(Dialog.already_have_appointment)
        client = db.get_client(user_id)
        if client:
            registered_date = client[3]
            dt = get_date_from_string(registered_date)
            date_desc = f"{dt.year}-{dt.month}-{dt.day} {dt.hour}:00"
            await message.answer(Dialog.date_desc + f" {date_desc}")
    else:
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
    dt = get_date_from_string(user_data["date"] + " " + user_data["hour"])
    date_desc = f"{dt.year}-{dt.month}-{dt.day} {dt.hour}:00"
    response = f'{Dialog.name_desc} {user_name}\n' \
               f'{Dialog.phone_desc} {user_phone}\n' \
               f'{Dialog.date_desc} {date_desc}'
    await message.answer(response)
    await state.finish()
    await state.reset_state(with_data=True)

    event_created = create_new_event(dt, user_name, user_phone)
    if event_created:
        user_id = message.chat.id
        client_added = db.add_client(user_id, user_phone, f"{datetime.now()}", f"{dt}", user_name)
        print(client_added)
        await message.answer(Dialog.thanks_for_registration)
