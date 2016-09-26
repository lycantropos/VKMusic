import re
from datetime import time, datetime
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Audio
from settings import DATETIME_FORMAT


class DataAccessObject:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=False)
        self.session = sessionmaker(bind=self.engine)()

    def __del__(self):
        self.session.close()

    def save_in_db(self, audios: List[Audio]):
        for audio in audios:
            self.session.merge(audio)
        self.session.commit()

    def load_audios_from_db(self, filters: dict):
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
        genre_id = filters.get('genre_id')
        if genre_id is not None:
            q = q.filter(
                Audio.genre_id == genre_id
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

        start_time = filters.get('start_time')
        if start_time is not None:
            q = q.filter(
                Audio.date_time >= start_time
            )
        end_time = filters.get('end_time')
        if end_time is not None:
            q = q.filter(
                Audio.date_time <= end_time
            )

        audios = q.all()
        return audios


OWNER_ID_RE = r'^(-?\d+$)$'


def check_filters(filters: dict):
    owner_id = filters.get('owner_id')
    if owner_id is not None:
        filters['owner_id'] = re.match(OWNER_ID_RE, owner_id).group(1)

    artist = filters.get('artist')
    if artist is not None:
        filters['artist'] = str(artist)
    title = filters.get('title')
    if title is not None:
        filters['title'] = str(title)

    genre_id = filters.get('genre_id')
    if genre_id is not None:
        filters['genre_id'] = int(genre_id)

    min_duration = filters.get('min_duration')
    if min_duration is not None:
        filters['min_duration'] = time(second=int(min_duration))
    max_duration = filters.get('max_duration')
    if max_duration is not None:
        filters['max_duration'] = time(second=int(max_duration))

    start_time = filters.get('start_time')
    if start_time is not None:
        filters['start_time'] = datetime.strptime(start_time, DATETIME_FORMAT)
    end_time = filters.get('end_time')
    if end_time is not None:
        filters['end_time'] = datetime.strptime(end_time, DATETIME_FORMAT)
