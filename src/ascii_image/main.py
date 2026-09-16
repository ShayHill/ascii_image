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


# For each row, a selected color and selected character.
_ImageData = list[list[tuple[tuple[int, int, int], str]]]


def build_ascii_image(
    font_path: Path,
    image_path: Path,
    width: int | None = None,
    height: int | None = None,
) -> _ImageData:
    """Create an ascii-image given a source image and font path.

    :param font_path: path to the font file
    :param image_path: path to the source image
    :param width: width of the ascii-image in characters
        (inferred if only height given)
    :param height: height of the ascii-image in characters
        (inferred if only width given)
    :return: a nested list (one list per row) of tuples (rgb color, char)
    """
    char_vectors = get_font_vectors(font_path)
    image_vectors, image_colors = get_pixel_vectors(image_path, width, height)
    char_pts = [find_nn_char_pnt(vec, char_vectors) for vec in image_vectors]
    zip_colors_charpts = zip(image_colors.reshape((-1, 3)), char_pts, strict=True)
    rgb_chars = ((_unblacken_color(x), chr(y)) for x, y in zip_colors_charpts)
    rows, cols = image_colors.shape[:2]
    return [list(it.islice(rgb_chars, cols)) for _ in range(rows)]


def format_ascii_image_for_term(image_data: _ImageData) -> list[str]:
    """Format an ascii-image for terminal output.

    :param colors: list of RGB colors (from get_ascii_image_data)
    :param chars: list of characters (from get_ascii_image_data)
    :param shape: shape of the ascii-image in characters (from get_ascii_image_data)
    :return: ansi escaped list of strings, one per row.
    """
    return ["".join(format_term(*row)) for row in image_data]


def format_ascii_image_for_html(image_data: _ImageData) -> list[str]:
    """Format an ascii-image for HTML output.

    :param colors: list of RGB colors (from get_ascii_image_data)
    :param chars: list of characters (from get_ascii_image_data)
    :param shape: shape of the ascii-image in characters (from get_ascii_image_data)
    :return: span-tagged list of strings, one per row.
    """
    return ["".join(format_html(*row)) for row in image_data]
