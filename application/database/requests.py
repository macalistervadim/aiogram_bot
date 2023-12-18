from sqlalchemy.ext.asyncio import AsyncSession

from application.database.models import User, Category, Product, async_session, Tickets
from sqlalchemy import select, delete

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

async def get_ticket(id):
    async with async_session() as session:
        result = await session.scalar(select(Tickets.tg_id).where(Tickets.id == id))
        return result

async def get_ticket_user(user_id):
    async with async_session() as session:
        result = await session.scalar(select(Tickets.tg_id).where(Tickets.tg_id == user_id))
        return result

async def close_ticket_in_database(ticket_id):
    async with async_session() as session:
        try:
            await session.execute(delete(Tickets).where(Tickets.id == ticket_id))
            await session.commit()
        except Exception as e:
            print(f"Error closing ticket: {e}")
            await session.rollback()

async def add_user(session: AsyncSession,tg_id):
    try:
        new_user = User(
            tg_id=tg_id
        )

        session.add(new_user)
        await session.commit()
    except Exception:
        pass

async def add_ticket(tg_id):
    async with async_session() as session:
        try:
            new_ticket = Tickets(
                tg_id=tg_id
            )
            session.add(new_ticket)
            await session.commit()
            await session.refresh(new_ticket)  # Обновляем состояние объекта, чтобы получить его ID
            return new_ticket.id
        except Exception:
            return False