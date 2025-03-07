from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncEngine


class BaseModel(DeclarativeBase):
    def __repr__(self) -> str:
        values = ", ".join(
            [f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns.values()],
        )
        return f"{self.__tablename__}({values})"


async def init_db(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)