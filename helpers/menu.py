from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from helpers.dialogs import Dialog


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(Dialog.book_session),
            KeyboardButton(Dialog.cancel_session)
        ],
        [
            KeyboardButton(Dialog.tattoo_care),
            KeyboardButton(Dialog.how_to_get)
        ]
    ],
    resize_keyboard=True
)
