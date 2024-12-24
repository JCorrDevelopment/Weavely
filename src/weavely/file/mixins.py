from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from weavely.blocks.heading import HeadingBlock, HeadingKwargs
from weavely.blocks.paragraph import ParagraphBlock

if TYPE_CHECKING:
    from weavely.blocks import BaseBlock, Data
    from weavely.formatters.base import IBlockFormatter
    from weavely.renderers.base import IBlockRenderer


class WithAddBlockProtocol(Protocol):
    """Protocol for mixins that can provide traits to add a new block to the file content."""

    def add_block(self, block: BaseBlock[Data]) -> str:
        """
        Add a new block to the file content.

        Args:
            block (BaseBlock[Data]): Block object to add.

        Returns:
            str: Name of the added block.
        """
        ...


class WithHeading(WithAddBlockProtocol):
    """Provide ability to add a new heading block to the file content."""

    def add_heading(
        self,
        title: str,
        level: int | None = None,
        *,
        formatter: IBlockFormatter | None = None,
        renderer: IBlockRenderer | None = None,
        name: str | None = None,
    ) -> str:
        """
        Add a new heading block to the content.

        Args:
            title (str): Title of the heading.
            level (int | None): Level of the heading. Default is `None`.
            formatter (IBlockFormatter | None): Custom formatter object to format the data object. If None, the block
                will use the default formatter provided by the file formatter implementation.
            renderer (IBlockRenderer | None): Custom renderer object to render the block into a specific format.
                If None, the block will use the default renderer provided by the file renderer implementation.
            name (str | None): Optional name of the block. Used to reference the block in the file. If None, the block
                will generate it based on the class name and some randomized suffix

        Returns:
            str: Name of the block.
        """
        data = HeadingKwargs(text=title) if level is None else HeadingKwargs(text=title, level=level)

        heading = HeadingBlock.by_data(
            name=name,
            formatter=formatter,
            renderer=renderer,
            **data,
        )

        return self.add_block(heading)


class WithParagraph(WithAddBlockProtocol):
    """Provide ability to add a new paragraph block to the file content."""

    def add_paragraph(
        self,
        text: str,
        *,
        formatter: IBlockFormatter | None = None,
        renderer: IBlockRenderer | None = None,
        name: str | None = None,
    ) -> str:
        """
        Add a new paragraph block to the content.

        Args:
            text (str): Text of the paragraph.
            formatter (IBlockFormatter | None): Custom formatter object to format the data object. If None, the block
                will use the default formatter provided by the file formatter implementation.
            renderer (IBlockRenderer | None): Custom renderer object to render the block into a specific format.
                If None, the block will use the default renderer provided by the file renderer implementation.
            name (str | None): Optional name of the block. Used to reference the block in the file. If None, the block
                will generate it based on the class name and some randomized suffix.

        Returns:
            str: Name of the block.
        """
        paragraph = ParagraphBlock.by_data(
            name=name,
            formatter=formatter,
            renderer=renderer,
            text=text,
        )

        return self.add_block(paragraph)
