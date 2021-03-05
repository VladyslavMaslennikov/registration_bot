from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

options_callback = CallbackData("info", "option", "user_id")


def return_options(user_id: int):
    buttons = [
        [InlineKeyboardButton(text="Изменить часы сеанса",
                              callback_data=options_callback.new(option=1, user_id=user_id))],
        [InlineKeyboardButton(text="Залог",
                              callback_data=options_callback.new(option=2, user_id=user_id))],
        [InlineKeyboardButton(text="Удалить сеанс",
                              callback_data=options_callback.new(option=3, user_id=user_id))]
    ]
    markup = InlineKeyboardMarkup(row_width=0, inline_keyboard=buttons)
    return markup
