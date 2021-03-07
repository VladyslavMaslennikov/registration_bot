from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types.bot_command import BotCommand

from data.config import admins

from model.dialogs import Dialog

from loader_model import dp, db


# trigger action when bot runs
async def notify_on_startup(dispatcher: Dispatcher):
    try:
        db.create_table()  # создаем таблицу если ее нет
    except Exception as e:
        print(e)


# Start handler
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(Dialog.welcome_message)

