"""Create an ascii-image given a source image and font path.

:author: Shay Hill
:created: 2026-09-12
"""

from pathlib import Path

from ascii_image.paths import FONTS, PROJECT_ROOT
from ascii_image.sample_chars import get_font_vectors
from ascii_image.sample_image import get_pixel_vectors


def new_ascii_image(
    font_path: Path,
    image_path: Path,
    width: int | None = None,
    height: int | None = None,
) -> tuple[list[str], list[tuple[int, int, int]]]:
    """Create an ascii-image given a source image and font path.

    :param font_path: path to the font file
    :param image_path: path to the source image
    :param width: width of the ascii-image in characters
    :param height: height of the ascii-image in characters
    :return: ascii-image as a string
    """
    char_vectors = get_font_vectors(font_path)
    image_vectors = get_pixel_vectors(image_path, width, height)


if __name__ == "__main__":
    image_path = PROJECT_ROOT / "the_ancient_oasis.png"
    CASCADIA_MONO = FONTS / "CascadiaMono.ttf"
    _ = new_ascii_image(CASCADIA_MONO, image_path, 100)
    print("done")
