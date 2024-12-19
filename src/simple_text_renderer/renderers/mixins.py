from __future__ import annotations

import abc
from typing import Protocol

from simple_text_renderer.blocks.base import BaseBlock, Data


class IBlockRenderer(Protocol):
    """
    Protocol describing required interfaces of an object which may be registered as a block renderer.

    Responsible for rendering a block content into a string representation according to the specific document
    format rules.

    Note the difference between `FormatterProtocol` and this protocol.

    Formatters are responsible for data formatting inside the block object, while block renderers are responsible for
    transforming the block data info a representation suitable for the document format.
    """

    def __call__[TData: Data](self, block: BaseBlock[TData]) -> str:
        """
        Render the block content into a string representation.

        Args:
            block (BaseBlock[TData]): Block object to render.

        Returns:
            str: String representation of the block content.

        """
        ...


class BlockRendererBase(IBlockRenderer, abc.ABC):
    """
    Implementation of the `IBlockRenderer` protocol as a callable class.

    Responsible for rendering a block content into a string representation according to the specific document
    format rules.

    Note the difference between formatters and renderers.

    Formatters are responsible for data formatting inside the block object, while block renderers are responsible for
    transforming the block data info a representation suitable for the document format.

    """

    @abc.abstractmethod
    def __call__[TData: Data](self, block: BaseBlock[TData]) -> str:
        """
        Render the block content into a string representation.

        Args:
            block (BaseBlock[TData]): Block object to render.

        Returns:
            str: String representation of the block content.
        """
