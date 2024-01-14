from aiogram.types import Message
from aiogram import Dispatcher

from tgbot.repository.db import UserRepo
from tgbot.models.user_dto import UserDTO


async def start(msg: Message, repo: UserRepo):
    await msg.reply("Start command.")
    from_user = msg.from_user
    if from_user is not None:
        await repo.create_user(UserDTO(from_user.id, from_user.username))


async def get_movie(msg):
    pass


def register_user(dp: Dispatcher):
    dp.message.register(start)
