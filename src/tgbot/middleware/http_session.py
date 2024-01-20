from aiogram import BaseMiddleware
from aiohttp import ClientSession


class HTTPMiddleware(BaseMiddleware):
    def __init__(self, http_session: ClientSession):
        super().__init__()
        self.http_session = http_session

    async def __call__(self, handler, event, data):
        data["http_session"] = self.http_session
        return await handler(event, data)
