from aiogram import types
from data.config import admins
from filters import MenuCommand
from model.dialogs import Dialog
from model.menu import menu, admin_menu

from loader_model import dp


# Menu handlers
@dp.message_handler(MenuCommand())
async def show_menu(message: types.Message):
    user_id = message.chat.id
    if user_id in admins:
        await message.answer(Dialog.opening_menu, reply_markup=admin_menu)
    else:
        await message.answer(Dialog.opening_menu, reply_markup=menu)
