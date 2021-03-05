from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from data import config

from database.sqlite import Database

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()

db = Database()
dp = Dispatcher(bot, storage=storage)