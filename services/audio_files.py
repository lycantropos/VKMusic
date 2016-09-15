import logging
import os

from mutagen.mp3 import MP3

from models import Audio


def parse_lastfm(audio: Audio, path: str):
    audio_file_path = audio.get_file_path(path)
    if os.path.exists(audio_file_path):
        audio_file = MP3(audio_file_path)
        audio_file.info.pprint()
    else:
        logging.warning("File '{}' not found".format(audio_file_path))
