from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import Insert

from models import Audio
from models import engine


@compiles(Insert)
def append_string(insert, compiler, **kw):
    s = compiler.visit_insert(insert, **kw)
    if 'mysql_append_string' in insert.kwargs:
        return s + " " + insert.kwargs['mysql_append_string']
    return s


Insert.argument_for("mysql", "append_string", None)

Session = sessionmaker(bind=engine)


def save_in_db(audios: list):
    audios_dicts = list(audio.as_dict() for audio in audios)
    info_fields = Audio.info_fields()
    update_str = ' AND '.join(' {0} = VALUES({0})'.format(info_field) for info_field in info_fields)
    with engine.connect() as connection:
        connection.execute(Audio.__table__.insert(mysql_append_string='ON DUPLICATE KEY UPDATE' + update_str),
                           audios_dicts)


def load_audios_from_db(session, filters: dict):
    q = session.query(Audio)

    owner_id = filters.get('owner_id', None)
    if owner_id:
        q.filter(
            Audio.owner_id == owner_id
        )

    artist = filters.get('artist', None)
    if artist:
        q.filter(
            Audio.artist == artist
        )
    title = filters.get('title', None)
    if title:
        q.filter(
            Audio.title.like(title)
        )
    genre_id = filters.get('genre_id', None)
    if genre_id:
        q.filter(
            Audio.genre_id == genre_id
        )

    min_duration = filters.get('min_duration', None)
    if min_duration:
        q.filter(
            Audio.duration >= min_duration
        )
    max_duration = filters.get('max_duration', None)
    if max_duration:
        q.filter(
            Audio.duration <= max_duration
        )

    audios = q.all()
    return audios


if __name__ == '__main__':
    save_in_db([])
