from aiogram import Dispatcher
from data.config import my_chat_id

from loader_model import db


# trigger action when bot runs
async def notify_on_startup(dp: Dispatcher):
    # TODO: need to setup admin commands below
    # TODO: await dp.bot.send_message(chat_id=my_chat_id, text="Привет, админ")
    # db.clear_database()
    try:
        db.create_table()  # создаем таблицу если ее нет
    except Exception as e:
        print(e)
    clients = db.get_all_clients()
    for client in clients:
        print(client)
