from aiogram.types import Message
from aiogram import Dispatcher

from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.db.models.user import User


async def start(msg: Message, session: AsyncSession):
    await msg.reply("Start command.")
    from_user = msg.from_user
    if from_user is not None:
        await session.merge(User(id=from_user.id, username=from_user.username))
        await session.commit()


def register_user(dp: Dispatcher):
    dp.message.register(start)
