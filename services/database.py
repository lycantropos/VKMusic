from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert

from models import Audio


@compiles(Insert)
def append_string(insert, compiler, **kw):
    s = compiler.visit_insert(insert, **kw)
    if 'append_string' in insert.kwargs:
        return s + " " + insert.kwargs['append_string']
    return s


def save_in_db(audios: list):
    x = Audio.__dict__
    Audio.fields()
    Audio.__table__.insert(append_string='ON DUPLICATE KEY UPDATE =VALUES()')


if __name__ == '__main__':
    save_in_db([])
