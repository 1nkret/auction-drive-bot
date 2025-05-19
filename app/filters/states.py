from aiogram.fsm.state import State, StatesGroup


class EditStates(StatesGroup):
    editing = State()
    edit_mark = State()
    edit_model = State()
    edit_min_year = State()
    edit_max_year = State()
    edit_min_mileage = State()
    edit_max_mileage = State()
    edit_engine_type = State()
    edit_drive_type = State()
    edit_min_price = State()
    edit_max_price = State()
    edit_allow_damaged = State()

    confirm_delete = State()
