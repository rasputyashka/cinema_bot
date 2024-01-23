from __future__ import annotations

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

from tgbot.db.repos.base import BaseUserRepo
from tgbot.core.models.user import UserDTO
from tgbot.core.presenters.content import ContentPresenter
from tgbot.api.base import BaseAPIClient


async def start(msg: Message, repo: BaseUserRepo):
    await msg.reply("Start command.")
    from_user = msg.from_user
    if from_user:
        await repo.add_user(
            UserDTO(id=from_user.id, username=from_user.username, uses=0)
        )


async def get_movies(inline_query: InlineQuery, api_client: BaseAPIClient):
    offset = int(inline_query.offset) if inline_query.offset else 1
    all_content = await api_client.get_movies_and_series(
        inline_query.query, limit=10, page=offset
    )
    results = []
    for content in all_content:
        if content.thumb_url is not None:
            if not content.is_series:
                button = InlineKeyboardButton(
                    text="Смотреть на RUTUBE",
                    url=await api_client.get_watch_link(
                        content.name, content.year
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
                    message_text=ContentPresenter(content).get_message(),
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
