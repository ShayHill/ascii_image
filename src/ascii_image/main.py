"""Create an ascii-image given a source image and font path.

:author: Shay Hill
:created: 2026-09-12
"""

import itertools as it
from pathlib import Path
from typing import Annotated

import numpy as np
from basic_colormath import float_tuple_to_8bit_int_tuple
from numpy import typing as npt

from ascii_image.format_colored_text import format_html, format_term
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


def build_ascii_image(
    font_path: Path,
    image_path: Path,
    width: int | None = None,
    height: int | None = None,
) -> tuple[list[tuple[int, int, int]], list[str], tuple[int, int]]:
    """Create an ascii-image given a source image and font path.

    :param font_path: path to the font file
    :param image_path: path to the source image
    :param width: width of the ascii-image in characters
    :param height: height of the ascii-image in characters
    :return: list of RGB colors, list of characters,
        and the shape of the image (height, width).
    """
    char_vectors = get_font_vectors(font_path)
    image_vectors, image_colors = get_pixel_vectors(image_path, width, height)
    char_pts = [find_nn_char_pnt(vec, char_vectors) for vec in image_vectors]
    return (
        [_unblacken_color(x) for x in image_colors.reshape((-1, 3))],
        [chr(x) for x in char_pts],
        image_colors.shape[:2],
    )


def format_ascii_image_for_term(
    colors: list[tuple[int, int, int]], chars: list[str], shape: tuple[int, int]
) -> list[str]:
    """Format an ascii-image for terminal output.

    :param colors: list of RGB colors (from get_ascii_image_data)
    :param chars: list of characters (from get_ascii_image_data)
    :param shape: shape of the ascii-image in characters (from get_ascii_image_data)
    :return: ansi escaped list of strings, one per row.
    """
    colored = format_term(*zip(colors, chars, strict=True))
    h, w = shape
    return ["".join(it.islice(colored, w)) for _ in range(h)]


def format_ascii_image_for_html(
    colors: list[tuple[int, int, int]], chars: list[str], shape: tuple[int, int]
) -> list[str]:
    """Format an ascii-image for HTML output.

    :param colors: list of RGB colors (from get_ascii_image_data)
    :param chars: list of characters (from get_ascii_image_data)
    :param shape: shape of the ascii-image in characters (from get_ascii_image_data)
    :return: span-tagged list of strings, one per row.
    """
    colored = format_html(*zip(colors, chars, strict=True))
    h, w = shape
    return ["".join(it.islice(colored, w)) for _ in range(h)]
