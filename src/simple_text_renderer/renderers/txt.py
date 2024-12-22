from __future__ import annotations

__all__ = ["PlainTextRenderer"]


from simple_text_renderer.blocks.txt import PlainTextData

from .base import BlockRendererBase


class PlainTextRenderer(BlockRendererBase[PlainTextData]):
    """
    Renderer for the plain text block.

    Just returns the plain text in the same way it has been formatted.
    """

    _SUPPORTED_DATA_TYPES = (PlainTextData,)

    def _render(self, data: PlainTextData) -> str:
        return data.text
