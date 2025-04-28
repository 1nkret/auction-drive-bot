from core.models import User


from sqlalchemy.future import select


async def register_user_if_not_exitst(message, session):
    user = (await session.execute(select(User).where(User.telegram_id == message.from_user.id))).scalar_one_or_none()
    if not user:
        phone = message.contact.phone_number if message.contact else None
        user = User(telegram_id=message.from_user.id, phone_number=phone)
        session.add(user)
        await session.commit()