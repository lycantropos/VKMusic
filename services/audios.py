import logging
from datetime import datetime
from time import sleep

from models import Audio
from .vk_objects import get_raw_vk_object_date


def get_audios_from_raw(raw_audios: list) -> list:
    audios = list(
        Audio(
            int(raw_audio['id']), int(raw_audio['owner_id']),
            raw_audio['artist'], raw_audio['title'],
            int(raw_audio['genre_id']),
            int(raw_audio['lyrics_id']),
            int(raw_audio['duration']),
            get_raw_vk_object_date(raw_audio),
            raw_audio['url'],
        )
        for raw_audio in raw_audios
    )
    return audios


def download_audios(audios: list, save_path: str):
    last_download_time = datetime.utcnow()
    for audio in audios:
        try:
            # we can send request to VK servers only 3 times a second
            time_elapsed_since_last_download = (datetime.utcnow() - last_download_time).total_seconds()
            if time_elapsed_since_last_download < 0.33:
                sleep(0.33 - time_elapsed_since_last_download)
            last_download_time = datetime.utcnow()

            audio.download(save_path)
        except OSError as e:
            # e.g. raises when there is no photo on the server anymore
            logging.info(audio)
            logging.exception(e)
