from vk_app import App
from vk_app.services.logging_config import LoggingConfig
from vk_app.services.vk_objects import get_vk_objects_from_raw

from models import Audio
from settings import BASE_DIR, LOGGING_CONFIG_PATH, LOGS_PATH


class MusicApp(App):
    def __init__(self, app_id: int, user_login='', user_password='', scope='', access_token='', api_version='5.53'):
        super().__init__(app_id, user_login, user_password, scope, access_token, api_version)
        self.logging_config = LoggingConfig(BASE_DIR, LOGGING_CONFIG_PATH, LOGS_PATH)
        self.logging_config.set()

    def load_audios_from_vk(self, params: dict):
        params['access_token'] = self.access_token
        raw_audios = self.get_items('audio.get', params)
        audios = get_vk_objects_from_raw(Audio, raw_audios)
        return audios
