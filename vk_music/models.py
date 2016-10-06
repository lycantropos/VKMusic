from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from vk_app.models.attachments import VKAudio
from vk_app.utils import map_non_primary_columns_by_ancestor

Base = declarative_base()


class Audio(VKAudio, Base):
    __tablename__ = 'audios'
    __table_args__ = {
        'mysql_charset': 'utf8'
    }

    vk_id = Column(String(255), primary_key=True)


map_non_primary_columns_by_ancestor(Audio, VKAudio)
