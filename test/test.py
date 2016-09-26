from app import MusicApp
from services.audio_files import parse_lastfm
from settings import APP_ID, USER_LOGIN, USER_PASSWORD, SCOPE, DST_ABSPATH

if __name__ == '__main__':
    music_app = MusicApp(APP_ID, USER_LOGIN, USER_PASSWORD, SCOPE)
    path = DST_ABSPATH
    music_app.synchronize_with_files(path)
    audio_filters = dict()
    audio_files_path = DST_ABSPATH
    db_audios = music_app.data_access_object.load_audios_from_db(audio_filters)
    for db_audio in db_audios:
        parse_lastfm(db_audio, audio_files_path)
