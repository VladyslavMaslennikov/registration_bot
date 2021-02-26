from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

data_correct_callback = CallbackData("data_is_correct", "result")

choice = InlineKeyboardMarkup(row_width=2,
                              inline_keyboard=[
                                  [
                                    InlineKeyboardButton(
                                        text="Да, все верно",
                                        callback_data=data_correct_callback.new(result="correct")
                                    ),
                                    InlineKeyboardButton(
                                        text="Нет",
                                        callback_data=data_correct_callback.new(result="correct")
                                    )
                                  ]
                              ])
