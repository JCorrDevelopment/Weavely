from __future__ import annotations

from typing import Protocol

from simple_text_renderer.blocks.base import BaseBlock, Data


class RendererProtocol[TData: Data](Protocol):
    """
    Protocol describing required interfaces of an object which may be registered as a block renderer.

    Responsible for rendering a block content into a string representation according to the specific document
    format rules.

    Note the difference between `FormatterProtocol` and this protocol.

    Formatters are responsible for data formatting inside the block object, while block renderers are responsible for
    transforming the block data info a representation suitable for the document format.
    """

    def __call__(self, block: BaseBlock[TData]) -> str:
        """
        Render the block content into a string representation.

        Args:
            block (BaseBlock[TData]): Block object to render.

        Returns:
            str: String representation of the block content.

        """
        ...
