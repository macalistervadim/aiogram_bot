from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import SQLACLHEMY_URL

engine = create_async_engine(SQLACLHEMY_URL, echo=True)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    teacher: Mapped[str] = mapped_column()
    duration: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()

class Tickets(Base):
    __tablename__ = 'tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True)

class Pcodes(Base):
    __tablename__ = 'pcodes'

    id: Mapped[int] = mapped_column(primary_key=True)
    pcode: Mapped[str] = mapped_column(unique=True)
    count: Mapped[int] = mapped_column()
    discount: Mapped[int] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
