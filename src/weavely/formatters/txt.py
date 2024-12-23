import textwrap

from weavely.blocks.txt import PlainTextData, TitleData

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


class TitleCapitalizationFormatter(BlockFormatterBase[TitleData]):
    """
    Capitalize the first letter of each word in the title.

    More specifically:
        a. For the first-level title, make all letters uppercase.
        b. For the second-level title, capitalize the first letter of each word.

    This formatter should be used only with the TitleData blocks.
    """

    _SUPPORTED_DATA_TYPES = (TitleData,)

    def _format(self, data: TitleData) -> TitleData:
        if data.level == 1:
            data.title = data.title.upper()
        else:
            data.title = data.title.title()

        return data
