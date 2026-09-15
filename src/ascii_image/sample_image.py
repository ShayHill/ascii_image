"""Sample an image at 8 pixels per character.

:author: Shay Hill
:created: 2026-09-11
"""

from pathlib import Path
from typing import Annotated

import numpy as np
from numpy import typing as npt
from PIL import Image

from ascii_image.reshape import CHAR_H, CHAR_W, CharVectors, pixels_to_char_vectors


def _infer_width_height(
    image_size: tuple[int, int], width_in_chars: int | None, height_in_chars: int | None
) -> tuple[int, int]:
    """Match width or height to image aspect ratio if one not given."""
    if width_in_chars is not None and height_in_chars is not None:
        return width_in_chars, height_in_chars
    aspect_ratio = image_size[0] * 2 / image_size[1]
    if width_in_chars is None:
        if height_in_chars is None:
            msg = "Neither width nor height given."
            raise ValueError(msg)
        width_in_chars = round(height_in_chars * aspect_ratio)
    if height_in_chars is None:
        height_in_chars = round(width_in_chars / aspect_ratio)
    return width_in_chars, height_in_chars


def get_pixel_vectors(
    path: Path, width: int | None, height: int | None = None
) -> tuple[CharVectors, Annotated[npt.NDArray[np.uint8], (-1, -1, 3)]]:
    """Sample an image at 8 pixels per character.

    :param path: path to the image file
    :param width: width of the image in characters
    :param height: height of the image in characters
    :return: array of superpixel vectors, (h, w, 3) array of colors
    """
    img = Image.open(path)
    width, height = _infer_width_height(img.size, width, height)
    for_alphas = img.resize(
        (width * CHAR_W, height * CHAR_H), resample=Image.Resampling.BILINEAR
    )
    alphas = np.max(np.array(for_alphas)[:, :, :3], axis=2)
    for_colors = img.resize((width, height), resample=Image.Resampling.BILINEAR)
    return pixels_to_char_vectors(alphas), np.array(for_colors)[:, :, :3]
