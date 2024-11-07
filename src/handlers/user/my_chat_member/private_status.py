from aiogram import Bot, Router
from aiogram.filters.chat_member_updated import (KICKED, MEMBER,
                                                 ChatMemberUpdatedFilter)
from aiogram.types import ChatMemberUpdated

from src.db.repo import Repo


router = Router()


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=KICKED >> MEMBER)
)
async def user_unblocked_bot(
        event: ChatMemberUpdated,
        bot: Bot,
        repo: Repo
):
    await repo.change_user_status(user_id=event.from_user.id, pm_active=True)


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=MEMBER >> KICKED)
)
async def user_blocked_bot(
        event: ChatMemberUpdated,
        repo: Repo
):
    await repo.change_user_status(user_id=event.from_user.id, pm_active=False)