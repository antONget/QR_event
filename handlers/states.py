from aiogram.fsm.state import StatesGroup, State


class AddQR(StatesGroup):
    name = State()
    description = State()
    photos = State()
    date = State()


