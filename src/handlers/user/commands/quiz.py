from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.db.repo import Repo
from src.keyboards.inline_keyboards import select_plan, select_type
from src.states.quiz_states import QuizStates


def get_basal_metabolism(gender: str, age: int, weight: int, height: int):
    try:
        if gender == "male":
            formula = 66.5 + (13.75 * weight) + (5 * height) - (6.75 * age)
        elif gender == "female":
            formula = 66.5 + (9.55 * weight) + (1.8 * height) - (4.7 * age)
        return round(formula)
    except:
        pass
    return 0


router = Router()



@router.message(
    StateFilter(QuizStates.gender),
    F.text == "Мужчина 🧔🏻"
)
async def set_male_gender(message: Message, state: FSMContext, repo: Repo):
    await state.set_state(QuizStates.age)
    await state.update_data(gender="male")
    await repo.change_user_gender(user_id=message.from_user.id, gender="male")
    return await message.answer(text="Укажите ваш возраст (от 10 до 80 лет)", reply_markup=None)


@router.message(
    StateFilter(QuizStates.gender),
    F.text == "Женщина 👩🏻‍🦱"
)
async def set_male_gender(message: Message, state: FSMContext, repo: Repo):
    await state.set_state(QuizStates.age)
    await state.update_data(gender="female")
    await repo.change_user_gender(user_id=message.from_user.id, gender="female")
    return await message.answer("Укажите ваш возраст (от 10 до 80 лет)", reply_markup=None)


@router.message(
    StateFilter(QuizStates.age),
    F.text.isdigit()
)
async def set_users_age(message: Message, state: FSMContext, repo: Repo):
    age = int(message.text)
    if not (age >= 10 and age <= 80):
        return await message.answer("Укажите возраст в диапазоне от 10 до 80.")
    await state.set_state(QuizStates.weight)
    await state.update_data(age=age)
    await repo.change_user_age(user_id=message.from_user.id, age=age)
    return await message.answer("Укажите ваш вес в кг (от 30 до 200 кг)")


@router.message(
    StateFilter(QuizStates.weight),
    F.text.isdigit()
)
async def set_users_weight(message: Message, state: FSMContext, repo: Repo):
    weight = int(message.text)
    if not (weight >= 30 and weight <= 200):
        return await message.answer("Укажите вес в диапазоне от 30 до 200.")
    await state.set_state(QuizStates.height)
    await state.update_data(weight=weight)
    await repo.change_user_weight(user_id=message.from_user.id, weight=weight)
    return await message.answer("Укажите ваш рост в см (от 120 до 220 см)")


@router.message(
    StateFilter(QuizStates.height),
    F.text.isdigit()
)
async def set_users_height(message: Message, state: FSMContext, repo: Repo):
    GENDERS = {
        "male": "Мужчина 🧔🏻",
        "female": "Женщина 👩🏻‍🦱"
    }

    height = int(message.text)
    if not (height >= 120 and height <= 220):
        return await message.answer("Укажите вес в диапазоне от 30 до 200.")
    await state.update_data(height=height)
    await repo.change_user_height(user_id=message.from_user.id, height=height)

    data = await state.get_data()
    gender = data.get("gender")
    age = data.get("age")
    weight = data.get("weight")
    metabolism = get_basal_metabolism(gender=gender, age=age, weight=weight, height=height)
    train_metabolism = round((metabolism + 400), -2)
    await state.update_data(metabolism=metabolism)
    await state.set_state(QuizStates.select_type)

    await message.answer(
        text=f"Ваши показатели:\n\n"
             f"Пол: {GENDERS.get(gender)}\n"
             f"Возраст: {age} лет\n"
             f"Вес: {weight} кг\n"
             f"Рост: {height} см\n\n"
             f"Ваш дневной метаболизм: {metabolism} ккал\n\n"
             f"При 2-3 тренировках в неделю: {train_metabolism}-{train_metabolism+200} ккал"
    )
    return await message.answer(
        text=f"Теперь вы можете выбрать тип программы, которая вас интересует",
        reply_markup=select_type()
    )


@router.message(
    StateFilter(QuizStates.gender)
)
async def set_gender(message: Message):
    return await message.answer(text="Укажите ваш пол")


@router.message(
    StateFilter(QuizStates.age)
)
async def set_age(message: Message):
    return await message.answer(text="Укажите ваш возраст (от 10 до 80 лет)")


@router.message(
    StateFilter(QuizStates.weight)
)
async def set_weight(message: Message):
    return await message.answer(text="Укажите ваш вес в кг (от 30 до 200 кг)")


@router.message(
    StateFilter(QuizStates.height)
)
async def set_height(message: Message):
    return await message.answer(text="Укажите ваш рост в см (от 120 до 220 см)")
