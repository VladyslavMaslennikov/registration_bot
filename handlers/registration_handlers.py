from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from datetime import datetime

from filters import CancelCommand, BookSessionCommand

from helpers.calendar import calendar_callback, create_calendar, process_calendar_selection
from helpers.date_helper import DateHelper
from model.dialogs import Dialog
from inline_buttons.hours import available_hours_callback
from inline_buttons.hours import return_inline_buttons_for_hours
from loader_model import dp, db
from middlewares.throttling_middleware import rate_limit
from states import RegistrationState


@rate_limit(5)
@dp.message_handler(CancelCommand())
async def cancel_session(message: types.Message):
    user_id = message.chat.id
    client_has_appointment = db.check_if_user_has_appointment(user_id)
    if client_has_appointment:
        db.delete_the_user(user_id)
        await message.answer(Dialog.cancellation_success)
    else:
        await message.answer(Dialog.no_appointment_for_you)


@rate_limit(5)
@dp.message_handler(BookSessionCommand())
async def open_calendar(message: types.Message):
    user_id = message.chat.id
    client_has_appointment = db.check_if_user_has_appointment(user_id)
    if client_has_appointment:
        await message.answer(Dialog.already_have_appointment)
        client = db.get_client(user_id)
        if client:
            registered_date = client[3]
            session_start = client[4]
            dt = DateHelper.get_date_from_string(registered_date)
            month = f"{dt.month}" if dt.month > 9 else f"0{dt.month}"
            day = f"{dt.day}" if dt.day > 9 else f"0{dt.day}"
            date_desc = f"{day}.{month}.{dt.year} {session_start}:00"
            await message.answer(Dialog.date_desc + f" {date_desc}")
    else:
        await message.answer(Dialog.opening_calendar, reply_markup=ReplyKeyboardRemove())
        await message.answer(Dialog.pick_date, reply_markup=create_calendar())
        await RegistrationState.picking_date.set()


@dp.callback_query_handler(calendar_callback.filter(), state=RegistrationState.picking_date)
async def process_name(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await process_calendar_selection(callback_query, callback_data)
    if selected:
        picked_date = date.strftime("%m/%d/%Y")
        await callback_query.message.answer(f"{Dialog.you_picked_day} {picked_date}")
        # check available time for event
        day_is_ok = DateHelper.day_is_correct(date)
        if not day_is_ok:
            await callback_query.message.answer(Dialog.pick_another_day,
                                                reply_markup=create_calendar())
            return
        available_hours = db.find_all_events_for_day(date)
        if not available_hours:
            await callback_query.message.answer(Dialog.no_available_date,
                                                reply_markup=create_calendar())
            return
        # proceed if date is correct and there are available hours
        hours_markup = return_inline_buttons_for_hours(available_hours)
        await callback_query.message.answer(Dialog.pick_hour, reply_markup=hours_markup)
        await state.update_data(
            {"date": picked_date}
        )
        await RegistrationState.next()


@dp.callback_query_handler(available_hours_callback.filter(), state=RegistrationState.choosing_hour)
async def handle_available_hours(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    picked_hour = callback_data.get("hour")
    await state.update_data(
        {"hour": picked_hour}
    )
    await call.message.answer(f"{Dialog.you_picked_hour} {picked_hour}{Dialog.enter_phone}")
    await call.message.edit_reply_markup(reply_markup=None)
    await RegistrationState.next()


@dp.message_handler(state=RegistrationState.setting_phone_number)
async def ask_phone_number(message: types.Message, state: FSMContext):
    phone = message.text
    await message.answer(text=Dialog.enter_name)
    await state.update_data(
        {"phone": phone}
    )
    await RegistrationState.next()


@dp.message_handler(state=RegistrationState.setting_username)
async def ask_username(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    user_name = message.text
    user_phone = user_data["phone"]
    start_hour = int(user_data["hour"])
    end_hour = int(start_hour + 1)
    dt = DateHelper.get_date_from_string(user_data["date"] + " " + f"{start_hour}")
    month = f"{dt.month}" if dt.month > 9 else f"0{dt.month}"
    day = f"{dt.day}" if dt.day > 9 else f"0{dt.day}"
    date_desc = f"{day}.{month}.{dt.year} {start_hour}:00"
    response = f'{Dialog.name_desc} {user_name}\n' \
               f'{Dialog.phone_desc} {user_phone}\n' \
               f'{Dialog.date_desc} {date_desc}'
    await message.answer(response)
    await state.finish()
    await state.reset_state(with_data=True)

    user_id = message.chat.id
    client_added = db.add_client(user_id=user_id,phone=user_phone, creation_date=f"{datetime.now()}",
                                 registration_date=f"{dt}", start=start_hour, end=end_hour,
                                 user_name=user_name, deposit=0)
    print(client_added)
    await message.answer(Dialog.thanks_for_registration)

