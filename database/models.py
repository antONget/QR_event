from sqlalchemy import String, Integer, DateTime, BigInteger, Boolean, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime


engine = create_async_engine(url='sqlite+aiosqlite:///database/db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = 'Events'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    photo_ids: Mapped[str] = mapped_column(String, default='', nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    reg_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    enter_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    enter_users_ids: Mapped[str] = mapped_column(String, default='', nullable=False)


class User(Base):
    __tablename__ = 'Users'
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    events_ids: Mapped[str] = mapped_column(String, default='', nullable=False)
    role: Mapped[str] = mapped_column(String, default='user')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

from asyncio import run
run(async_main())
