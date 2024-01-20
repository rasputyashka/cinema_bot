import asyncio
import logging
import sys

from aiohttp import ClientSession
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from tgbot.config import load_config
from tgbot.handlers.user import register_user
from tgbot.middleware.db import DBMiddleware
from tgbot.middleware.http_session import HTTPMiddleware

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )
    config = load_config(sys.argv[1])
    db_config = config.database

    engine = create_async_engine(db_config.db_uri, echo=db_config.echo)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(config.bot.token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher()

    register_user(dispatcher)

    session = ClientSession(config.api.base_url)

    dispatcher.update.middleware(DBMiddleware(sessionmaker))
    dispatcher.update.middleware(HTTPMiddleware(session))

    await dispatcher.start_polling(bot)


def cli():
    asyncio.run(main())
