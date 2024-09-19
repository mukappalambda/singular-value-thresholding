from typing import Tuple

import numpy as np
from PIL import Image


def draw_image(
    arr: np.ndarray,
    height: int,
    width: int,
    fname: str,
):
    img = Image.fromarray(
        np.clip(arr, 0, 255).astype(np.uint8).reshape(height, width, -1)
    )
    img.save(fname)


def gen_mask(A: np.ndarray, pct: float, random_state: int = 0) -> np.ndarray:
    """
    Examples
    --------
    >>> mask = gen_mask(arr, pct=0.1, random_state=123)
    """
    shape = A.shape
    ndims = np.prod(shape, dtype=np.int32)
    mask = np.full(ndims, False)
    mask[: int(pct * ndims)] = True
    np.random.seed(random_state)
    np.random.shuffle(mask)
    mask = mask.reshape(shape)
    return mask


def resize_image(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    img = img.copy()
    img.thumbnail(size=size)
    return img
