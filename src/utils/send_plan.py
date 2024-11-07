import asyncio
from aiogram.types import FSInputFile, Message

from src.config import PLANS
from src.keyboards.inline_keyboards import select_type


async def send_users_plan(message: Message, fullname: str, plan_type: str, plan: str):
    await message.edit_text("<b>Подбираем наиболее оптимальную программу под ваши данные... ⏳</b>")
    await asyncio.sleep(2)
    plan_file = FSInputFile(
        path=f"plans/{plan_type}/{plan}.xlsx",
        filename=f"{PLANS.get(plan_type, "Программа")} для {fullname}.xlsx"
    )
    await message.delete()
    await message.answer_document(
        caption=f"<b>Тренировка</b>\n\n",
        document=plan_file
    )
    return await message.answer(
        text=f"Здесь вы можете выбрать интересующую вас программу тренировок",
        reply_markup=select_type()
    )
