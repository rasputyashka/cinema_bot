from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class ReleaseYears:
    start: int
    end: int


@dataclass
class Content:
    id: int
    type: str
    name: str
    en_name: str
    alternative_name: str  # if en_name is missing
    short_descripton: str
    description: str
    thumb_url: str | None
    kinopoisk_rating: float
    year: int
    is_series: bool
    series_length: int
    # movies don't have status
    status: str | None
    # for series, this field is null
    movie_length: int
    # movie's release_year is a empty list
    release_years: ReleaseYears | None
    genres: list[str] = field(default_factory=list)
    countries: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item) -> Content:
        genres = [x["name"] for x in item["genres"]]
        countries = [x["name"] for x in item["countries"]]
        if release_years := item["releaseYears"]:
            start_year = release_years[0]["start"]
            end_year = release_years[0]["end"]
            release_years = ReleaseYears(start=start_year, end=end_year)
        else:
            # by default, releaseYears is an empty list, not None
            release_years = None

        if item["poster"] is None:
            thumb_url = None
        else:
            thumb_url = item['poster']['url']

        return cls(
            id=item["id"],
            type=item["type"],
            name=item["name"],
            en_name=item["enName"],
            alternative_name=item["alternativeName"],
            short_descripton=item["shortDescription"],
            description=item["description"],
            thumb_url=thumb_url,
            kinopoisk_rating=item["rating"]["kp"],
            year=item["year"],
            countries=countries,
            is_series=item["isSeries"],
            genres=genres,
            release_years=release_years,
            movie_length=item["movieLength"],
            status=item["status"],
            series_length=item["seriesLength"],
        )
