from __future__ import annotations

__all__ = ["PlainTextRenderer"]


from weavely.blocks.txt import PlainTextData, TitleData

from .base import BlockRendererBase


class PlainTextRenderer(BlockRendererBase[PlainTextData]):
    """
    Renderer for the plain text block.

    Just returns the plain text in the same way it has been formatted.
    """

    _SUPPORTED_DATA_TYPES = (PlainTextData,)

    def _render(self, data: PlainTextData) -> str:
        return data.text


class TitleRenderer(BlockRendererBase[TitleData]):
    """
    Renderer for the title block.

    Respecting converting to a regular plain text, following rules are applied:

    - The first level title is rendered inside a rectangle of provided characters.

    ====================
    =    MAIN TITLE    =
    ====================

    - The second level title is rendered with a line of provided characters beneath it.

    Section Title
    ===============

    - The third level and below are rendered as plain text with a different number of prefix and suffix characters.

    === Subsection Title ===
    ==== Sub-subsection Title ====
    """

    _SUPPORTED_DATA_TYPES = (TitleData,)

    def __init__(self, *, decoration: str = "=", top_level_indent: int = 4, top_level_spacing: int = 2) -> None:
        """
        Initialize the TitleRenderer with a decoration character and top-level indentation.

        Parameters:
            decoration (str): Character used for decoration.
            top_level_indent (int): Number of characters used for indentation at the top level.
            top_level_spacing (int): Number of characters used for spacing at the top level.
        """
        self._decoration = decoration
        self._top_level_indent = top_level_indent
        self._top_level_spacing = top_level_spacing

    def _render(self, data: TitleData) -> str:
        match data.level:
            case 1:
                return self._render_level_1_title(data)
            case 2:
                # Simplify second level formatting
                underline = f"{self._decoration * len(data.title)}"
                return f"{data.title}\n{underline}"
            case _:
                # Prefix and suffix decoration for lower levels
                decoration = f"{self._decoration * data.level}"
                return f"{decoration} {data.title} {decoration}"

    def _render_level_1_title(self, data: TitleData) -> str:
        title = (
            f"{self._decoration * self._top_level_indent}"
            f"{" " * self._top_level_spacing}"
            f"{data.title}"
            f"{" " * self._top_level_spacing}"
            f"{self._decoration * self._top_level_indent}"
        )
        title_len = len(title)
        border = self._decoration * title_len
        f"{self._decoration * (title_len + self._top_level_indent)}"
        return f"{border}\n{title}\n{border}"
