import asyncio
from contextlib import suppress
from typing import List, Union
import random

import ujson as json
from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter, TelegramBadRequest
from pydantic import parse_obj_as

from src.keyboards.inline_keyboards import stop_mailing

InputMedia = Union[
    types.InputMediaPhoto, types.InputMediaVideo,
    types.InputMediaAudio, types.InputMediaDocument
]

def progress_bar(current, total, length=10):
    percent = current / total
    arrow = '🟧' * int(length * percent)
    spaces = '⬜️' * (length - len(arrow))

    return f'{arrow}{spaces} {int(percent * 100)}%'

class Mailing:

    def __init__(self):
        self.lock = asyncio.Lock()
        self.all_count = 0
        self.ban_count = 0
        self.len_users = 0

    async def copy_sending(self, bot: Bot, users, from_chat_id, message_id, notif_msg_id, reply_markup) -> None:
        self.len_users += len(users)
        buttons = InlineKeyboardMarkup.model_validate(json.loads(reply_markup)) if reply_markup != "None" else None
        for chat_id in users:
            async with self.lock:
                with suppress (TelegramBadRequest, TelegramForbiddenError):
                    try:
                        if random.randint(1, 20) == 3:
                            await bot.edit_message_text(
                                    text="<b>Сообщение получило: {}</b>\n\n{}".format(self.all_count, progress_bar(self.all_count, self.len_users)),
                                    chat_id=from_chat_id,
                                    message_id=notif_msg_id,
                                    reply_markup=stop_mailing()
                                )
                        await bot.copy_message(
                            chat_id=chat_id,
                            from_chat_id=from_chat_id, 
                            message_id=message_id,
                            reply_markup=buttons)
                        self.all_count += 1
                        await asyncio.sleep(.05)
                    except TelegramRetryAfter as e:
                        await asyncio.sleep(e.retry_after)
        await bot.edit_message_text(
            text="Рассылка успешно завершена!\n<b>Сообщение получило: {}</b>\n\n{}".format(self.all_count, progress_bar(self.all_count, self.len_users)),
            chat_id=from_chat_id,
            message_id=notif_msg_id
        )


    async def sending_media_group(self, bot: Bot, media_group_pack, users, from_chat_id, notif_msg_id) -> None:
        self.len_users += len(users)
        for chat_id in users:
            async with self.lock:
                with suppress(TelegramBadRequest, TelegramForbiddenError):
                    try:
                        if random.randint(1, 20) == 3:
                            await bot.edit_message_text(
                                    text="<b>Сообщение получило: {}</b>\n\n{}".format(self.all_count, progress_bar(self.all_count, self.len_users)),
                                    chat_id=from_chat_id,
                                    message_id=notif_msg_id,
                                    reply_markup=stop_mailing()
                                )
                        media_group_unpack = json.loads(media_group_pack)
                        media_group = parse_obj_as(List[InputMedia], media_group_unpack)
                        await bot.send_media_group(
                            chat_id=chat_id, 
                            media=media_group)
                        self.all_count += 1
                        await asyncio.sleep(.05)
                    except TelegramRetryAfter as e:
                        await asyncio.sleep(e.retry_after)
        await bot.edit_message_text(
            text="Рассылка успешно завершена!\n<b>Сообщение получило: {}</b>\n\n{}".format(self.all_count, progress_bar(self.all_count, self.len_users)),
            chat_id=from_chat_id,
            message_id=notif_msg_id
        )