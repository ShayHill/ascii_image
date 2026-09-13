"""Reshape arrays for conversions in the project.

:author: Shay Hill
:created: 2026-09-12
"""

from typing import Annotated

import numpy as np
from numpy import typing as npt
from paragraphs import par

CharVectors = Annotated[npt.NDArray[np.floating], (-1, 8)]

CHAR_W = 2
CHAR_H = CHAR_W * 2


def pixels_to_char_vectors(
    pixels: Annotated[npt.NDArray[np.uint8], (-1, -1)],
) -> CharVectors:
    """Flatten a 2D image array into a (n, 8) array of 8d vectors.

    Each vector in a 2 column by 4 row block of pixels flattened into a 1D vector of
    length 8.
    """
    if pixels.shape[0] % CHAR_H != 0 or pixels.shape[1] % CHAR_W != 0:
        msg = par(
            f"""Image dimensions {pixels.shape} not divisible by block size
            {(CHAR_H, CHAR_W)}."""
        )
        raise ValueError(msg)
    superpixels = pixels.reshape(
        pixels.shape[0] // CHAR_H, CHAR_H, pixels.shape[1] // CHAR_W, CHAR_W
    )
    return superpixels.transpose(0, 2, 1, 3).reshape(-1, CHAR_H * CHAR_W).astype(float)
