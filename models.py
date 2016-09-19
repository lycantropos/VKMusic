import os
from datetime import datetime, timedelta, time

from sqlalchemy import Column, Integer, String, DateTime, Time
from sqlalchemy.ext.declarative import declarative_base
from vk_app.models import VKObject
from vk_app.services.loading import download
from vk_app.utils import check_dir

from settings import MAX_FILE_NAME_LEN

Base = declarative_base()

VK_ID_FORMAT = '{}_{}'


class Audio(Base, VKObject):
    FILE_NAME_FORMAT = "{artist} - {title}"
    FILE_EXTENSION = ".mp3"

    __tablename__ = 'audio'
    __table_args__ = {
        'mysql_charset': 'utf8'
    }

    vk_id = Column(String(255), primary_key=True)
    owner_id = Column(Integer, nullable=False)
    audio_id = Column(Integer, nullable=False)

    artist = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    genre_id = Column(Integer, nullable=True)
    lyrics_id = Column(Integer, nullable=True)
    duration = Column(Time, nullable=False)

    date_time = Column(DateTime, nullable=False)
    link = Column(String(255), nullable=True)

    def __init__(self, owner_id: int, audio_id: int, artist: str, title: str, genre_id: int, lyrics_id: int,
                 duration: time, date_time: datetime, link: str):
        # VK utility fields
        self.vk_id = VK_ID_FORMAT.format(owner_id, audio_id)
        self.owner_id = owner_id
        self.audio_id = audio_id

        # info fields
        self.artist = artist
        self.title = title
        self.genre_id = genre_id
        self.lyrics_id = lyrics_id

        # technical info fields
        self.duration = duration
        self.date_time = date_time
        self.link = link

    def __repr__(self):
        return "<Audio(artist='{}', title='{}', duration='{}')>".format(
            self.artist, self.title, self.duration
        )

    def __str__(self):
        return "Audio called '{}'".format(
            Audio.FILE_NAME_FORMAT.format(**self.__dict__)
        )

    @classmethod
    def name(cls):
        return 'audio'

    def download(self, path: str):
        audio_file_subdirs = self.get_file_subdirs()
        check_dir(path, *audio_file_subdirs)

        audio_file_dir = os.path.join(path, *audio_file_subdirs)
        audio_file_name = self.get_file_name()
        audio_file_path = os.path.join(audio_file_dir, audio_file_name)

        download(self.link, audio_file_path)

    def get_file_subdirs(self) -> str:
        audio_file_subdirs = [self.artist]
        return audio_file_subdirs

    def get_file_name(self) -> str:
        file_name = Audio.FILE_NAME_FORMAT.format(
            **self.__dict__
        )[:MAX_FILE_NAME_LEN - len(Audio.FILE_EXTENSION)].replace(os.sep, ' ') + Audio.FILE_EXTENSION
        return file_name

    @classmethod
    def from_raw(cls, raw_vk_object: dict):
        return Audio(owner_id=int(raw_vk_object['owner_id']), audio_id=int(raw_vk_object['id']),
                     artist=raw_vk_object['artist'].strip(), title=raw_vk_object['title'].strip(),
                     genre_id=int(raw_vk_object.pop('genre_id', 0)), lyrics_id=int(raw_vk_object.pop('lyrics_id', 0)),
                     duration=(
                         datetime.min + timedelta(
                             seconds=int(raw_vk_object['duration'])
                         )
                     ).time(), date_time=datetime.fromtimestamp(raw_vk_object['date']),
                     link=raw_vk_object['url'] or None)
