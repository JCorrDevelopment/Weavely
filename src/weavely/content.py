from __future__ import annotations

from collections.abc import Iterable, Sized
from typing import TYPE_CHECKING

from weavely.blocks.base import BaseBlock, Data
from weavely.blocks.txt import PlainText, Title

if TYPE_CHECKING:
    from collections.abc import Iterator

    from weavely.formatters.base import IBlockFormatter
    from weavely.renderers.base import IBlockRenderer


class Content(Sized, Iterable[BaseBlock[Data]]):
    """
    A class to represent a file content.

    Responsible for storing, adding, removing and other operations with the file blocks.
    By itself this class does not render the file content, as well as know nothing about blocks formatting, which
    is delegated to `File` object.

    Blocks are stored inside the contend as a dictionary, where the key is the block name, and the values is
    the block object itself. This allows for simple block reference, as well as guarantees block insertion order.
    """

    def __init__(self) -> None:
        self._blocks: dict[str, BaseBlock[Data]] = {}

    def __iter__(self) -> Iterator[BaseBlock[Data]]:
        """
        Iterate over the blocks in the content in insertion order.

        Returns:
            Iterator[BaseBlock[Data]]: Block object.
        """
        return iter(self._blocks.values())

    def __len__(self) -> int:
        """
        Get the number of blocks in the content.

        Returns:
            int: Number of blocks in the content.
        """
        return len(self._blocks)

    def add_block(self, block: BaseBlock[Data]) -> str:
        """
        Add a new block to the content.

        Args:
            block (BaseBlock[Data]): Block object to add.

        Returns:
            str: Name of the block.
        """
        self._blocks[block.name] = block
        return block.name

    def add_plain_text(
        self,
        text: str,
        *,
        name: str | None = None,
        formatter: IBlockFormatter | None = None,
        renderer: IBlockRenderer | None = None,
    ) -> str:
        """
        Add a new plain text block to the content.

        Args:
            text (str): Plain text that should be added to the content as a PlainText block.
            name (str | None): Name of the block. If not specified, it will be generated automatically.
            formatter (IBlockFormatter | None): Specific formatter to use for this block.
            renderer (IBlockRenderer | None): Specific renderer to use for this block.

        Returns:
            str: Name of the block.
        """
        block = PlainText.by_data(name=name, formatter=formatter, renderer=renderer, text=text)
        return self.add_block(block)

    def add_title(
        self,
        title: str,
        level: int = 1,
        *,
        name: str | None = None,
        formatter: IBlockFormatter | None = None,
        renderer: IBlockRenderer | None = None,
    ) -> str:
        """
        Add a new title block to the content.

        Args:
            title (str): Title text.
            level (int): Title level. Default is 1.
            name (str | None): Name of the block. If not specified, it will be generated automatically.
            formatter (IBlockFormatter | None): Specific formatter to use for this block.
            renderer (IBlockRenderer | None): Specific renderer to use for this block.

        Returns:
            str: Name of the block.
        """
        block = Title.by_data(title=title, level=level, name=name, formatter=formatter, renderer=renderer)
        return self.add_block(block)
