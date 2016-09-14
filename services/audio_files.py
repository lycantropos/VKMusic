from mutagen.mp3 import MP3


def parse_lastfm(audio_file_path: str):
    audio_file = MP3(audio_file_path)
    audio_file.info.pprint()
