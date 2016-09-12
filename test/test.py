from app import MusicApp
from services.database import insert_audios
from settings import APP_ID, USER_LOGIN, USER_PASSWORD, SCOPE

if __name__ == '__main__':
    music_app = MusicApp(APP_ID, USER_LOGIN, USER_PASSWORD, SCOPE)
    params = dict(owner_id=17547926)
    audios = music_app.load_audios(params)
    insert_audios(audios)
