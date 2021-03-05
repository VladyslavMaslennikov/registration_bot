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
    # clients = db.get_all_clients()
    # for client in clients:
    #     print(client)


# Start handler
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(Dialog.welcome_message)
    # set admin command
    user_id = message.chat.id
    print(user_id)
    if user_id in admins:
        await dp.bot.set_my_commands(commands=[
            BotCommand(command="menu", description=Dialog.menu_inline_description),
            # BotCommand(command="statistics", description=Dialog.show_statistics_for_delta),
            BotCommand(command="calendar", description="Показать ближайшие записи")
        ])
    else:
        await dp.bot.set_my_commands(commands=[
            BotCommand(command="menu", description=Dialog.menu_inline_description)
        ])

