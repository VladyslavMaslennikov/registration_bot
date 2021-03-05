from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from helpers.date_helper import DateHelper

upcoming_events_callback = CallbackData("client", "user_id")


def return_inline_buttons_for_events(events: list):
    count = len(events)
    buttons = []
    for event in events:
        date = DateHelper.get_formatted_date(event[3], event[4]) + f"-{event[5]}:00"
        name = event[6]
        user_id = event[0]
        button = [InlineKeyboardButton(text=name + "\n" + date,
                                       callback_data=upcoming_events_callback.new(user_id=user_id))]
        buttons.append(button)
    markup = InlineKeyboardMarkup(row_width=count, inline_keyboard=buttons)
    return markup
