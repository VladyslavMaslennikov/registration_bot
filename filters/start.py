from aiogram import Dispatcher

from data.config import my_chat_id

from loader_model import db


# trigger action when bot runs
async def notify_on_startup(dp: Dispatcher):
    # TODO: need to setup admin commands below
    # TODO: await dp.bot.send_message(chat_id=my_chat_id, text="Привет, админ")
    # TODO: db.clear_database() ??? + delete google events
    try:
        db.create_table()  # создаем таблицу если ее нет
    except Exception as e:
        print(e)
    db.get_newly_registered_clients(1)
    # clients = db.get_all_clients()
    # for client in clients:
    #     print(client)
