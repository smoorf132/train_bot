from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.keyboards.reply_keyboards import gender_keyboard
from src.states.quiz_states import QuizStates


router = Router()

@router.message(F.text)
@router.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(QuizStates.gender)
    return await message.answer(
        text=f"⚡️ Добро пожаловать в бота, который поможет найти подходящую программу тренировок для вас.\n\nДля начала вам нужно пройти мини-анкету, чтобы бот подобрал необходимую программу под ваши характеристики. \n\nУкажите ваш пол",
        reply_markup=gender_keyboard()
    )


@router.callback_query(F.data == "checksub")
async def checksub_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(QuizStates.gender)
    await callback.message.delete()
    return await callback.message.answer(
        text=f"⚡️ Добро пожаловать в бота, который поможет найти подходящую программу тренировок для вас.\n\nДля начала вам нужно пройти мини-анкету, чтобы бот подобрал необходимую программу под ваши характеристики. \n\nУкажите ваш пол",
        reply_markup=gender_keyboard()
    )
