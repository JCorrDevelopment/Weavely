from __future__ import annotations

__all__ = ["BlockRendererBase", "FileRenderer", "IBlockRenderer"]

import abc
from collections.abc import Iterator, MutableMapping
from typing import Protocol, TypeIs

from simple_text_renderer.blocks.base import Data


class IBlockRenderer(Protocol):
    """
    Protocol describing required interfaces of an object which may be registered as a block renderer.

    Responsible for rendering a block content into a string representation according to the specific document
    format rules.

    Note the difference between `FormatterProtocol` and this protocol.

    Formatters are responsible for data formatting inside the block object, while block renderers are responsible for
    transforming the block data info a representation suitable for the document format.
    """

    def __call__(self, data: Data) -> str:
        """
        Render the block content into a string representation.

        Args:
            data (Data): Data object to render.

        Returns:
            str: String representation of the block content.

        """
        ...


class BlockRendererBase[TData: Data](IBlockRenderer, abc.ABC):
    """
    Implementation of the `IBlockRenderer` protocol as a callable class.

    Responsible for rendering a block content into a string representation according to the specific document
    format rules.

    Note the difference between formatters and renderers.

    Formatters are responsible for data formatting inside the block object, while block renderers are responsible for
    transforming the block data info a representation suitable for the document format.

    NOTE: TData of the inherited renderer must repeat the `_SUPPORTED_DATA_TYPES` class attribute.
    """

    _SUPPORTED_DATA_TYPES: tuple[type[Data], ...] = ()

    def __call__(self, data: Data) -> str:
        """
        Render the block content into a string representation.

        Args:
            data (Data): Data object to render.

        Returns:
            str: String representation of the block content.

        Raises:
            TypeError: If the renderer cannot be applied to the provided data object.
        """
        if not self._can_be_applied(data):
            msg = f"Renderer {self.__class__.__name__!r} cannot be applied to the data {data!r}."
            raise TypeError(msg)
        return self._render(data)

    def _get_supported_data_types(self) -> tuple[type[Data], ...]:
        """
        Get the list of supported data types for the renderer.

        Returns:
            tuple[type[Data], ...]: List of supported data types.
        """
        return self._SUPPORTED_DATA_TYPES

    def _can_be_applied(self, data: Data) -> TypeIs[TData]:
        """
        Check if the renderer can be applied to the provided data object.

        Args:
            data (Data): Data object to check.

        Returns:
            bool: True if the renderer can be applied to the provided data object, False otherwise.
        """
        return isinstance(data, self._SUPPORTED_DATA_TYPES)

    @abc.abstractmethod
    def _render(self, data: TData) -> str:
        """
        Apply actual rendering logic of the provided data object.

        Args:
            data (TData): Data object to render. Is one of this renderer supported data types.

        Returns:
            str: String representation of the block content.
        """


class FileRenderer(MutableMapping[type[Data], IBlockRenderer]):
    """
    Base class for a collection of default renderers used by the `File` object.

    When any block is rendered, it uses the following order to select the renderer:
        1. If the block has a specific renderer, it will be used.
        2. Otherwise, the default renderer will be used.
        3. If no renderer is found, raises RendererIsUnknownError exception.
    """

    _renderers: dict[type[Data], IBlockRenderer]
    """
    Dictionary of default block renderers used by the `File` object.

    Key is a block data type, value is a block renderer object.
    Block renderer object must implement the `IBlockRenderer` protocol. So it may be a callable class inheriting from
    the `BlockRendererBase` class, or any function that repeat IBlockRenderer protocol.
    """

    def __init__(self, renderers: dict[type[Data], IBlockRenderer] | None = None) -> None:
        """
        Initialize the collection of default renderers.

        Args:
            renderers (dict[type[Data], IBlockRenderer]): Dictionary of default renderers to initialize the collection
                with.
        """
        self._renderers: dict[type[Data], IBlockRenderer] = renderers or {}

    def __setitem__(self, key: type[Data], value: IBlockRenderer, /) -> None:
        """
        Set or update the default renderer for the provided block data type.

        Args:
            key (type[Data]): Block data type to set the renderer for.
            value (IBlockRenderer): Renderer object to set. Can be any object that implements
                the `IBlockRenderer` protocol.
        """
        self._renderers[key] = value

    def __delitem__(self, key: type[Data], /) -> None:
        """
        Remove the default renderer for the provided block data type.

        Args:
            key (type[Data]): Block data type to remove the renderer for.

        Raises:
            KeyError: If the renderer is not found for the provided block data type.
        """  # noqa: DOC502
        del self._renderers[key]

    def __getitem__(self, key: type[Data], /) -> IBlockRenderer:
        """
        Get the default renderer for the provided block data type.

        Args:
            key: Block data type to get the renderer for.

        Returns:
            IBlockRenderer: Renderer object for the provided block data type.

        Raises:
            KeyError: If the renderer for the provided block data type is not found.
        """  # noqa: DOC502
        return self._renderers[key]

    def __len__(self) -> int:
        """
        Return size of the renderers' collection.

        Returns:
            int: Number of renderers in the collection.
        """
        return len(self._renderers)

    def __iter__(self) -> Iterator[type[Data]]:
        """
        Return an iterator over data types in the renderers' collection.

        Returns:
            Iterator[type[Data]]: Iterator over the renderers' collection.
        """
        return self._renderers.__iter__()
