from aiogram.filters.state import StatesGroup, State


class BroadcastStates(StatesGroup):
    writing = State()
    choosing = State()
    choosing_media_group = State()
    add_button = State()
    sending = State()