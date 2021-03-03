from aiogram import types
from filters import MenuCommand
from helpers.dialogs import Dialog
from helpers.menu import menu

from loader_model import dp


# Menu handlers
@dp.message_handler(MenuCommand())
async def show_menu(message: types.Message):
    await message.answer(Dialog.opening_menu, reply_markup=menu)
