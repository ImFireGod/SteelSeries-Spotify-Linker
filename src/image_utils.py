from PIL import Image

from src.utils import fetch_content_path


def convert_color(o):
    if o >= 1:
        return 1
    return 0


def convert_to_bitmap(image_data):
    res = []
    for i in range(0, len(image_data), 8):
        byte = 0
        for j in range(7, -1, -1):
            byte += convert_color(image_data[i + j]) << (7 - j)
        res.append(byte)

    return res


def draw_spotify(image, position):
    with Image.open(fetch_content_path('./assets/spotify-18.png')).convert('1') as im:
        image.paste(im, position)
