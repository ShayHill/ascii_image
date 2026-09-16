"""Tests for aspect ratio calculations.

:author: Shay Hill
:created: 2026-09-11
"""

# pyright: reportPrivateUsage=false

import pytest

from ascii_image.sample_image import _infer_width_or_height


class TestInferWidthHeight:
    def test_height_halved(self) -> None:
        """Return height at half aspect ratio when not given."""
        result = _infer_width_or_height((100, 400), 10, None)
        assert result == (10, 20)

    def test_width_inferred(self) -> None:
        """Return width when not given."""
        result = _infer_width_or_height((100, 400), None, 20)
        assert result == (10, 20)

    def test_value_error_on_no_width_or_height(self) -> None:
        """Raise ValueError when neither width nor height given."""
        with pytest.raises(ValueError, match="Neither width nor height"):
            _ = _infer_width_or_height((100, 400), None, None)

    def test_return_width_height(self) -> None:
        """Return width and height when both given."""
        result = _infer_width_or_height((100, 400), 15, 25)
        assert result == (15, 25)
