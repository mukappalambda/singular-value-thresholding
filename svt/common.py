from typing import Tuple

from PIL import Image


def resize_image(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    img = img.copy()
    img.thumbnail(size=size)
    return img
