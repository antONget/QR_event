from aiogram.fsm.state import StatesGroup, State



class AddQR(StatesGroup):
    name = State()
    description = State()
    photos = State() # 'photo_id1;photo_id2;photo_id3; etc.;'
    date = State()


class AdminSendAll(StatesGroup):
    text = State()
    photo = State()
    