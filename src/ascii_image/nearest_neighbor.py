"""Lightly optimized nearest-neighbot search for 8d vectors.

:author: Shay Hill
:created: 2026-09-12
"""

from typing import Annotated

import numpy as np
from numpy import typing as npt

from ascii_image.reshape import CharVectors
from ascii_image.sample_chars import ASCII_PRINTABLE_CHAR_PTS

CharVector = Annotated[npt.NDArray[np.floating], (8,)]


def find_nn_char_pnt(query_vector: CharVector, candidates: CharVectors) -> int:
    """Find the nearest neighbor of a query vector in a set of candidate vectors.

    :param query_vector: the vector to find the nearest neighbor for
    :param candidates: the set of candidate vectors to search
    :return: the character point of the nearest neighbor

    Each candidate vector represents a character. Return the character point of the
    nearest neighbor.
    """
    char_pts = np.array(ASCII_PRINTABLE_CHAR_PTS)
    min_sqd_dist = np.sum(query_vector**2)  # to space
    best = char_pts[0]  # space

    candidates = candidates[1:]
    char_pts = char_pts[1:]
    max_axis_deltas = np.max(abs(candidates - query_vector), axis=1)

    while candidates.shape[0]:
        ruled_in = np.where(max_axis_deltas <= np.sqrt(min_sqd_dist))
        candidates = candidates[ruled_in]
        max_axis_deltas = max_axis_deltas[ruled_in]
        char_pts = char_pts[ruled_in]

        for i, candidate in enumerate(candidates):
            sqd_dist = np.sum((candidate - query_vector) ** 2)
            if sqd_dist < min_sqd_dist:
                min_sqd_dist = sqd_dist
                best = char_pts[i]
                candidates = candidates[i + 1 :]
                max_axis_deltas = max_axis_deltas[i + 1 :]
                char_pts = char_pts[i + 1 :]
                break
        else:
            break

    return best
