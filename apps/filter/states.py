from aiogram.fsm.state import State, StatesGroup


class FilterStates(StatesGroup):
    waiting_for_mark = State()
    waiting_for_model = State()
    waiting_for_year = State()
    waiting_for_mileage = State()
    waiting_for_engine_type = State()
    waiting_for_drive_type = State()
    waiting_for_price = State()
    waiting_for_damage = State()