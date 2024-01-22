from .base import BaseAPIClient

from aiohttp import ClientSession

from tgbot.core.models.kinopoisk import Content


class APIClient(BaseAPIClient):
    MOVIES_ENDPOINT = "/movie"
    WATCH_LINK_ENDPOINT = "/watch"

    def __init__(self, session: ClientSession):
        self.session = session

    async def get_movies_and_series(
        self, title: str, limit: int, page: int
    ) -> list[Content]:
        params = {"title": title, "limit": limit, "page": page}
        async with self.session.get(
            self.MOVIES_ENDPOINT, params=params
        ) as response:
            resp_json = await response.json()
            models = [Content.from_dict(item) for item in resp_json["docs"]]
            return models

    async def get_watch_link(self, valid_title: str, year: int) -> str:
        params = {"title": valid_title, "year": year}
        async with self.session.get(
            self.WATCH_LINK_ENDPOINT, params=params
        ) as response:
            response_json = await response.json()
            return response_json["link"]
