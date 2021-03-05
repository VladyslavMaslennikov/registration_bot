from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from data.config import admins
from filters import ShowUpcomingEventsCommand
from model.dialogs import Dialog
from model.utils import get_description

from loader_model import db, dp

from inline_buttons.events import upcoming_events_callback, return_inline_buttons_for_events
from inline_buttons.options import options_callback, return_options
from inline_buttons.hours import available_hours_callback


# statistics commands for admin
@dp.message_handler(ShowUpcomingEventsCommand())
async def show_stats(message: types.Message):
    user_id = message.chat.id
    if user_id in admins:
        events = db.find_all_events_in_range()
        if not events:
            await message.answer(f"Нет записей в этом промежутке.", reply_markup=None)
        else:
            events_markup = return_inline_buttons_for_events(events)
            await message.answer("Записи:", reply_markup=events_markup)


@dp.callback_query_handler(upcoming_events_callback.filter())
async def show_clients(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    user_id = callback_data.get("user_id")
    user = get_description(user_id)
    options_markup = return_options(user_id)
    await call.message.answer(user, reply_markup=options_markup)


@dp.callback_query_handler(options_callback.filter())
async def choose_option(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    option = int(callback_data.get("option"))
    user_id = callback_data.get("user_id")
    if option == 1:
        db.toggle_deposit(user_id)
        await call.message.answer("Значение залога изменено.")
        await call.message.edit_reply_markup(reply_markup=None)
    if option == 2:
        user = db.get_client(user_id)
        if user:
            db.delete_the_user(user_id)
            await call.message.answer("Сеанс удален.")
            await call.message.edit_reply_markup(reply_markup=None)


@dp.callback_query_handler(available_hours_callback.filter(), state="prolong")
async def handle_available_hours(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)

    user_data = await state.get_data()
    user_id = user_data["user_id"]
    picked_hour = callback_data.get("hour")

    db.update_session_end(user_id, picked_hour)

    await call.message.answer("Время сеанса успешно изменено")
    await call.message.edit_reply_markup(reply_markup=None)
    await state.finish()
