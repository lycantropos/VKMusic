from app import MusicApp
from services.database import save_in_db, load_audios_from_db, Session
from settings import APP_ID, USER_LOGIN, USER_PASSWORD, SCOPE, DST_ABSPATH

if __name__ == '__main__':
    music_app = MusicApp(APP_ID, USER_LOGIN, USER_PASSWORD, SCOPE)
    params = dict(owner_id=17547926)
    audios = music_app.load_audios_from_vk(params)
    audios.sort(key=lambda item: item.date_time, reverse=True)
    save_in_db(audios)
    filters = dict()
    session = Session()
    audios = load_audios_from_db(session, filters)
    path = DST_ABSPATH
    for audio in audios:
        audio.synchronize(path)
