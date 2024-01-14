import toml
from dataclasses import dataclass


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


def load_config(path: str) -> Config:
    with open(path) as f:
        data = toml.load(f)
    return Config(
        BotConfig(**data['tgbot']),
        DBConfig(**data['database'])
    )
