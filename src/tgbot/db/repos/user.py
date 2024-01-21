from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.db.models import User
from .base import BaseUserRepo
from tgbot.core.models.user import UserDTO


class UserRepo(BaseUserRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user: UserDTO):
        await self.session.merge(
            User(id=user.id, username=user.username, uses=user.uses)
        )
        await self.session.commit()
