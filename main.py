from pathlib import Path

import numpy as np
from PIL import Image

from svt_helpers import svt_solver


def resize_image(img, width: int):
    width_pct = width / float(img.size[0])
    height = int(float(img.size[1]) * float(width_pct))
    return img.resize((width, height))


def gen_mask(A: np.ndarray, pct: float, random_seed: int) -> np.ndarray:
    shape = A.shape
    ndims = np.prod(shape, dtype=np.int32)
    mask = np.full(ndims, False)
    mask[: int(pct * ndims)] = True
    np.random.seed(random_seed)
    np.random.shuffle(mask)
    mask = mask.reshape(shape)
    return mask


def draw_image(arr: np.ndarray, height: int, width: int, fname: str):
    img = Image.fromarray(
        np.clip(arr, 0, 255).astype(np.uint8).reshape(height, width, -1)
    )
    img.save(fname)


def main():
    fname = "landscape.jpg"
    raw_img = Image.open(fname)
    width = 2048
    img = resize_image(raw_img, width)
    print(f"Raw image size: {raw_img.size}")  # (6000, 4000)
    print(f"Resized image size: {img.size}")  # (2048, 1365)

    # image to numpy array
    img = np.array(img)
    height, width, channel = img.shape
    img = img.reshape(-1, width)
    assert img.shape == (height * channel, width)

    # for faster convergence
    scaled_img = img / 255
    # percentage of sampled pixels
    pct = 0.1
    # for reproducibility
    random_seed = 1234
    mask = gen_mask(A=img, pct=pct, random_seed=random_seed)

    max_iterations = 200
    X = svt_solver(
        M=scaled_img,
        mask=mask,
        n_iters=max_iterations,
        tol=0.2,
        random_state=random_seed,
    )

    path = Path("./output_folder")

    if not path.is_dir():
        path.mkdir()

    # draw_image(img, height, width, path/"original.png")
    draw_image(mask * img, height, width, path / "impaired.png")
    draw_image(X * 255, height, width, path / "recovered.png")


if __name__ == "__main__":
    main()
