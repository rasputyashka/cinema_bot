from dataclasses import dataclass
import os

import toml


@dataclass
class BotConfig:
    token: str


@dataclass
class DBConfig:
    db_uri: str
    echo: bool = True


@dataclass
class Config:
    bot: BotConfig
    database: DBConfig


def load_config(path: str | None = None) -> Config:
    if path is None:
        path = os.getenv("CONFIG_PATH", "/usr/local/etc/cinemabot.toml")
    with open(path) as f:
        data = toml.load(f)
    return Config(
        BotConfig(**data['tgbot']),
        DBConfig(**data['database'])
    )
