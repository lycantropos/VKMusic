import json

from vk_app import App

from services.audios import get_audios_from_raw


class MusicApp(App):
    def __init__(self, app_id: int, user_login='', user_password='', scope='', access_token='', api_version='5.53'):
        super().__init__(app_id, user_login, user_password, scope, access_token, api_version)

    def load_audios(self, params: dict):
        params['access_token'] = self.access_token

        raw_audios = self.get_items('audio.get', params)
        audios = get_audios_from_raw(raw_audios)

        x = 5

