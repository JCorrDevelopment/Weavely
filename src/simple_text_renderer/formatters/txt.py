import textwrap

from ..blocks.txt import PlainTextData
from .base import BlockFormatterBase


class TextWrapFormatter(BlockFormatterBase[PlainTextData]):
    """
    Wrap the text data in the block to the specified width.

    Args:
        *max_width (int): Maximum width of the text data.
    """

    def __init__(self, max_width: int = 120) -> None:
        self._max_width = max_width

    _SUPPORTED_DATA_TYPES = (PlainTextData,)

    def _format(self, data: PlainTextData) -> PlainTextData:
        data.text = textwrap.fill(data.text, width=self._max_width)
        return data
