import logging
from aiogram import Bot

from src.config import CIDS
from src.keyboards.inline_keyboards import subscription_check_buttons


async def checker(bot: Bot, user_id: int):
    for CID in CIDS:
        try:
            if (await bot.get_chat_member(chat_id=CID[0], user_id=user_id)).status == 'left':
                return False
        except:
            logging.error("Bad check sub user by id {}".format(CID[0]))
    return True


async def o_p(bot: Bot, user_id: int):
    return await bot.send_message(chat_id=user_id, text='Для использования бота нужно быть подписанным на наши каналы!\n\n'
                         'Подпишись и нажми кнопку «Проверить подписку»',
                         reply_markup=await subscription_check_buttons(bot=bot, user_id=user_id))