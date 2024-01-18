from sqlalchemy.ext.asyncio import AsyncSession

from application.database.models import User, Category, async_session, Tickets, Pcodes
from sqlalchemy import select, delete

async def get_categories():
    async with async_session() as session:
        result = await session.execute(select(Category))
        return result.scalars().all()

async def get_course(name):
    async with async_session() as session:
        result = await session.execute(select(Category).where(Category.id == name))
        return result.scalars().all()

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

async def get_ticket_id(user_id):
    async with async_session() as session:
        result = await session.scalar(select(Tickets.id).where(Tickets.tg_id == user_id))
        return result

async def get_users():
    async with async_session() as session:
        result = await session.scalars(select(User.tg_id))
        return result


async def decrease_activation_count(session, pcode_id):
    try:
        pcode = await session.get(Pcodes, pcode_id)

        pcode.count -= 1

        await session.commit()

    except Exception as e:
        print(f"An error occurred while decreasing activation count: {e}")

async def activation_pcode(pcode):
    async with async_session() as session:
        session, pcode_obj = await get_pcode(session, pcode)

        if pcode_obj:
            if pcode_obj.count > 0:
                await decrease_activation_count(session, pcode_obj.id)

                return True, pcode_obj
            else:
                return False, None
        else:
            return False, None

async def get_pcode(session, pcod):
    result = await session.execute(select(Pcodes).where(Pcodes.pcode == pcod))
    pcode = result.scalar()

    if pcode:
        return session, pcode
    else:
        return session, None

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

async def add_pcode(data, session: AsyncSession):
    try:
        pcod = Pcodes(
            pcode=data.get('pcode'),
            count=data.get('validity'),
            discount=data.get('discount')
        )

        session.add(pcod)
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
            await session.refresh(new_ticket)
            return new_ticket.id
        except Exception:
            return False