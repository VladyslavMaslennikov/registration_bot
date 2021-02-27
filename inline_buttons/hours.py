from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

available_hours_callback = CallbackData("available_hour", "hour")


def return_inline_buttons_for_hours(hours: list):
    count = len(hours)
    if count > 7:
        keyboard_buttons = [
            [InlineKeyboardButton(text=f"{x}:00",
                                  callback_data=available_hours_callback.new(hour=f"{x}"))
             for x in hours[:int(count/2)]],
            [InlineKeyboardButton(text=f"{x}:00",
                                  callback_data=available_hours_callback.new(hour=f"{x}"))
             for x in hours[int(count/2):]]
        ]
        markup = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=keyboard_buttons)
        return markup
    else:
        keyboard_buttons = [
            InlineKeyboardButton(text=f"{x}:00",
                                 callback_data=available_hours_callback.new(hour=f"{x}"))
            for x in hours
        ]
        markup = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=keyboard_buttons)
        return markup

