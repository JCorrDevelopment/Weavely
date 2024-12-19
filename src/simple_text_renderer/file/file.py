from __future__ import annotations

from typing import TYPE_CHECKING

from simple_text_renderer.content import Content

if TYPE_CHECKING:
    from simple_text_renderer.formatters.base import FileFormatter
    from simple_text_renderer.renderers.base import FileRenderer


class BaseFile:
    """
    General representation of a file as an idea.

    Responsible for adding, modifying and removing data blocks from the file. As well, it orchestrates the document
    rendering process.

    Blocks are stored inside the file object as a dictionary where the key is the block name and the value is the
    block object itself. This allows to simple block reference, as well as it guarantees block insertion order.
    """

    def __init__(
        self, formatter: FileFormatter | None = None, renderer: FileRenderer | None = None, *, encoding: str = "utf-8"
    ) -> None:
        """
        Args:
            formatter (FileFormatter): Formatter object to format the file.
            renderer (FileRenderer): Renderer object to render the file.
            encoding (str): Encoding of the file content. Default is UTF-8.
        """  # noqa: D205
        self._formatter = formatter
        self._renderer = renderer
        self._content = Content()
        self._encoding = encoding

    @property
    def encoding(self) -> str:
        """
        Get the encoding of the file content.

        Returns:
            str: Encoding of the file content.
        """
        return self._encoding
