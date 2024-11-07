from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    def __repr__(self) -> str:
        values = ", ".join(
            [f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns.values()],
        )
        return f"{self.__tablename__}({values})"