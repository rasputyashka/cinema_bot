from tgbot.repository.db import BaseUserRepo

class UserService:
    def __init__(self, user_repo: BaseUserRepo):
        self.user_repo = user_repo
    async def get_all_users(self) -> list[User]:
        users = await self.user_repo.get_all_users()
        return users