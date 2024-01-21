from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgbot.db.repos.user import UserRepo

class DBMiddleware(BaseMiddleware):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__()
        self.session_maker = session_maker

    async def __call__(self, handler, event, data):
        async with self.session_maker() as session:
            data['repo'] = UserRepo(session)
            return await handler(event, data)
