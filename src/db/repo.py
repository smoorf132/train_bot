from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Users

class Repo:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def change_user_status(self, user_id: int, pm_active: bool):
        stmt = (
            update(Users)
            .where(Users.user_id == user_id)
            .values(pm_active=pm_active)
        )
        await self.session.execute(stmt)
        await self.commit()


    async def change_user_age(self, user_id: int, age: int):
        stmt = (
            update(Users)
            .where(Users.user_id == user_id)
            .values(age=age)
        )
        await self.session.execute(stmt)
        await self.commit()


    async def change_user_weight(self, user_id: int, weight: int):
        stmt = (
            update(Users)
            .where(Users.user_id == user_id)
            .values(weight=weight)
        )
        await self.session.execute(stmt)
        await self.commit()


    async def change_user_height(self, user_id: int, height: int):
        stmt = (
            update(Users)
            .where(Users.user_id == user_id)
            .values(height=height)
        )
        await self.session.execute(stmt)
        await self.commit()


    async def change_user_gender(self, user_id: int, gender: str):
        stmt = (
            update(Users)
            .where(Users.user_id == user_id)
            .values(gender=gender)
        )
        await self.session.execute(stmt)
        await self.commit()


    async def get_user(self, tg_id: int):
        return (await self.session.scalars(select(Users).where(Users.user_id == tg_id))).one_or_none()


    async def get_active_users(self):
        return list(await self.session.scalars(select(Users.user_id).where(Users.pm_active == True).limit(None)))


    async def insert_user(self, tg_id: int):
        stmt = (
            insert(Users)
            .values(user_id=tg_id)
            .returning(Users)
        )
        res = await self.session.scalar(stmt)
        await self.commit()
        return res


    async def commit(self):
        await self.session.commit()