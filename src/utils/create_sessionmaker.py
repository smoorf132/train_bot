from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


def create_sessionmaker_func(url: str) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    async_engine = create_async_engine(
        url=url,
        echo=True,
        pool_pre_ping=True
    )
    session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
    return async_engine, session_maker