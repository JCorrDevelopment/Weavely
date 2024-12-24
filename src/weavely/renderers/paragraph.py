import textwrap

from weavely.blocks.paragraph import Paragraph
from weavely.renderers.base import BlockRendererBase


class WrappedParagraphRenderer(BlockRendererBase[Paragraph]):
    """
    Render a paragraph block into a wrapped text format.

    Args:
        width (int): Maximum width of the paragraph text. Default is 120.
    """

    def __init__(self, width: int = 120) -> None:
        self._width = width

    _SUPPORTED_DATA_TYPES = (Paragraph,)

    def _render(self, data: Paragraph) -> str:
        return textwrap.fill(data.text, width=self._width)
