import os
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Time, create_engine
from sqlalchemy.ext.declarative import declarative_base
from vk_app import VKObject
from vk_app.utils import download

from settings import MAX_FILE_NAME_LEN, DATABASE_URI

engine = create_engine(DATABASE_URI)
connection = engine.connect()
Base = declarative_base()


class Audio(VKObject, Base):
    FILE_NAME_FORMAT = "{artist} - {title}"
    FILE_EXTENSION = ".mp3"

    __tablename__ = 'audio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vk_id = Column(Integer, primary_key=True, autoincrement=False)
    owner_id = Column(Integer, nullable=False)

    artist = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    genre_id = Column(Integer, nullable=True)
    lyrics_id = Column(Integer, primary_key=True, nullable=True)
    duration = Column(Time, nullable=False)

    date_time = Column(DateTime, nullable=False)
    link = Column(String(255), primary_key=True)

    def __init__(self, vk_id: int, owner_id: int, artist: str, title: str,
                 genre_id: int, lyrics_id: int, duration: int, date_time: datetime, link: str):
        self.vk_id = vk_id
        self.owner_id = owner_id
        self.artist = artist
        self.title = title
        self.genre_id = genre_id
        self.lyrics_id = lyrics_id
        self.duration = duration
        self.date_time = date_time
        self.link = link

    def __str__(self):
        return "Audio called '{}'".format(
            Audio.FILE_NAME_FORMAT.format(**self.__dict__)
        )

    def download(self, save_path: str):
        audio_link = self.link
        audio_file_path = self.get_audio_file_path(save_path)

        download(audio_link, audio_file_path)

    def get_audio_file_path(self, save_path: str) -> str:
        audio_file_name = self.get_audio_file_name()
        audio_file_path = os.path.join(save_path, audio_file_name)
        return audio_file_path

    def get_audio_file_name(self) -> str:
        audio_file_name = Audio.FILE_NAME_FORMAT.format(
            **self.__dict__
        )[:MAX_FILE_NAME_LEN - len(Audio.FILE_EXTENSION)].replace(os.sep, ' ') + Audio.FILE_EXTENSION
        return audio_file_name

    @classmethod
    def from_raw(cls, raw_vk_object: dict):
        return Audio(
            int(raw_vk_object['id']), int(raw_vk_object['owner_id']),
            raw_vk_object['artist'].strip(), raw_vk_object['title'].strip(),
            int(raw_vk_object.pop('genre_id', 0)),
            int(raw_vk_object.pop('lyrics_id', 0)),
            int(raw_vk_object['duration']),
            datetime.strptime(raw_vk_object['date']),
            raw_vk_object['url'],
        )
