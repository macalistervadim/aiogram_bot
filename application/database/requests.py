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
        new_ticket = Tickets()
        session.add(new_ticket)
        await session.commit()
        await session.refresh(new_ticket)  # Обновляем состояние объекта, чтобы получить его ID
        return new_ticket.id