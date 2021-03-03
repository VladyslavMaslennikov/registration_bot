import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
# /Users/vladyslav/Desktop/Bots/First_Bot/venv/bin/python3 - директория
GOOGLE_CALENDAR_ID = str(os.getenv("GOOGLE_CALENDAR_ID"))

admins = [
    270518430,  # my chat_id
    318852507  # lena id
]

krakow_lat = 50.038305
krakow_lon = 19.9406286