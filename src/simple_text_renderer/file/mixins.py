from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from simple_text_renderer.blocks.text import PlainText, PlainTextBlock

if TYPE_CHECKING:
    from collections.abc import Sequence

    from simple_text_renderer.blocks.base import TBaseBlock
    from simple_text_renderer.formatters.base import FormatterProtocol


class StdFileProtocol(Protocol):
    """
    Protocol describing required interfaces of a SimpleFile object class.

    Any mixins used by SimpleFile must implement this protocol.
    """

    _blocks: dict[str, TBaseBlock]

    def add_block(self, block: TBaseBlock) -> str: ...  # noqa: D102 - Interface only, no need for docstring


class WithPlainTextMixin(StdFileProtocol):
    """Mixin class for SimpleFile object to provide methods for working with plain text blocks."""

    def add_plain_text(
        self, text: str, name: str | None = None, formatters: Sequence[FormatterProtocol[PlainText]] = ()
    ) -> str:
        """
        Add a text to a file as a plain text block.

        Parameters:
            text (str): Text to add to the file.
            name (str | None): Optional name of the block. Used to reference the block in the file. If None, the block
                will generate it based on the class name and some randomized suffix.
            formatters (Sequence[FormatterProtocol[PlainText]]): Collection of formatters to be applied to the data.

        Returns:
            Name of the created block.
        """
        block = PlainTextBlock.by_content(name=name, formatters=formatters, text=text)
        return self.add_block(block)
