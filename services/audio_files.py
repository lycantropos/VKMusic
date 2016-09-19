import logging
import os

from mutagen.mp3 import MP3

from models import Audio


def parse_lastfm(audio: Audio, path: str):
    audio_file_path = audio.get_file_path(path)
    if os.path.exists(audio_file_path):
        audio_file = MP3(audio_file_path)
        tags = audio_file.tags
        if tags:
            tags = dict(tags)
            for tag_key in tags:
                if tags[tag_key]:
                    print(tags[tag_key])
    else:
        logging.warning("File '{}' not found".format(audio_file_path))
