import asyncio
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.config import PLANS
from src.keyboards.cbs_data.select_plan import SelectPlanCallback, SelectTypeCallback
from src.keyboards.inline_keyboards import select_plan, select_type
from src.states.quiz_states import QuizStates
from src.utils.send_plan import send_users_plan


router = Router()


@router.callback_query(F.data == "select_plan")
async def back_but(callback: CallbackQuery):
    return await callback.message.edit_text(
        text=f"Теперь вы можете выбрать тип программы, которая вас интересует",
        reply_markup=select_type()
    )


@router.callback_query(SelectTypeCallback.filter())
async def select_type_func(callback: CallbackQuery, callback_data: SelectTypeCallback, state: FSMContext):
    plan_type = callback_data.type
    await state.update_data(plan_type=plan_type)
    await state.set_state(QuizStates.select_plan)
    return callback.message.edit_text(
        text=f"{PLANS.get(plan_type)}\n\n"
             f"— Выберите уровень:",
        reply_markup=select_plan()
    )


@router.callback_query(SelectPlanCallback.filter(), StateFilter(QuizStates.select_plan))
async def select_plan_func(callback: CallbackQuery, callback_data: SelectPlanCallback, state: FSMContext):
    plan_level = callback_data.level
    data = await state.get_data()
    plan_type = data.get("plan_type")
    asyncio.create_task(send_users_plan(message=callback.message, fullname=callback.from_user.full_name, plan_type=plan_type, plan=plan_level))

