from pathlib import Path

import numpy as np
from PIL import Image

from svt.common import draw_image, gen_mask, resize_image
from svt.svt_helpers import svt_solver


def main():
    """
    Main
    """
    fname = "landscape.jpg"
    raw_img = Image.open(fname)
    width = 600
    img = resize_image(raw_img, (width, width))
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
    random_state = 1234
    mask = gen_mask(A=img, pct=pct, random_state=random_state)

    n_iters = 300
    X = svt_solver(
        M=scaled_img,
        mask=mask,
        n_iters=n_iters,
        tol=0.1,
        random_state=random_state,
    )
    X = np.clip(X, a_min=0, a_max=1) * 255

    path = Path("./output_folder")
    impaired_img_path = path.joinpath("impaired.png")
    recovered_img_path = path.joinpath("recovered.png")
    path.mkdir(parents=True, exist_ok=True)

    draw_image(mask * img, height, width, impaired_img_path.as_posix())
    draw_image(X, height, width, recovered_img_path.as_posix())


if __name__ == "__main__":
    main()
