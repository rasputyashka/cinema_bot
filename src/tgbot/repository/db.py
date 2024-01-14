from asyncpg import Pool

from tgbot.models.user_dto import UserDTO


class UserRepo:
    def __init__(
        self, connection: Pool
    ):  # pool has execute* and fetch* methods
        self.connection = connection

    async def get_user_by_id(self, user_id: int) -> UserDTO | None:
        user = await self.connection.fetchrow(
            "SELECT id, username from users WHERE id = ", user_id
        )
        if user is None:
            return None
        else:
            return UserDTO(user[0], user[1])

    async def create_user(self, user: UserDTO):
        await self.connection.execute(
            "INSERT INTO users VALUES ($1, $2) ON CONFLICT DO NOTHING",
            (user.user_id, user.username),
        )
