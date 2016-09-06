from vk_app import App, download_vk_objects

from models import Audio
from settings import DST_PATH


class MusicApp(App):
    def __init__(self, app_id: int, user_login='', user_password='', scope='', access_token='', api_version='5.53'):
        super().__init__(app_id, user_login, user_password, scope, access_token, api_version)

    def load_audios(self, params: dict):
        params['access_token'] = self.access_token

        save_path = DST_PATH

        raw_audios = self.get_items('audio.get', params)
        audios = Audio.get_vk_objects_from_raw(raw_audios)
        download_vk_objects(audios, save_path)
