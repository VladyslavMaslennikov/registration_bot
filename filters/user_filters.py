from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from model.dialogs import Dialog


class CancelCommand(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.text == Dialog.cancel_session


class BookSessionCommand(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.text == Dialog.book_session


class MenuCommand(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.text == "/menu"
