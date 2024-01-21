from abc import ABC, abstractmethod


class BaseUserRepo(ABC):
    @abstractmethod
    def add_user(self, user_dto):
        ...
