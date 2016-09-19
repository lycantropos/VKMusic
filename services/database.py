from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Audio
from settings import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


def save_in_db(session: Session, audios: List[Audio]):
    for audio in audios:
        session.merge(audio)
    session.commit()


def load_audios_from_db(session: Session, filters: dict):
    q = session.query(Audio)

    owner_id = filters.get('owner_id', None)
    if owner_id:
        q = q.filter(
            Audio.owner_id == owner_id
        )

    artist = filters.get('artist', None)
    if artist:
        q = q.filter(
            Audio.artist == artist
        )
    title = filters.get('title', None)
    if title:
        q = q.filter(
            Audio.title.like(title)
        )
    genre_id = filters.get('genre_id', None)
    if genre_id:
        q = q.filter(
            Audio.genre_id == genre_id
        )

    min_duration = filters.get('min_duration', None)
    if min_duration:
        q = q.filter(
            Audio.duration >= min_duration
        )
    max_duration = filters.get('max_duration', None)
    if max_duration:
        q = q.filter(
            Audio.duration <= max_duration
        )

    start_time = filters.get('start_time', None)
    if start_time:
        q = q.filter(
            Audio.date_time >= start_time
        )
    end_time = filters.get('end_time', None)
    if end_time:
        q = q.filter(
            Audio.date_time <= end_time
        )

    audios = q.all()
    return audios
