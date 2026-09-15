"""Import functions into the package namespace.

:author: Shay Hill
:created: 2026-09-12
"""

from ascii_image.format_colored_text import format_html, format_term
from ascii_image.main import (
    build_ascii_image,
    format_ascii_image_for_html,
    format_ascii_image_for_term,
)

__all__ = [
    "build_ascii_image",
    "format_ascii_image_for_html",
    "format_ascii_image_for_term",
    "format_html",
    "format_term",
]
