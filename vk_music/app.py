import logging
import os
from typing import List

from vk_app import App
from vk_app.utils import check_dir
from vk_music.models import Audio
from vk_music.services.data_access import DataAccessObject


class MusicApp(App):
    def __init__(self, app_id: int, user_login: str = '', user_password: str = '', scope: str = '',
                 access_token: str = '', api_version: str = '5.57',
                 dao: DataAccessObject = DataAccessObject('sqlite:///music_app.db')):
        super().__init__(app_id, user_login, user_password, scope, access_token, api_version)
        self.dao = dao

    def synchronize(self, images_path: str, **params):
        audios = self.load_audios(**params)
        self.dao.save_audios(audios)
        self.synchronize_files(images_path)

    def synchronize_files(self, path: str):
        audios = self.dao.load_audios()
        audios.sort(key=lambda item: item.date_time)
        files_paths = list(
            os.path.join(root, file)
            for root, dirs, files in os.walk(path)
            for file in files
            if file.endswith('.mp3')
        )
        check_dir(path)
        for audio in audios:
            logging.info(audio)
            audio.synchronize(path, files_paths)

    def load_audios(self, **params) -> List[Audio]:
        raw_audios = self.get_all_objects('audio.get', **params)
        audios = list(
            Audio.from_raw(raw_audio)
            for raw_audio in raw_audios
        )
        return audios
