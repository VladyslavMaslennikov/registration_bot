import logging

from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, CallbackQuery, ReplyKeyboardMarkup, ContentType

from helpers.dialogs import Dialog
from helpers.menu import menu
from helpers.calendar import calendar_callback, create_calendar, process_calendar_selection
from helpers.date_functions import day_is_correct, get_date_from_string
from helpers.google_api import find_all_events_for_day, create_new_event

from inline_buttons.hours import available_hours_callback
from inline_buttons.hours import return_inline_buttons_for_hours

from loader_model import dp

from states import RegistrationState


# Start handler
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Добро пожаловать. Для записи на сеанс пройдите в Меню.")


# Menu handlers
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer("Открываю Меню...", reply_markup=menu)


@dp.message_handler(text=Dialog.book_session)
async def open_calendar(message: types.Message):
    await message.answer("Открываю календарь...", reply_markup=ReplyKeyboardRemove())
    await message.answer("Выберите дату", reply_markup=create_calendar())
    await RegistrationState.picking_date.set()


@dp.callback_query_handler(calendar_callback.filter(), state=RegistrationState.picking_date)
async def process_name(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await process_calendar_selection(callback_query, callback_data)
    if selected:
        picked_date = date.strftime("%d/%m/%Y")
        await callback_query.message.answer(f"Вы выбрали {picked_date}")
        # check available time for event
        day_is_ok = day_is_correct(date)
        if not day_is_ok:
            await callback_query.message.answer("Пожалуйста, выберите другой день",
                                                reply_markup=create_calendar())
            return
        available_hours = find_all_events_for_day(date)
        if not available_hours:
            await callback_query.message.answer("Нет свободной записи. Пожалуйста, выберите другой день",
                                                reply_markup=create_calendar())
            return
        # proceed if date is correct and there are available hours
        hours_markup = return_inline_buttons_for_hours(available_hours)
        await callback_query.message.answer("Выберите время", reply_markup=hours_markup)
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
    await call.message.answer(f"Вы выбрали время на {picked_hour}:00. Пожалуйста, введите номер телефона")
    await call.message.edit_reply_markup(reply_markup=None)
    await RegistrationState.next()


@dp.message_handler(state=RegistrationState.setting_phone_number)
async def ask_phone_number(message: types.Message, state: FSMContext):
    phone = message.text
    await message.answer(text="Введите имя и фамилию")
    await state.update_data(
        {"phone": phone}
    )
    await RegistrationState.next()


@dp.message_handler(state=RegistrationState.setting_username)
async def ask_username(message: types.Message, state: FSMContext):
    await message.answer(text="Спасибо за регистрацию")
    user_data = await state.get_data()

    user_name = message.text
    user_phone = user_data["phone"]
    register_date = get_date_from_string(user_data["date"] + " " + user_data["hour"])

    response = f'Имя и фамилия: {user_name}\n' \
               f'Телефон: {user_phone}\n' \
               f'Дата записи: {register_date}'
    await message.answer(response)
    await state.finish()
    await state.reset_state(with_data=True)

    event_created = create_new_event(register_date, user_name, user_phone)
    if event_created:
        await message.answer("Спасибо за регистрацию. Я свяжусь с Вами в течении дня.")


