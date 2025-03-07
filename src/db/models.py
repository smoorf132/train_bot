from datetime import datetime
from sqlalchemy.dialects.postgresql import INTEGER, BIGINT, BOOLEAN, TIMESTAMP, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from src.db.base import BaseModel


class Users(BaseModel):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False, unique=True)
    pm_active: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=True)
    registration_datetime: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False, precision=0),
        nullable=False,
        server_default=expression.text("(now() AT TIME ZONE 'UTC'::text)"),
    )
    gender: Mapped[str] = mapped_column(VARCHAR(6), nullable=True)
    age: Mapped[int] = mapped_column(INTEGER, nullable=True)
    weight: Mapped[int] = mapped_column(INTEGER, nullable=True)
    height: Mapped[int] = mapped_column(INTEGER, nullable=True)

    __table_args__ = {'schema': 'train_bot'}
