"""Sample all ascii printable chars by rendering them as low-res pixel images.

Each character will be an 8-dimensional vector. Each dimension is one pixel of a
low-res image of the character.

01
23
45
67

Render the entire alphabet into a rasterized image (2-pixels wide per character,
4-pixels tall). Cut up the array of that image to give each character an
8-dimensional vector roughly corresponding to the character shape.

The array manupiluation is pretty much instant, but the rasterization in
INKSCAPE takes a few seconds. Write the rasterized image to the temp directory
as a cache. Expect the cache to periodically disappear.

:author: Shay Hill
:created: 2026-09-11
"""

import tempfile
from pathlib import Path

import numpy as np
import svg_ultralight as su
from PIL import Image

from ascii_image.reshape import CHAR_H, CHAR_W, CharVectors, pixels_to_char_vectors

FONTS = Path("C:/Windows/Fonts")

CASCADIA_MONO = FONTS / "CascadiaMono.ttf"
INKSCAPE = Path("C:/Program Files/Inkscape/bin/inkscape")

ASCII_PRINTABLE_CHAR_PTS = tuple(range(32, 127))

_temp_dir = Path(tempfile.gettempdir()) / "char_vector_cache"


def _get_sample_shape() -> tuple[int, int]:
    """Return the dimensions of the rasterized font sample."""
    return (CHAR_W * len(ASCII_PRINTABLE_CHAR_PTS), CHAR_H)


def _stretch_to_dims(maleable: su.SupportsBounds, dims: tuple[float, float]) -> None:
    """Apply a non-uniform scale to give maleable the shape of the template."""
    maleable.scale = (dims[0] / maleable.width, dims[1] / maleable.height)


def _rasterize_printable_ascii(filename: Path, font: Path) -> None:
    """Rasterize all ASCII printable characters into a dictionary of vectors."""
    ascii_printable = "".join(chr(i) for i in ASCII_PRINTABLE_CHAR_PTS)
    padded_text = su.pad_text(font, ascii_printable)
    _stretch_to_dims(padded_text, _get_sample_shape())
    root = su.new_svg_root_around_bounds(padded_text)
    svg = su.write_svg(filename.with_suffix(".svg"), root)
    _ = su.write_png_from_svg(INKSCAPE, svg)


def _normalize_char_vectors(char_vecs: CharVectors) -> CharVectors:
    """Normalize the character vectors to the range [0, 255].

    Zero values are guaranteed, because the space character will always be eight 0s.
    The maximum value will be non-zero in every situation I can imagine, but check
    that it is 0 to avoid division by 0. It *could* happen if you used a very narrow
    set of characters.
    """
    maxs = np.max(char_vecs, axis=0)
    maxs[np.where(maxs == 0)] = 255
    scalars = 255.0 / maxs
    return np.clip(char_vecs * scalars, 0, 255)


def get_font_vectors(font: Path) -> CharVectors:
    """Return all ASCII printable characters into a dictionary of vectors.

    :param font: Path to the font file.
    :return: a (95, 8) array of character vectors stretched to [0, 255]
    """
    cache = (_temp_dir / f"{font.stem}_{CHAR_W}_{CHAR_H}").with_suffix(".png")
    if not cache.exists():
        _rasterize_printable_ascii(cache, font)
    _rasterize_printable_ascii(cache, font)
    alphas = np.array(Image.open(cache))[:, :, 3]
    char_vecs = pixels_to_char_vectors(alphas)
    return _normalize_char_vectors(char_vecs)


