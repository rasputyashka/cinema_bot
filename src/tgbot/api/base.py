from abc import ABC, abstractmethod


class BaseAPIClient(ABC):
    @abstractmethod
    async def get_movies_and_series(self, title: str, limit: int, page: int):
        ...

    @abstractmethod
    async def get_watch_link(self, valid_title: str, year: int):
        ...
