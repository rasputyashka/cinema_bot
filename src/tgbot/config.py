from __future__ import annotations

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
    api: APIConfig


@dataclass
class APIConfig:
    base_url: str


def load_config(path: str | None = None) -> Config:
    if path is None:
        path = os.getenv("CONFIG_PATH", "/usr/local/etc/cinemabot.toml")
    with open(path) as f:
        data = toml.load(f)
    return Config(
        BotConfig(**data["tgbot"]),
        DBConfig(**data["database"]),
        APIConfig(**data["api"]),
    )
