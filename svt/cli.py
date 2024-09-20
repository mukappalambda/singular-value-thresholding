from pathlib import Path

import numpy as np
import typer
from PIL import Image

from svt.common import draw_image, gen_mask, resize_image
from svt.svt_helpers import svt_solver

app = typer.Typer(name="svt-cli")


@app.command()
def main(
    fname: str = typer.Argument(
        default=..., metavar="/path/to/image", help="input image path"
    ),
    random_state: int = typer.Option(default=None, min=0, help="random state"),
    width: int = typer.Option(
        default=500,
        min=0,
        help="resize width; smaller width for faster convergence.",
    ),
    pct: float = typer.Option(
        default=0.1,
        min=0.0,
        max=1.0,
        help="mask percentage; higher percentage for faster convergence",
    ),
    it: int = typer.Option(default=100, min=0, help="maximum iterations"),
):
    """
    Examples:

    $ svt-cli ./input.png

    $ svt-cli ./input.png --pct 0.2

    $ svt-cli ./input.png --it 150
    """
    raw_img = Image.open(fname)
    img = resize_image(raw_img, (width, width))
    print(f"Resized image from {img.size} to {raw_img.size}")

    # image to numpy array
    img = np.array(img)
    height, width, channel = img.shape
    img = img.reshape(-1, width)
    assert img.shape == (height * channel, width)

    # for faster convergence
    scaled_img = img / 255
    # for reproducibility
    mask = gen_mask(A=img, pct=pct, random_state=random_state)

    X = svt_solver(
        M=scaled_img,
        mask=mask,
        n_iters=it,
        tol=0.1,
        random_state=random_state,
    )
    X = np.clip(X, a_min=0, a_max=1) * 255

    impaired_img_path = Path("./impaired.png")
    recovered_img_path = Path("./recovered.png")

    draw_image(mask * img, height, width, impaired_img_path.as_posix())
    draw_image(X, height, width, recovered_img_path.as_posix())
    print(f"generated images: {impaired_img_path} and {recovered_img_path}")


if __name__ == "__main__":
    app()
