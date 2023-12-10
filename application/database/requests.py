from sqlalchemy.ext.asyncio import AsyncSession

from application.database.models import User, Category, Product, async_session, Tickets
from sqlalchemy import select

async def get_categories():
    async with async_session() as session:
        result = await session.scalars(select(Category))
        return result

async def get_products(category_id):
    async with async_session() as session:
        result = await session.scalars(select(Product).where(Product.category_id == category_id))
        return result

async def get_user(tg_id):
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.tg_id == tg_id))
        if len(result) > 0:
            return True

async def add_user(session: AsyncSession,tg_id):
    try:
        new_user = User(
            tg_id=tg_id
        )

        session.add(new_user)
        await session.commit()
    except Exception:
        pass

async def add_ticket():
    async with async_session() as session:
        # Получаем максимальный номер билета
        max_ticket_number = await session.scalar(select(Tickets.number))

        # Если нет билетов в базе, устанавливаем номер 1
        t_number = max_ticket_number + 1 if max_ticket_number else 1

        new_ticket = Tickets(
            number=t_number
        )

        session.add(new_ticket)
        await session.commit()