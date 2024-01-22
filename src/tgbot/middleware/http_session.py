from aiogram import BaseMiddleware

from tgbot.api.base import BaseAPIClient


class APIMiddleware(BaseMiddleware):
    def __init__(self, api_wrapper: BaseAPIClient):
        super().__init__()
        self.api_wrapper = api_wrapper

    async def __call__(self, handler, event, data):
        data["api_wrapper"] = self.api_wrapper
        return await handler(event, data)
