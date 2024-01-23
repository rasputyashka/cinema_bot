from ..models.kinopoisk import Content


MOVIE_DESCRIPTION_TEMPLATE = """
Название: <code>{movie_name} / {en_name}</code>

Описание: <b>{description}</b>

Жанры: <i>{genres}</i>

Страны выпуска: {countries}

Год выпуска: <code>{year}</code>

Рейтинг кинопоиска: <b>{kinopoisk_rating}</b>

Длительность: <code>{duration}</code> минут"""

SERIES_DESCRIPTION_TEMPLATE = """
Название: <code>{series_name} / {en_name}</code>

Описание: <b>{description}</b>

Жанры: <i>{genres}</i>

Страны выпуска: {countries}

Годы выхода: <code>{start_year} - {end_year}</code>

Рейтинг кинопоиска: <b>{kinopoisk_rating}</b>

Длительность серии: ~<code>{episode_duration}</code> минут"""


class ContentPresenter:
    def __init__(self, content: Content):
        self.content = content

    def get_series_message(self, template: str):
        content = self.content
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

    def get_movie_message(self, template: str):
        content = self.content
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

    def get_message(self):
        if self.content.is_series:
            return self.get_series_message(
                template=SERIES_DESCRIPTION_TEMPLATE
            )
        else:
            return self.get_movie_message(template=MOVIE_DESCRIPTION_TEMPLATE)
