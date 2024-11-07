from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config import CIDS
from src.handlers.user import callback
from src.keyboards.cbs_data.broadcast import ConfirmingCallback
from src.keyboards.cbs_data.select_plan import SelectPlanCallback, SelectTypeCallback


def main_menu_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🏋️‍♂️ Пауэрлифтинг и силовые", callback_data="powerlifting")],
                [InlineKeyboardButton(text="💪 Бодибилдинг", callback_data="bodybuilding")]]
    )


def confirm_mailing():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Добавить кнопки",
        callback_data=ConfirmingCallback(
            action="add_buttons"
        )
    )
    builder.button(
        text="Подтвердить",
        callback_data=ConfirmingCallback(
            action="sure"
        )
    )
    builder.button(
        text="Отклонить",
        callback_data=ConfirmingCallback(
            action="back"
        )
    )
    builder.adjust(1, 2)
    return builder.as_markup()


def select_type():
    builder = InlineKeyboardBuilder()
    """
    builder.button(
        text="Пауэрлифтинг и силовые 🏋️‍♂️",
        callback_data=SelectTypeCallback(type="powerlifting").pack()
    )
    """
    builder.button(
        text="Бодибилдинг 💪",
        callback_data=SelectTypeCallback(type="bodybuilding").pack()
    )
    builder.adjust(1)

    return builder.as_markup()


def select_plan():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Для начинающих 👶",
        callback_data=SelectPlanCallback(level="lite").pack()
    )
    builder.button(
        text="Для продвинутых 💪",
        callback_data=SelectPlanCallback(level="medium").pack()
    )
    builder.button(
        text="Для профи 🦍",
        callback_data=SelectPlanCallback(level="hard").pack()
    )
    builder.button(
        text="⬅️ Назад",
        callback_data="select_plan"
    )
    builder.adjust(2, 1)

    return builder.as_markup()


async def subscription_check_buttons(bot: Bot, user_id: int):
    channels_two = InlineKeyboardBuilder()
    for CID in CIDS:
        if (await bot.get_chat_member(CID[0], user_id)).status == 'left':
            channel_key = InlineKeyboardButton(text=CID[2], url=CID[1])
            channels_two.row(channel_key, width=1)
    menu = InlineKeyboardButton(text='Проверить подписку 🔄', callback_data="checksub")
    channels_two.row(menu, width=1)
    return channels_two.as_markup()


def confirm_mailing_media_group():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Подтвердить",
        callback_data=ConfirmingCallback(
            action="sure"
        )
    )

    builder.button(
        text="Отклонить",
        callback_data=ConfirmingCallback(
            action="back"
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def stop_mailing():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Остановить",
        callback_data=ConfirmingCallback(
            action="stop"
        )
    )

    return builder.as_markup()
