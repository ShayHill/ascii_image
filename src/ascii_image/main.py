"""Create an ascii-image given a source image and font path.

:author: Shay Hill
:created: 2026-09-12
"""

from pathlib import Path
from typing import Annotated

import numpy as np
from basic_colormath import float_tuple_to_8bit_int_tuple
from numpy import typing as npt

from ascii_image.nearest_neighbor import find_nn_char_pnt
from ascii_image.sample_chars import get_font_vectors
from ascii_image.sample_image import get_pixel_vectors


def _unblacken_color(
    rgb: Annotated[npt.NDArray[np.uint8], (-1, 3)], dampen: float = 0.5
) -> tuple[int, int, int]:
    """Remove some black from a color.

    The blackness in each pixel color has been replaced with black parts of the
    character shape. In theory, this means we could remove all black from the color
    applied to the character, and the net shade would be the same. Perhaps, if you
    stood far back enough it would, but the best look subjectively is to dampen the
    "unblackening" by 50%.
    """
    if max(rgb) == 0:
        return (0, 0, 0)
    scale = dampen + (1 - dampen) * 255 / max(rgb)
    r, g, b = (x * scale for x in rgb)
    return float_tuple_to_8bit_int_tuple((r, g, b))


def colored_char(char: str, rgb: tuple[int, int, int]) -> str:
    """Return a colored character using ANSI escape codes.

    :param char: character to color
    :param rgb: RGB color tuple
    :return: colored character as a string
    """
    r, g, b = rgb
    return f"\033[38;2;{r};{g};{b}m{char}\033[0m"


def new_ascii_image(
    font_path: Path,
    image_path: Path,
    width: int | None = None,
    height: int | None = None,
) -> list[str]:
    """Create an ascii-image given a source image and font path.

    :param font_path: path to the font file
    :param image_path: path to the source image
    :param width: width of the ascii-image in characters
    :param height: height of the ascii-image in characters
    :return: ascii-image as a string
    """
    char_vectors = get_font_vectors(font_path)
    image_vectors, image_colors = get_pixel_vectors(image_path, width, height)
    char_pts = [find_nn_char_pnt(vec, char_vectors) for vec in image_vectors]
    chars = [chr(x) for x in char_pts]
    flat_colors = [_unblacken_color(x) for x in image_colors.reshape((-1, 3))]

    result: list[str] = []
    for _ in range(image_colors.shape[0]):
        chrs = chars[: image_colors.shape[1]]
        cols = flat_colors[: image_colors.shape[1]]
        result.append(
            "".join(colored_char(c, col) for c, col in zip(chrs, cols, strict=True))
        )
        chars = chars[image_colors.shape[1] :]
        flat_colors = flat_colors[image_colors.shape[1] :]
    return result

