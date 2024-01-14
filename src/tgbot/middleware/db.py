from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker

from tgbot.repository.db import UserRepo


class DBMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(self, handler, event, data):
        
        async with self.session_pool() as session:
            data['session'] = session
            data['repo'] = UserRepo(session)
            return await handler(event, data)
