from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simple_text_renderer.blocks.base import BaseBlock, Data


class Content:
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
