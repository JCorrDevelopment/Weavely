import dataclasses
from typing import Self, TypedDict, Unpack

from weavely.blocks import BaseBlock, Data
from weavely.errors import DataIsMissingError
from weavely.formatters.base import IBlockFormatter
from weavely.renderers.base import IBlockRenderer


@dataclasses.dataclass(slots=True)
class Paragraph(Data):
    """
    Data class for containing paragraph data.

    Attributes:
        text (str): Paragraph text.
    """

    text: str


class ParagraphKwargs(TypedDict):
    """Type hint for the ParagraphBlock `to_data` method keyword arguments."""

    text: str


class ParagraphBlock(BaseBlock[Paragraph]):
    """Represents a paragraph block in the content."""

    @classmethod
    def by_data(  # type: ignore[override]  # Overriding a parent class kwarg type hint to improve code completion.
        cls,
        *,
        name: str | None = None,
        formatter: IBlockFormatter | None = None,
        renderer: IBlockRenderer | None = None,
        **data: Unpack[ParagraphKwargs],
    ) -> Self:
        """
        Create a new paragraph block object.

        Args:
            name (str | None): Optional name of the block. Used to reference the block in the file. If None, the block
                will generate it based on the class name and some randomized suffix.
            formatter (IBlockFormatter): Formatter object to format the data object. If None, the block will
                use the default formatter provided by the file formatter implementation.
            renderer (IBlockRenderer | None): Renderer object to render the block into a specific format.
                If None, the block will use the default renderer provided by the file renderer implementation.
            data (ParagraphKwargs): Arbitrary range of keyword arguments to initialize the data object.
                Must be specified by the specific block class.

        Returns:
            ParagraphBlock: New block instance.

        Raises:
            DataIsMissingError: If information provided in `**data` is not enough to create data object.
        """
        if "text" not in data:
            raise DataIsMissingError(data_type=Paragraph, field="text")

        return cls(Paragraph(**data), name=name, formatter=formatter, renderer=renderer)
