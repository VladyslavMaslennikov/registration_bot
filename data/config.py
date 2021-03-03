import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
# /Users/vladyslav/Desktop/Bots/First_Bot/venv/bin/python3 - директория
GOOGLE_CALENDAR_ID = str(os.getenv("GOOGLE_CALENDAR_ID"))

admins = [
    270518430  # my chat_id
]