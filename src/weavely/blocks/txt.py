from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any, Self

from weavely.blocks import BaseBlock, Data
from weavely.errors import DataIsMissingError, TitleIsEmptyError, TitleLevelIsInvalidError

if TYPE_CHECKING:
    from weavely.formatters.base import IBlockFormatter
    from weavely.renderers.base import IBlockRenderer


@dataclasses.dataclass(slots=True)
class PlainTextData(Data):
    """
    Data class for containing plain text data.

    Attributes:
        text (str): Plain text data.
    """

    text: str


@dataclasses.dataclass(slots=True)
class TitleData(Data):
    """
    Data class for representing a title.

    Attributes:
        title (str): Title text to be displayed.
        level (int): Level of the title. Lower level means higher priority. Default is 1.
    """

    title: str
    """
    Arbitrary title text.
    """
    level: int = 1
    """
    Defines the level of the title.

    Lover number means bigger title importance. Default is 1.
    """

    def __post_init__(self) -> None:
        """
        Validate the provided title information.

        Ensures in the following:
            - The title is not empty.
            - The level is a positive integer.

        Raises:
            TitleIsEmptyError: If the title is empty.
            TitleLevelIsInvalidError: If the level is not a positive integer.
        """
        if not self.title:
            msg = f"Title cannot be empty. Got: {self.title!r}"
            raise TitleIsEmptyError(msg)
        if self.level < 1:
            msg = f"Title level must be a positive integer. Got: {self.level!r}"
            raise TitleLevelIsInvalidError(msg)


class Title(BaseBlock[TitleData]):
    """Describe a title block in the content."""

    @classmethod
    def by_data(
        cls,
        *,
        name: str | None = None,
        formatter: IBlockFormatter | None = None,
        renderer: IBlockRenderer | None = None,
        **data: Any,  # noqa: ANN401
    ) -> Self:
        """
        Create a new Title block by providing the title data.

        Args:
            name (str | None): Name of the block. If not specified, it will be generated automatically.
            formatter (IBlockFormatter | None): Specific formatter to use for this block.
            renderer (IBlockRenderer | None): Specific renderer to use for this block.
            **data (Any): Number of keyword arguments to initialize the block data. Must contain the `title` key.

        Keyword Args:
            title (str): Title text.
            level (int): Title level. If not specified, default will be used.

        Returns:
            Title: New Title block object.

        Raises:
            DataIsMissingError: If the `title` key is not present in the `data` dictionary.W
        """
        if "title" not in data:
            msg = "`**data` dictionary must contain the `title` key."
            raise DataIsMissingError(msg)

        title = data["title"]
        level = data.get("level")

        if level is not None:
            return cls(TitleData(title=title, level=level), name=name, formatter=formatter, renderer=renderer)

        return cls(TitleData(title=title), name=name, formatter=formatter, renderer=renderer)


class PlainText(BaseBlock[PlainTextData]):
    """Block containing plain text data."""

    @classmethod
    def by_data(
        cls,
        *,
        name: str | None = None,
        formatter: IBlockFormatter | None = None,
        renderer: IBlockRenderer | None = None,
        **data: Any,  # noqa: ANN401
    ) -> Self:
        """
        Create a new PlainText block by providing the text data.

        Args:
            name (str | None): Name of the block. If not specified, it will be generated automatically.
            formatter (IBlockFormatter | None): Specific formatter to use for this block.
            renderer (IBlockRenderer[Data] | None): Specific renderer to use for this block.
            **data (Any): Number of keyword arguments to initialize the block data. Must contain the `text` key.

        Keyword Args:
            text (str): Plain text data.

        Returns:
            PlainText: New PlainText block object.

        Raises:
            DataIsMissingError: If the `text` key is not present in the `data` dictionary.
        """
        if "text" not in data:
            msg = "`**data` dictionary must contain the `text` key."
            raise DataIsMissingError(msg)
        return cls(PlainTextData(text=data["text"]), name=name, formatter=formatter, renderer=renderer)
