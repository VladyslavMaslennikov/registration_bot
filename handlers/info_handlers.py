from aiogram import types
from data.config import krakow_lon, krakow_lat
from filters import GetDestinationCommand
from loader_model import dp
from middlewares.throttling_middleware import rate_limit


@rate_limit(10)
@dp.message_handler(GetDestinationCommand())
async def show_destination_info(message: types.Message):
    await message.answer("https://goo.gl/maps/sUEwTP1RxVv1adsd7")