from aiogram.filters.state import StatesGroup, State


class QuizStates(StatesGroup):
    gender = State()
    age = State()
    weight = State()
    height = State()
    select_type = State()
    select_plan = State()
