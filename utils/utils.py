import os
from urllib.request import urlopen


def download(link: str, save_path: str):
    if not os.path.exists(save_path):
        response = urlopen(link)
        if response.status == 200:
            with open(save_path, 'wb') as out:
                image_content = response.read()
                out.write(image_content)
