from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from model.dialogs import Dialog


class ShowUpcomingEventsCommand(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.text == Dialog.show_calendar_sessions
