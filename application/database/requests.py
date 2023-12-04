from sqlalchemy.ext.asyncio import AsyncSession

from application.database.models import User, Category, Product, async_session
from sqlalchemy import select

async def get_categories():
    async with async_session() as session:
        result = await session.scalars(select(Category))
        return result

async def get_products(category_id):
    async with async_session() as session:
        result = await session.scalars(select(Product).where(Product.category_id == category_id))
        return result

async def add_user(session: AsyncSession, user_data: dict, tg_id: int):
    new_user = User(
        f_name=user_data["first_name"],
        l_name=user_data["last_name"],
        phone=user_data["phone"],
        tg_id=tg_id
    )

    session.add(new_user)
    await session.commit()