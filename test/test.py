import logging

from sqlalchemy.orm import sessionmaker, Session

from app import MusicApp
from services.audio_files import parse_lastfm
from services.database import save_in_db, load_audios_from_db, engine
from settings import APP_ID, USER_LOGIN, USER_PASSWORD, SCOPE, DST_ABSPATH


def synchronize(session: Session, path=DST_ABSPATH):
    music_app = MusicApp(APP_ID, USER_LOGIN, USER_PASSWORD, SCOPE)
    params = dict()
    audios = music_app.load_audios_from_vk(params)
    audios.sort(key=lambda item: item.date_time)
    save_in_db(session, audios)

    filters = dict()
    audios = load_audios_from_db(session, filters)

    for audio in audios:
        logging.info(audio)
        audio.synchronize(path)


if __name__ == '__main__':
    db_session = sessionmaker(bind=engine)()
    try:
        synchronize(db_session)
        audio_filters = dict()
        audio_files_path = DST_ABSPATH
        db_audios = load_audios_from_db(db_session, audio_filters)
        for db_audio in db_audios:
            parse_lastfm(db_audio, audio_files_path)
    finally:
        db_session.close()
