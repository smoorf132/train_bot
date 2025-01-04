
import asyncio
import re
from typing import List
from aiogram import F, Bot, Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import ujson

from src.db.repo import Repo
from src.keyboards.cbs_data.broadcast import ConfirmingCallback
from src.keyboards.inline_keyboards import confirm_mailing, confirm_mailing_media_group, stop_mailing
from src.states.broadcast_states import BroadcastStates
from src.utils.broadcast import Mailing


router = Router()


router.message.filter()


@router.message(Command("send"))
async def send_func(message: Message, state: FSMContext):
    await state.set_state(BroadcastStates.writing)
    await message.answer("Отправь сообщение, которое будет рассылать")


@router.message(
    F.media_group_id,
    BroadcastStates.writing
)
async def sending_media_group_func(
        message: Message,
        state: FSMContext,
        album: List[Message]
):
    group_elements = []
    for element in album:
        caption_kwargs = {"caption": element.html_text, "caption_entities": element.caption_entities, "parse_mode": "html", "show_caption_above_media": message.show_caption_above_media}
        if element.photo:
            input_media = types.InputMediaPhoto(media=element.photo[-1].file_id, **caption_kwargs)
        elif element.video:
            input_media = types.InputMediaVideo(media=element.video.file_id, **caption_kwargs)
        elif element.document:
            input_media = types.InputMediaDocument(media=element.document.file_id, **caption_kwargs)
        elif element.audio:
            input_media = types.InputMediaAudio(media=element.audio.file_id, **caption_kwargs)
        else:
            return message.answer("This media type isn't supported!")
        group_elements.append(input_media)
    await message.answer_media_group(group_elements)
    await message.answer(
        text="Подтвердите начало рассылки.",
        reply_markup=confirm_mailing_media_group()
    )

    album = [model.model_dump() for model in group_elements]
    pack_album = ujson.dumps(album)

    await state.set_state(BroadcastStates.choosing_media_group)
    await state.set_data({"album_pack": pack_album})


@router.message(
    BroadcastStates.writing
)
async def sending_func(
        message: Message,
        bot: Bot,
        state: FSMContext
):
    m = await bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        reply_markup=message.reply_markup
    )
    await message.answer(
        text="Подтвердите начало рассылки.",
        reply_markup=confirm_mailing()
    )
    await state.set_state(BroadcastStates.choosing)
    if message.reply_markup:
        await state.set_data({"msg_id": m.message_id, "reply_markup": ujson.dumps(message.reply_markup.model_dump())})
    else:
        await state.set_data({"msg_id": m.message_id, "reply_markup": "None"})


@router.callback_query(ConfirmingCallback.filter(
                        F.action == "add_buttons"
                    ),
                    BroadcastStates.choosing

)
async def add_buttons_button(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Здесь вы можете добавить url кнопки.\nСинтаксис как в телепосте:\n<b>Кнопка 1 - example.com/</b>", parse_mode="html")
    await state.set_state(BroadcastStates.add_button)


@router.message(BroadcastStates.add_button)
async def extract_data(message: Message, state: FSMContext, bot: Bot):
    line_pattern = r'(.+?)[ -]+((?:https?://)?[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\S*)\s*(?:\||$)'
    builder = InlineKeyboardBuilder()
    sizes = []
    data = await state.get_data()
    msg_id = data.get("msg_id")
    button_data_lines = message.text.strip().split('\n')
    for line in button_data_lines:
        parted = re.findall(line_pattern, line)
        if parted:
            sizes.append(len(parted))
            for i in parted:
                builder.button(text=i[0].strip(), url=i[1].strip())
    builder.adjust(*sizes)
    m = await bot.copy_message(chat_id=message.from_user.id, from_chat_id=message.from_user.id, message_id=msg_id, reply_markup=builder.as_markup())
    await message.answer("Подтвердите начало рассылки", reply_markup=confirm_mailing())
    await state.set_state(BroadcastStates.choosing)
    await state.set_data({"msg_id": m.message_id, "reply_markup": ujson.dumps((builder.as_markup()).model_dump())})


@router.callback_query(
    BroadcastStates.choosing_media_group,
    ConfirmingCallback.filter(  
        F.action == "sure"
    )
)
async def sending_func(
        call: types.CallbackQuery,
        state: FSMContext,
        repo: Repo,
        bot: Bot
):
    data = await state.get_data()
    album_pack = data.get("album_pack")
    await call.message.edit_text(
        text="Рассылка начнется через несколько секунд.",
        reply_markup=stop_mailing()
    )
    mailing = Mailing()
    users = await repo.get_active_users()

    asyncio.create_task(mailing.sending_media_group(
        users=users,
        bot=bot,
        media_group_pack=album_pack,
        from_chat_id=call.from_user.id,
        notif_msg_id=call.message.message_id
    ))
    await call.message.edit_text("<i>Рассылка успешно начата. \nРассылку получат: {} пользователей</i>".format(len(users)), parse_mode="html", reply_markup=stop_mailing())
    await state.clear()


@router.callback_query(
    BroadcastStates.choosing,
    ConfirmingCallback.filter(  
        F.action == "sure"
    )
)
async def sending_func(
        call: types.CallbackQuery,
        state: FSMContext,
        repo: Repo,
        bot: Bot
):
    data = await state.get_data()
    message_id = data.get("msg_id")
    reply_markup = data.get("reply_markup")
    await call.message.edit_text(
        text="Рассылка начнется через несколько секунд.",
        reply_markup=stop_mailing()
    )
    mailing = Mailing()
    users = await repo.get_active_users()

    asyncio.create_task(mailing.copy_sending(
        users=users,
        bot=bot,
        message_id=message_id,
        from_chat_id=call.from_user.id,
        notif_msg_id=call.message.message_id,
        reply_markup=reply_markup
    ))
    await call.message.edit_text("<i>Рассылка успешно начата. \nРассылку получат: {} пользователей</i>".format(len(users)), parse_mode="html", reply_markup=stop_mailing())
    await state.clear()


@router.callback_query(
    ConfirmingCallback.filter(
        F.action == "back"
    )
)
async def back_mailing_button(
        call: types.CallbackQuery,
        state: FSMContext
):
    await state.clear()
    await call.message.edit_text(
        "Рассылка успешно отменена!")


@router.callback_query(
    ConfirmingCallback.filter(
        F.action == "stop"
    )
)
async def stop_mailing_button(
        call: types.CallbackQuery,
        state: FSMContext
):
    await state.clear()
    await call.message.edit_text(
        "Рассылка успешно отменена!")
    exit()

