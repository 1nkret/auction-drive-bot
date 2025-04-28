from core.models import User


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user(session: AsyncSession, user_id: int):
    user = (await session.execute(select(User).where(User.telegram_id == user_id))).scalar_one()
    return user