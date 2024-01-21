from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int
    username: str | None
    uses: int
