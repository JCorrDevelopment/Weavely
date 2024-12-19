from __future__ import annotations

import abc
import dataclasses
from typing import Protocol

from simple_text_renderer.blocks.base import Data, TData


class IBlockFormatter(Protocol):
    """
    Protocol for formatters used by the simple text renderer.

    Respecting the idea to have class-based formatters in general,
    this protocol may be useful to define a common function-based formatter interface.
    """

    def __call__[TData: Data](self, data: TData) -> TData:
        """
        Format the block data according to the formatter rules.

        Args:
            data (TData): Data object to format.

        Returns:
            TData: new or modified data object.
        """
        ...


class BlockFormatterBase(IBlockFormatter, abc.ABC):
    """
    Base class for all formatters in the simple text renderer.

    Idea is to unify ways of data objects formatting behind the single interface and decouple it from the
    block object itself.

    Each of formatters may implement the `__init__` method to accept any additional parameters required for the
    formatting process.
    """

    @abc.abstractmethod
    def __call__[TData: Data](self, data: TData) -> TData:
        """
        Format the block data according to the formatter rules.

        Args:
            data (TData): Data object to format.

        Returns:
            TData: new or modified data object.
        """


class Identity(BlockFormatterBase):
    """Formatter that doesn't change the data object."""

    def __call__[Data](self, data: Data) -> Data:
        """
        Returns the data object as is.

        Args:
            data (Data): Data object to format.

        Returns:
            Data: The same data object as input.

        """
        return data


@dataclasses.dataclass(slots=True)
class FileFormatter:
    """
    Base class to describe a file formatter.

    It used as a container class for default block formatter objects used by File object.

    Selecting of the formatter for specific block will be done in the following order:
        1. If block has a specific formatter object, it will be used.
        2. If it doesn't, file will try to find default formatter in corresponding file formatter instance.
        3. If both are missing, the `Identity` formatter wil be used as a global fallback to any block.
    """

    formatters: dict[type[TData], IBlockFormatter] = dataclasses.field(
        default_factory=dict[type[TData], IBlockFormatter]
    )
    """
    Dictionary of default block formatters used by the `File` object.

    Key is a block data type, value is a block formatter object. It may be any object that implements the
    `IBlockFormatter` protocol. So it may be a callable class inheriting from the `BlockFormatterBase` class, or any
    function that repeat IBlockFormatter protocol.
    """
