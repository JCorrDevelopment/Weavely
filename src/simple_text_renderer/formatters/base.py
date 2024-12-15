from __future__ import annotations

import abc
from typing import Protocol

from simple_text_renderer.blocks.base import Data


class FormatterProtocol[TData: Data](Protocol):
    """
    Protocol for formatters used by the simple text renderer.

    Respecting the idea to have class-based formatters in general,
    this protocol may be useful to define a common function-based formatter interface.
    """

    def __call__(self, data: TData) -> TData:
        """
        Format the block data according to the formatter rules.

        Args:
            data (TData): Data object to format.

        Returns:
            TData: new or modified data object.
        """
        ...


class BaseFormatter[TData: Data](FormatterProtocol[TData], abc.ABC):
    """
    Base class for all formatters in the simple text renderer.

    Idea is to unify ways of data objects formatting behind the single interface and decouple it from the
    block object itself.
    """

    @abc.abstractmethod
    def __call__(self, data: TData) -> TData:
        """
        Format the block data according to the formatter rules.

        Args:
            data (TData): Data object to format.

        Returns:
            TData: new or modified data object.
        """
