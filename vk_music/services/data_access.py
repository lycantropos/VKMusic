from datetime import time, datetime
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from vk_music.models import Audio


class DataAccessObject:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=False)
        self.session = sessionmaker(bind=self.engine)()

    def __del__(self):
        self.session.close()

    def save_audios(self, audios: List[Audio]):
        for audio in audios:
            self.session.merge(audio)
        self.session.commit()

    def load_audios(self, **filters) -> List[Audio]:
        q = self.session.query(Audio)

        owner_id = filters.get('owner_id')
        if owner_id is not None:
            q = q.filter(
                Audio.owner_id == owner_id
            )

        artist = filters.get('artist')
        if artist is not None:
            q = q.filter(
                Audio.artist == artist
            )
        title = filters.get('title')
        if title is not None:
            q = q.filter(
                Audio.title.like(title)
            )
        genre = filters.get('genre')
        if genre is not None:
            q = q.filter(
                Audio.genre_id == genre
            )

        min_duration = filters.get('min_duration')
        if min_duration is not None:
            q = q.filter(
                Audio.duration >= min_duration
            )
        max_duration = filters.get('max_duration')
        if max_duration is not None:
            q = q.filter(
                Audio.duration <= max_duration
            )

        start_datetime = filters.get('start_datetime')
        if start_datetime is not None:
            q = q.filter(
                Audio.date_time >= start_datetime
            )
        end_datetime = filters.get('end_datetime')
        if end_datetime is not None:
            q = q.filter(
                Audio.date_time < end_datetime
            )

        audios = q.all()
        return audios


def check_filters(filters: dict):
    owner_id = filters.get('owner_id')
    if owner_id is not None:
        filters['owner_id'] = int(owner_id)

    artist = filters.get('artist')
    if artist is not None:
        filters['artist'] = str(artist).strip()
    title = filters.get('title')
    if title is not None:
        filters['title'] = str(title).strip()

    genre = filters.get('genre')
    if genre is not None:
        filters['genre'] = str(genre).title()

    min_duration = filters.get('min_duration')
    if min_duration is not None:
        min_duration = int(min_duration)
        minutes, seconds = divmod(min_duration, 60)
        hours, minutes = divmod(minutes, 60)
        filters['min_duration'] = time(hour=hours, minute=minutes, second=seconds)
    max_duration = filters.get('max_duration')
    if max_duration is not None:
        max_duration = int(max_duration)
        minutes, seconds = divmod(max_duration, 60)
        hours, minutes = divmod(minutes, 60)
        filters['max_duration'] = time(hour=hours, minute=minutes, second=seconds)

    start_datetime = filters.get('start_datetime')
    if start_datetime is not None:
        filters['start_datetime'] = datetime.utcfromtimestamp(start_datetime)
    end_datetime = filters.get('end_datetime')
    if end_datetime is not None:
        filters['end_datetime'] = datetime.utcfromtimestamp(end_datetime)
