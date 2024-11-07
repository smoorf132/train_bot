import logging
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.db.repo import Repo
from src.utils.check_sub import checker, o_p


class DbMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        
        async with self.session_pool() as session:
            repo = Repo(session)
            data["repo"] = repo
            data["session"] = session

            return await handler(event, data)


class CheckSubscriptionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user_id = data["event_from_user"].id
        redis: Redis = data["redis"]
        bot: Bot = data["bot"]
        
        status = await redis.get(name=f"sub_{user_id}")
        if not status:
            try:
                check_sub = await checker(bot=bot, user_id=user_id)
                if not check_sub:
                    return await o_p(bot=bot, user_id=user_id)
            except Exception as e:
                logging.error("Some error at checking sub: {}".format(e))
            await redis.set(name=f"sub_{user_id}", value=1, ex=86400)
        return await handler(event, data)


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        
        repo: Repo = data["repo"]
        user_id = data["event_from_user"].id
        redis: Redis = data["redis"]
        user = await redis.get(f"{user_id}")

        if not user:
            user = await repo.get_user(tg_id=user_id)

            if user is None:
                await repo.insert_user(tg_id=user_id)
            await redis.set(name=f"{user_id}", value=1, ex=86400)

        return await handler(event, data)
