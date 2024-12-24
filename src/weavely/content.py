from __future__ import annotations

from collections.abc import Iterable, Sized
from typing import TYPE_CHECKING

from weavely.blocks.base import BaseBlock, Data

if TYPE_CHECKING:
    from collections.abc import Iterator


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
