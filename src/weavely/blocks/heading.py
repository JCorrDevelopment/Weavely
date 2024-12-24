import dataclasses
from typing import NotRequired, Self, TypedDict, Unpack

from weavely.blocks import BaseBlock, Data
from weavely.errors import DataIsInvalidError, DataIsMissingError
from weavely.formatters.base import IBlockFormatter
from weavely.renderers.base import IBlockRenderer


@dataclasses.dataclass(slots=True)
class Heading(Data):
    """
    Data object representing a heading block.

    Contains the following attributes:
        text (str): Text of the heading.
        level (int): Level of the heading. Default is 1.
    """

    text: str
    """
    Text of the heading.
    """
    level: int = dataclasses.field(default=1)
    """
    Level of the heading.

    Controls the importance of the heading. Lower level means higher priority. Default is 1.
    """

    def __post_init__(self) -> None:
        """
        Validate the provided heading information.

        Ensures in the following:
            - The text is not empty.
            - The level is a positive integer.

        Raises:
            DataIsMissingError: If the text is empty.
            DataIsInvalidError: If the level is not a positive integer.
        """
        if not self.text:
            raise DataIsMissingError(data_type=self.__class__, field="text")
        if self.level < 1:
            raise DataIsInvalidError(data_type=self.__class__, field="level", reason="must be a positive integer")


class HeadingKwargs(TypedDict):
    """Type hint for the HeadingBlock `to_data` method keyword arguments."""

    text: str
    level: NotRequired[int]


class HeadingBlock(BaseBlock[Heading]):
    """Represents a heading block in the content."""

    @classmethod
    def by_data(  # type: ignore[override]  # Overriding a parent class kwarg type hint to improve code completion.
        cls,
        *,
        name: str | None = None,
        formatter: IBlockFormatter | None = None,
        renderer: IBlockRenderer | None = None,
        **data: Unpack[HeadingKwargs],
    ) -> Self:
        """
        Create a new block instance by providing the data object.

        Args:
            name (str | None): Optional name of the block. Used to reference the block in the file. If None, the block
                will generate it based on the class name and some randomized suffix.
            formatter (IBlockFormatter): Formatter object to format the data object. If None, the block will
                use the default formatter provided by the file formatter implementation.
            renderer (IBlockRenderer | None): Renderer object to render the block into a specific format.
                If None, the block will use the default renderer provided by the file renderer implementation.
            data (HeadingKwargs): Arbitrary range of keyword arguments to initialize the data object.

        Returns:
            HeadingBlock: New block instance.

        Raises:
            DataIsMissingError: If information provided in `**data` is not enough to create data object.
        """
        if "text" not in data:
            raise DataIsMissingError(data_type=Heading, field="text")

        return cls(Heading(**data), name=name, formatter=formatter, renderer=renderer)
