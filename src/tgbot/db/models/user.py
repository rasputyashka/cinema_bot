from sqlalchemy.orm import Mapped, mapped_column

from tgbot.db.models.base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True, unique=False)
    uses: Mapped[int] = mapped_column(nullable=False, unique=False)
