from __future__ import annotations

import asyncio
from datetime import timedelta
from functools import partial
import logging
from asyncio import CancelledError
from typing import TYPE_CHECKING

from aiogram.utils.callback_answer import CallbackAnswerMiddleware
import msgspec
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers.user import setup_handlers
from src.middlewares.album import AlbumMiddleware
from src.middlewares.db_middleware import CheckSubscriptionMiddleware, DbMiddleware, UserMiddleware
from src.settings import Settings
from src.utils.create_sessionmaker import create_sessionmaker_func


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def startup(dispatcher: Dispatcher, bot: Bot, settings: Settings) -> None:
    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Bot started")


async def main() -> None:
    settings = Settings()

    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    sessionmaker = create_sessionmaker_func(url=settings.psql_dsn())

    storage = RedisStorage(
        redis=await settings.redis_dsn(),
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        json_loads=msgspec.json.decode,
        json_dumps=partial(lambda obj: str(msgspec.json.encode(obj), encoding="utf-8")),
    )

    dp = Dispatcher(
        storage=storage,
        settings=settings,
        redis=storage.redis,
    )

    dp.update.middleware(DbMiddleware(session_pool=sessionmaker))
    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp.message.middleware(CheckSubscriptionMiddleware())
    dp.callback_query.middleware(CheckSubscriptionMiddleware())
    dp.message.middleware(AlbumMiddleware())

    dp.include_routers(setup_handlers())
    dp.startup.register(startup)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    loop_factory = asyncio.new_event_loop

    try:
        with asyncio.Runner(loop_factory=loop_factory) as runner:
            runner.run(main())

    except (CancelledError, KeyboardInterrupt):
        __import__("sys").exit(0)
