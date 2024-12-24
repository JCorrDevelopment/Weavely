from weavely.blocks.heading import Heading
from weavely.errors import DataIsInvalidError
from weavely.renderers.base import BlockRendererBase


class HeadingMarkdownRenderer(BlockRendererBase[Heading]):
    """Renderer for the `Heading` block into a Markdown format."""

    _MAX_HEADING_LEVEL = 6
    _SUPPORTED_DATA_TYPES = (Heading,)

    def _render(self, data: Heading) -> str:
        if data.level > self._MAX_HEADING_LEVEL:
            raise DataIsInvalidError(data_type=Heading, field="level", reason="must be less or equal to")
        return f"{'#' * data.level} {data.text}\n"


class HeadingPlainTextRenderer(BlockRendererBase[Heading]):
    """
    Renderer for the `Heading` block into plain text format.

    Example output:

        Level 1:
        =========
        = Title =
        =========

        Level 2:
        Subtitle
        ========

        Level 3:
          Section
          -------

    Args:
        top_decorator (str): Character for heading levels 1 and 2.
        basic_decorator (str): Character for generic headings.
    """

    _SUPPORTED_DATA_TYPES = (Heading,)
    _LEVEL_1: int = 1
    _LEVEL_2: int = 2

    def __init__(self, top_decorator: str = "=", basic_decorator: str = "-") -> None:
        self._top_decorator = top_decorator
        self._basic_decorator = basic_decorator

    def _render(self, data: Heading) -> str:
        if data.level == self._LEVEL_1:
            # Heading level 1 with a rectangle box
            decoration_line = self._top_decorator * (len(data.text) + 4)
            return f"{decoration_line}\n{self._top_decorator} {data.text} {self._top_decorator}\n{decoration_line}\n"
        if data.level == self._LEVEL_2:
            # Heading level 2 with a line decoration
            decoration = self._top_decorator * len(data.text)
            return f"{data.text}\n{decoration}\n"
        # Generic heading with indentation
        indent = " " * (data.level - 1) * 2
        decoration = self._basic_decorator * len(data.text)
        return f"{indent}{data.text}\n{indent}{decoration}\n"
