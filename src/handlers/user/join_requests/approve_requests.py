import asyncio
import logging
from aiogram import Bot, Router
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.types import ChatJoinRequest, FSInputFile

from src.keyboards.reply_keyboards import captcha_keyboard


router = Router()


@router.chat_join_request()
async def accept_application(
    request: ChatJoinRequest,
    bot: Bot
):  
    try:
        await request.approve()
        photo = FSInputFile(path="captcha.jpg")
        await bot.send_photo(chat_id=request.from_user.id, caption="Выбери свой тип телосложения:", photo=photo, reply_markup=captcha_keyboard())
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
    except TelegramForbiddenError:
        return
    except Exception as e:
        logging.error(e)