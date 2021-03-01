from aiogram import Dispatcher
from data.config import my_chat_id

from loader_model import db


# trigger action when bot runs
async def notify_on_startup(dp: Dispatcher):
    try:
        db.create_table()  # создаем таблицу если ее нет
    except Exception as e:
        print(e)
    db.add_client(user_id=270518430, phone="0939956089",
                  creation_date="01.03.2021", registration_date="09.03.2021",
                  user_name="Vladyslav Maslennikov")

    clients = db.get_all_clients()
    print(clients)
    # await dp.bot.send_message(chat_id=my_chat_id, text="Привет, админ")
