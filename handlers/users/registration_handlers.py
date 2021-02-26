from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from helpers.dialogs import Dialog
from helpers.menu import menu
from helpers.calendar import calendar_callback, create_calendar, process_calendar_selection

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
    await message.answer("Выберите дату", reply_markup=create_calendar())
    # нужно убрать меню после вызова календаря
    await RegistrationState.picking_date.set()


@dp.callback_query_handler(calendar_callback.filter(), state=RegistrationState.picking_date)
async def process_name(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await process_calendar_selection(callback_query, callback_data)
    if selected:
        picked_date = date.strftime("%d/%m/%Y")
        await callback_query.message.answer(f'Вы выбрали {picked_date}.',
                                            reply_markup=ReplyKeyboardRemove())
        await state.update_data(date=picked_date)
        await callback_query.message.answer("Выберите время")
        await RegistrationState.next()


@dp.message_handler(state=RegistrationState.choosing_hour)
async def show_available_dates(message: types.Message, state: FSMContext):
    picked_hour = message.text
    await message.answer(text=f"Вы выбрали время {picked_hour}. \nВведите номер телефона")
    await state.update_data(hour=picked_hour)
    await RegistrationState.next()


@dp.message_handler(state=RegistrationState.setting_phone_number)
async def ask_phone_number(message: types.Message, state: FSMContext):
    phone = message.text
    await message.answer(text=f"Номер телефона {phone}. \nВведите имя и фамилию")
    await state.update_data(phone=phone)
    await RegistrationState.next()


@dp.message_handler(state=RegistrationState.setting_username)
async def ask_username(message: types.Message, state: FSMContext):
    username = message.text
    await message.answer(text="Спасибо за регистрацию")
    await state.update_data(username=username)
    data = await state.get_data()
    print(data)
    await RegistrationState.next()


@dp.message_handler(state=RegistrationState.giving_instructions)
async def show_instructions(message: types.Message, state: FSMContext):
    await message.answer(text="Пройдите ...")
    data = await state.get_data()
    print(data)
    await state.finish()
