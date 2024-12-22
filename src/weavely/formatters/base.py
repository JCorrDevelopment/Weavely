from __future__ import annotations

import abc
from collections.abc import Iterator, MutableMapping
from typing import Protocol, TypeIs

from weavely.blocks.base import Data


class IBlockFormatter(Protocol):
    """
    Protocol for formatters used by the Weavely.

    Respecting the idea to have class-based formatters in general,
    this protocol may be useful to define a common function-based formatter interface.
    """

    def __call__(self, data: Data) -> Data:
        """
        Format the block data according to the formatter rules.

        Args:
            data (Data): Data object to format.

        Returns:
            Data: new or modified data object.
        """
        ...


class BlockFormatterBase[TData: Data](IBlockFormatter, abc.ABC):
    """
    Base class for all formatters in the Weavely.

    Idea is to unify ways of data objects formatting behind the single interface and decouple it from the
    block object itself.

    Each of formatters may implement the `__init__` method to accept any additional parameters required for the
    formatting process.
    """

    _SUPPORTED_DATA_TYPES: tuple[type[Data], ...] = ()

    def __call__(self, data: Data) -> TData:
        """
        Format the block data according to the formatter rules.

        Args:
            data (Data): Data object to format.

        Returns:
            Data: new or modified data object.

        Raises:
            TypeError: If the renderer cannot be applied to the provided data object.
        """
        if not self._can_be_applied(data):
            msg = f"Renderer {self.__class__.__name__!r} cannot be applied to the data {data!r}."
            raise TypeError(msg)
        return self._format(data)

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
    def _format(self, data: TData) -> TData:
        """
        Apply actual rendering logic of the provided data object.

        Args:
            data (Data): Data object to render. Is one of this renderer supported data types.

        Returns:
            Data: Block of the same type with formatted data.
        """


class FileFormatter(MutableMapping[type[Data], IBlockFormatter]):
    """
    Base class to describe a file formatter.

    It used as a container class for default block formatter objects used by File object.

    Selecting of the formatter for specific block will be done in the following order:
        1. If block has a specific formatter object, it will be used.
        2. If it doesn't, file will try to find default formatter in corresponding file formatter instance.
        3. If both are missing, the block will be kept as it is.
    """

    formatters: dict[type[Data], IBlockFormatter]
    """
    Dictionary of default block formatters used by the `File` object.

    Key is a block data type, value is a block formatter object. It may be any object that implements the
    `IBlockFormatter` protocol. So it may be a callable class inheriting from the `BlockFormatterBase` class, or any
    function that repeat IBlockFormatter protocol.
    """

    def __init__(self, formatters: dict[type[Data], IBlockFormatter] | None = None) -> None:
        """
        Initialize the collection of default formatters.

        Args:
            formatters (dict[type[Data], IBlockFormatter]): Dictionary of default formatters
            to initialize the collection with.
        """
        self._formatters: dict[type[Data], IBlockFormatter] = formatters or {}

    def __setitem__(self, key: type[Data], value: IBlockFormatter, /) -> None:
        """
        Set or update the default formatter for the provided block data type.

        Args:
            key (type[Data]): Block data type to set the formatter for.
            value (IBlockFormatter): Formatter object to set. Can be any object that implements
                the `IBlockFormatter` protocol.
        """
        self._formatters[key] = value

    def __delitem__(self, key: type[Data], /) -> None:
        """
        Remove the default formatter for the provided block data type.

        Args:
            key (type[Data]): Block data type to remove the formatter for.

        Raises:
            KeyError: If the formatter is not found for the provided block data type.
        """  # noqa: DOC502
        del self._formatters[key]

    def __getitem__(self, key: type[Data], /) -> IBlockFormatter:
        """
        Get the default formatter for the provided block data type.

        Args:
            key (type[Data]): Block data type to get the formatter for.

        Returns:
            IBlockFormatter: Formatter object for the provided block data type.

        Raises:
            KeyError: If the formatter for the provided block data type is not found.
        """  # noqa: DOC502
        return self._formatters[key]

    def __len__(self) -> int:
        """
        Get the number of formatters in the collection.

        Returns:
            int: Number of formatters in the collection.
        """
        return len(self._formatters)

    def __iter__(self) -> Iterator[type[Data]]:
        """
        Iterate over the formatters in the collection.

        Returns:
            Iterator[type[Data]]: List of data types in the collection.
        """
        return self._formatters.__iter__()
