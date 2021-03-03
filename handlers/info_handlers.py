from aiogram import types
from data.config import krakow_address
from filters import GetDestinationCommand, GetCareInfoCommand
from loader_model import dp
from middlewares.throttling_middleware import rate_limit
from model.dialogs import Dialog


@rate_limit(5)
@dp.message_handler(GetDestinationCommand())
async def show_destination_info(message: types.Message):
    await message.answer(krakow_address)
    await message.answer(Dialog.my_link)


@rate_limit(5)
@dp.message_handler(GetCareInfoCommand())
async def show_tattoo_care_info(message: types.Message):
    await message.answer(Dialog.tattoo_care_info)