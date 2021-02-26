from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationState(StatesGroup):
    picking_date = State()
    choosing_hour = State()
    setting_phone_number = State()
    setting_username = State()
    giving_instructions = State()
