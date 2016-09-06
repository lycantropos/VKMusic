import os

from utils import download


class Audio:
    FILE_NAME_FORMAT = "{artist} - {title}"
    FILE_EXTENSION = ".mp3"

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

    def get_audio_file_path(self, save_path: str) -> str:
        audio_file_name = self.get_audio_file_name()
        audio_file_path = os.path.join(save_path, audio_file_name)
        return audio_file_path

    def get_audio_file_name(self) -> str:
        audio_file_name = Audio.FILE_NAME_FORMAT.format(**self.__dict__) + Audio.FILE_EXTENSION
        return audio_file_name

    def download(self, save_path: str):
        audio_link = self.link
        audio_file_path = self.get_audio_file_path(save_path)

        download(audio_link, audio_file_path)
