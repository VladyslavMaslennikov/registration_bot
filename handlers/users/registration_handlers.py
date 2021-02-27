import logging

from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, CallbackQuery, ReplyKeyboardMarkup, ContentType

from helpers.dialogs import Dialog
from helpers.menu import menu
from helpers.calendar import calendar_callback, create_calendar, process_calendar_selection
from helpers.choice_buttons import choice, data_correct_callback
from helpers.date_functions import day_is_correct
import helpers.google_api as google_api

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
        available_hours = google_api.find_all_events_for_day(date)
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
async def handle_available_hours(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    print(call.data)
    await call.message.answer(f"Выбрано: {call.data}")


@dp.message_handler(state=RegistrationState.choosing_hour)
async def show_available_dates(message: types.Message, state: FSMContext):
    picked_hour = message.text
    await message.answer(text="Введите номер телефона")
    await state.update_data(
        {"hour": picked_hour}
    )
    # create new google calendar event
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
    username = message.text
    await state.update_data(
        {"username": username}
    )
    await message.answer(text="Спасибо за регистрацию")
    user_data = await state.get_data()
    response = f'Имя и фамилия: {user_data["username"]}\n' \
               f'Телефон: {user_data["phone"]}\n' \
               f'Дата записи: {user_data["date"]} {user_data["hour"]}'
    await message.answer(response)
    await message.answer("Данные заполнены верно?", reply_markup=choice)
    await RegistrationState.next()


@dp.callback_query_handler(data_correct_callback.filter(result="correct"), state=RegistrationState.check_if_correct)
async def handle_correct_data(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)  # что бы апдейты не приходили какое-то время
    print(call.data)
    print(callback_data)
    logging.info(f"callback data dict {callback_data}")
    # await call.message.edit_reply_markup(reply_markup=None)  # убрать инлайн кнопки
    await call.message.answer("Гуд.")
