import os

from vk_app import VKObject
from vk_app.utils import get_date_from_millis, download

MAX_FILE_NAME_LEN = 139

AUDIO_FILE_NAME_FORMAT = "{artist} - {title}"
AUDIO_FILE_EXTENSION = ".mp3"


class Audio(VKObject):
    def __init__(self, vk_id: int, owner_id: int, artist: str, title: str,
                 genre_id: int, lyrics_id: int, duration: int, date: str, link: str):
        self.id = vk_id
        self.owner_id = owner_id
        self.artist = artist
        self.title = title
        self.genre_id = genre_id
        self.lyrics_id = lyrics_id
        self.duration = duration
        self.date = date
        self.link = link

    def __str__(self):
        return "Audio called '{}'".format(
            AUDIO_FILE_NAME_FORMAT.format(**self.__dict__)
        )

    def download(self, save_path: str):
        audio_link = self.link
        audio_file_path = self.get_audio_file_path(save_path)

        download(audio_link, audio_file_path)

    def get_audio_file_path(self, save_path: str) -> str:
        audio_file_name = self.get_audio_file_name().replace(os.sep, ' ')
        audio_file_path = os.path.join(save_path, audio_file_name)
        return audio_file_path

    def get_audio_file_name(self) -> str:
        audio_file_name = \
            AUDIO_FILE_NAME_FORMAT.format(**self.__dict__)[:MAX_FILE_NAME_LEN] + AUDIO_FILE_EXTENSION
        return audio_file_name

    @classmethod
    def from_raw(cls, raw_vk_object: dict):
        return Audio(
            int(raw_vk_object['id']), int(raw_vk_object['owner_id']),
            raw_vk_object['artist'].strip(), raw_vk_object['title'].strip(),
            int(raw_vk_object.pop('genre_id', 0)),
            int(raw_vk_object.pop('lyrics_id', 0)),
            int(raw_vk_object['duration']),
            get_date_from_millis(raw_vk_object['date']),
            raw_vk_object['url'],
        )
