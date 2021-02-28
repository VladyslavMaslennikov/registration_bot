from aiogram import Dispatcher
from data.config import my_chat_id


# will trigger action when bot runs
async def on_startup(dp: Dispatcher):
    await dp.bot.send_message(chat_id=my_chat_id, text="Привет, админ")
