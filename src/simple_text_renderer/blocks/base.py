from __future__ import annotations

import abc
import dataclasses
from typing import TYPE_CHECKING, Any, Final, Self

from std_utils.more_str.generators import random_string

if TYPE_CHECKING:
    from collections.abc import Sequence

    from simple_text_renderer.formatters.base import FormatterProtocol


@dataclasses.dataclass(slots=True)
class Data:
    """
    Default label for data containing in the block to make operation on block more convenient.

    This class doesn't have any specific information, any specific Data type must be inherited from this class.
    """


class BaseBlock[TData: Data](abc.ABC):
    """
    Base class for all blocks in the simple text renderer.

    Idea of the block is to have a simple way to contain any arbitrary data and operate on it in abstract way. The best
    analogy for this is a simple paragraph in a text editor. It can contain any text, tables, images, etc. But you can
    move the paragraph around, change its style, etc. without knowing what is inside it.

    Parameters:
        data (Data): Data object containing any arbitrary data that block can operate on. Specific data type must be
            defined in the inherited class.
        formatters (Collection[FormatterProtocol[TData]]): Collection of formatters that can be applied to the
            data object.
        name (str | None): Optional name of the block. Used to reference the block in the file. If None, the block
            will generate it based on the class name and some randomized suffix.
    """

    def __init__(
        self, data: TData, name: str | None = None, formatters: Sequence[FormatterProtocol[TData]] = ()
    ) -> None:
        self._data = data
        self._formatters = formatters
        self._name: Final[str] = name or random_string(prefix=self.__class__.__name__)

    @classmethod
    @abc.abstractmethod
    def by_content(
        cls,
        *,
        name: str | None = None,
        formatters: Sequence[FormatterProtocol[TData]] = (),
        **kwargs: Any,  # noqa: ANN401
    ) -> Self:
        """
        Create a new block instance by provided input values.

        Parameters:
            name: Optional name of the block. Used to reference the block in the file. If None, the block
                will generate it based on the class name and some randomized suffix.
            formatters: Collection of formatters that can be applied to the data object.
            kwargs: arbitrary keyword arguments to specify the block content. See specific block implementation for
                details.

        Returns:
            Self: New block instance.
        """

    @property
    def name(self) -> str:
        """
        Guaranteed read-only access to the block name.

        Returns:
            str: Name of the block.
        """
        return self._name

    @property
    def data(self) -> TData:
        """
        Guaranteed read-only access to the block data.

        Returns:
            TData: Data object of the block.
        """
        return self._data

    def format(self, *, inplace: bool = True) -> Self:
        """
        Apply all specified formatters to the block.

        Parameters:
            inplace(bool): If True, modify the block in place and return it.
            If False, return a new block without modifying the original one.
            Keyword-only argument, defaults to True.


        Returns:
            Self: Formatted block as a new or modified instance based on inplace parameter.
        """
        data = self._data
        for formatter in self._formatters:
            data = formatter(data)

        if inplace:
            self._data = data
            return self

        return self.__class__(data=data, name=self._name, formatters=self._formatters)


type TBaseBlock = BaseBlock
