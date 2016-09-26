import logging
from typing import List

from vk_app import App
from vk_app.services.logging_config import LoggingConfig

from models import Audio
from services.data_access import DataAccessObject
from settings import DATABASE_URL, BASE_DIR, LOGGING_CONFIG_PATH, LOGS_PATH


class MusicApp(App):
    def __init__(self, app_id: int, user_login='', user_password='', scope='', access_token='', api_version='5.53'):
        super().__init__(app_id, user_login, user_password, scope, access_token, api_version)
        self.data_access_object = DataAccessObject(DATABASE_URL)
        self.logging_config = LoggingConfig(BASE_DIR, LOGGING_CONFIG_PATH, LOGS_PATH)
        self.logging_config.set()

    def synchronize_with_files(self, path):
        params = dict()
        audios = self.load_audios(params)
        audios.sort(key=lambda item: item.date_time)
        self.data_access_object.save_in_db(audios)

        filters = dict()
        audios = self.data_access_object.load_audios_from_db(filters)

        for audio in audios:
            logging.info(audio)
            audio.synchronize(path)

    def load_audios(self, params: dict) -> List[Audio]:
        params['access_token'] = self.access_token
        raw_audios = self.get_items('audio.get', params)
        audios = list(
            Audio.from_raw(raw_audio)
            for raw_audio in raw_audios
        )
        return audios
