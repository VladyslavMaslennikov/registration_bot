from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


class ShowUpcomingEventsCommand(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.text == "/calendar"
