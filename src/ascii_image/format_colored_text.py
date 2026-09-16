"""Format ((r, g, b), str) into a string with the given formatter.

Two public functions take multiple formatted text `((r, g, b), "text")` or text
`"just text"` and return an iterator of strings with the appropriate formatting
applied.

Tags are shared between strings of the same color, but returned as separate strings
so they can be manipulated. Specifically for this project, split into rows.

:author: Shay Hill
:created: 2026-09-15
"""

import itertools as it
from collections.abc import Callable, Iterator

from basic_colormath import rgb_to_hex

# Optionally colored text (rgb, text) or just text:
RgbText = tuple[tuple[int, int, int] | None, str]

# ansi_open and span_open are Formatter functions.
Formatter = Callable[[tuple[int, int, int]], str]


def _ansi_open(rgb: tuple[int, int, int]) -> str:
    """Formatter: Return an ansi escape code for a given RGB color.

    :param rgb: RGB color tuple
    :return: opening ANSI escape code as a string
    """
    r, g, b = rgb
    return f"\033[38;2;{r};{g};{b}m"


def _span_open(rgb: tuple[int, int, int]) -> str:
    """Formatter: Return a span tag for a given RGB color.

    :param rgb: RGB color tuple
    :return: opening and span tags
    """
    hex_color = rgb_to_hex(rgb)
    return f'<span style="color:{hex_color}">'


def _expand_bare_str_args(*texts: RgbText | str) -> Iterator[RgbText]:
    """Convert bare str arguments to (None, str) tuples and ...

    Minimize tags by deciding when whitespace is unformatted (None). This is preferred
    when:

    - whitespace is at the beginning or end of a string.
      '   <span style=...>text</span>    '
    - whitespace is adjacent to unformatted text.
      '<span style=...>text</span>   Unformatted text'
    - whitespace is between spans of different colors.
      '<span style=style_a>text</span>   <span style=style_b>text</span>'

    ... and when whitespace is arbitrarily formatted. This is preferred when:

    - whitespace bridges spans of the same color.
      '<span style=style_a>text   text</span>'

    When whitespace is found, mark unformatted if text to the left is unformatted. If
    not hold until text on the right is found. If the text on the right is
    unformatted, mark whitespace as unformatted. If both the text on the left and the
    text on the right are formatted, format whitespace with the color of the text on
    the left.
    """
    full = ((None, x) if isinstance(x, str) else x for x in texts)
    full = ((c, t) if t.strip() else (None, t) for c, t in full)

    whitespace_format = None
    consecutive_whitespace: Iterator[str] = iter([])
    for i, (c, t) in enumerate(full):
        if i == len(texts) - 1 or (t.strip() and c is None):
            whitespace_format = None
        if isinstance(c, tuple) or t.strip():
            yield from ((whitespace_format, x) for x in consecutive_whitespace)
            yield (c, t)
            if t.strip():
                whitespace_format = c
            continue
        if whitespace_format is None:  # We prefer unformatted, so yield it.
            yield (None, t)
            continue
        # Hold to see if maybe the text to the right is unformatted.
        consecutive_whitespace = it.chain(consecutive_whitespace, (t,))
    yield from ((whitespace_format, x) for x in consecutive_whitespace)


def format_term(*texts: RgbText | str) -> Iterator[str]:
    """Format (rgb, text) tuples into strings with ansi escape codes.

    :param texts: (rgb, text) tuples and / or bare strings
    :return: Iterator of strings with ansi escape codes
    """
    if not texts:
        return iter([""])
    rgbs, txts = zip(*_expand_bare_str_args(*texts), strict=True)
    begs = (
        _ansi_open(b) if a != b and b is not None else ""
        for a, b in it.pairwise((None, *rgbs))
    )
    ends = (
        "\033[0m" if b != a and b is None else "" for a, b in it.pairwise((*rgbs, None))
    )
    return (f"{b}{t}{e}" for b, t, e in zip(begs, txts, ends, strict=True))


def format_html(*texts: RgbText | str) -> Iterator[str]:
    """Format (rgb, text) tuples into strings with span tags.

    :param texts: (rgb, text) tuples and / or bare strings
    :return: Iterator of strings with span tags
    """
    if not texts:
        return iter([""])
    rgbs, txts = zip(*_expand_bare_str_args(*texts), strict=True)
    begs = (
        _span_open(b) if a != b and b is not None else ""
        for a, b in it.pairwise((None, *rgbs))
    )
    ends = (
        "</span>" if b != a and a is not None else ""
        for a, b in it.pairwise((*rgbs, None))
    )
    return (f"{b}{t}{e}" for b, t, e in zip(begs, txts, ends, strict=True))
