from __future__ import annotations

from aiohttp import ClientSession
from aiogram.types import (
    Message,
    InlineQuery,
    InputTextMessageContent,
    InlineQueryResultArticle,
    LinkPreviewOptions,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.filters import Command
from aiogram import Dispatcher

from tgbot.models.kinopoisk import Content
from tgbot.db.repos.base import BaseUserRepo
from tgbot.core.models.user import UserDTO


MOVIE_DESCRIPTION_TEMPLATE = """
Название: <code>{movie_name} / {en_name}</code>

Описание: <b>{description}</b>

Жанры: <i>{genres}</i>

Страны выпуска: {countries}

Год выпуска: <code>{year}</code>

Рейтинг кинопоиска: <b>{kinopoisk_rating}</b>

Длительность: <code>{duration}</code> минут
"""

SERIES_DESCRIPTION_TEMPLATE = """
Название: <code>{series_name} / {en_name}</code>

Описание: <b>{description}</b>

Жанры: <i>{genres}</i>

Страны выпуска: {countries}

Годы выхода: <code>{start_year} - {end_year}</code>

Рейтинг кинопоиска: <b>{kinopoisk_rating}</b>

Длительность серии: ~<code>{episode_duration}</code> минут
"""


async def start(msg: Message, repo: BaseUserRepo):
    await msg.reply("Start command.")
    from_user = msg.from_user
    if from_user:
        await repo.add_user(
            UserDTO(id=from_user.id, username=from_user.username, uses=0)
        )


async def get_movies_articles(
    http_session: ClientSession, title: str, page: int
) -> list[Content]:
    params = {"title": title, "limit": 10, "page": page}
    async with http_session.get("/movie", params=params) as response:
        resp_json = await response.json()
        models = [Content.from_dict(item) for item in resp_json["docs"]]
        return models


def get_message(content: Content):
    if content.is_series:
        template = SERIES_DESCRIPTION_TEMPLATE
        return template.format(
            series_name=content.name,
            en_name=content.en_name or content.alternative_name,
            description=content.description or "Отсутствует",
            genres=", ".join(content.genres),
            countries=", ".join(content.countries),
            start_year=content.release_years.start,  # type: ignore
            end_year=content.release_years.end or "н.в.",  # type: ignore
            kinopoisk_rating=content.kinopoisk_rating,
            episode_duration=content.series_length,
        )
    else:
        template = MOVIE_DESCRIPTION_TEMPLATE
        return template.format(
            movie_name=content.name,
            en_name=content.en_name or content.alternative_name,
            description=content.description or "Отсутствует",
            genres=", ".join(content.genres),
            countries=", ".join(content.countries),
            year=content.year,
            kinopoisk_rating=content.kinopoisk_rating,
            duration=content.movie_length,
        )


async def get_rutube_link(
    session: ClientSession, title: str, year: int
) -> str:
    params = {"title": title, "year": year}
    async with session.get("/watch", params=params) as response:
        response_json = await response.json()
        return response_json["link"]


async def get_movies(inline_query: InlineQuery, http_session: ClientSession):
    offset = int(inline_query.offset) if inline_query.offset else 1
    all_content = await get_movies_articles(
        http_session, inline_query.query, page=offset
    )
    results = []
    for content in all_content:
        if content.thumb_url is not None:
            if not content.is_series:
                button = InlineKeyboardButton(
                    text="Смотреть на RUTUBE",
                    url=await get_rutube_link(
                        http_session, content.name, content.year
                    ),
                )
                reply_markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
            else:
                reply_markup = None
            photo = InlineQueryResultArticle(
                id=str(content.id),
                title=content.name,
                description=content.short_descripton,
                input_message_content=InputTextMessageContent(
                    message_text=get_message(content),
                    parse_mode="html",
                    link_preview_options=LinkPreviewOptions(
                        url=content.thumb_url, show_above_text=True
                    ),
                ),
                parse_mode="html",
                thumbnail_url=content.thumb_url,
                reply_markup=reply_markup,
            )
            results.append(photo)
    if len(results) < 10:
        await inline_query.answer(results=results)  # type: ignore
    else:
        await inline_query.answer(
            results=results, next_offset=str(offset + 1)  # type: ignore
        )


def register_user_handlers(dp: Dispatcher):
    dp.message.register(start, Command("start"))
    dp.inline_query.register(get_movies)
