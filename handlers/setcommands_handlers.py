from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from filters import ShowStatisticsCommand
from helpers.dialogs import Dialog

from loader_model import db, dp


# statistics command for admin
@dp.message_handler(ShowStatisticsCommand())
async def ask_user_for_delta(message: types.Message, state: FSMContext):
    await message.answer(Dialog.enter_day_number_for_statistics)
    await state.set_state("stats")


@dp.message_handler(state="stats")
async def show_stats(message: types.Message, state: FSMContext):
    delta = message.text
    if delta.isdigit():
        clients = db.get_newly_registered_clients(int(delta))
        if clients:
            await message.answer(f"{Dialog.new_clients_are}\n{clients}")
        else:
            await message.answer(Dialog.no_new_appointments)
        await state.finish()
    else:
        await message.answer(Dialog.enter_integer)
