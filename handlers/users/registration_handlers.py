from aiogram.dispatcher.filters import Command, CommandStart
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from helpers.dialogs import Dialog
from helpers.menu import menu
from helpers.calendar import calendar_callback, create_calendar, process_calendar_selection

from loader_model import dp


# Start handler
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Ты нажал на /start.")


# Menu handlers
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer(reply_markup=menu)


@dp.message_handler(text=Dialog.book_session)
async def proceed_register(message: types.Message):
    await message.answer("Выберите дату.", reply_markup=ReplyKeyboardRemove)


# Calendar handlers
@dp.message_handler(text="calendar")
async def cmd_start(message: types.Message):
    await message.answer("Please select a date: ", reply_markup=create_calendar())


@dp.callback_query_handler(calendar_callback.filter())  # handler is processing only calendar_callback queries
async def process_name(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await process_calendar_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(f'You selected {date.strftime("%d/%m/%Y")}',
                                            reply_markup=ReplyKeyboardRemove())
