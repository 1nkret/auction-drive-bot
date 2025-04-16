from aiogram.fsm.state import StatesGroup, State


class filtersForm(StatesGroup):
    mark = State()
    model = State()
    year = State()
    mileage = State()
    engine_type = State()
    drive_type = State()
    price = State()
    damage = State()
