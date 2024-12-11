from __future__ import annotations

from pathlib import Path
from typing import IO, TYPE_CHECKING

from simple_text_renderer.file.mixins import WithPlainTextMixin

if TYPE_CHECKING:
    from collections.abc import Iterator

    from simple_text_renderer.blocks.base import BaseBlock, Data
    from simple_text_renderer.renderers.base import BaseRenderer


class BaseFile:
    """
    General representation of a file as an idea.

    Responsible for adding, modifying and removing data blocks from the file. As well, it orchestrates the document
    rendering process.

    Blocks are stored inside the file object as a dictionary where the key is the block name and the value is the
    block object itself. This allows to simple block reference, as well as it guarantees block insertion order.

    Parameters:
        renderer (BaseRenderer): Renderer object to render the file.
        encoding (str): Encoding of the file content. Default is UTF-8.
    """

    def __init__(self, renderer: BaseRenderer, *, encoding: str = "utf-8") -> None:
        self._blocks: dict[str, BaseBlock[Data]] = {}
        self._renderer = renderer
        self._encoding = encoding

    @property
    def encoding(self) -> str:
        """
        Get the encoding of the file content.

        Returns:
            str: Encoding of the file content.
        """
        return self._encoding

    def add_block(self, block: BaseBlock[Data]) -> str:
        """
        Add a new block to current file.

        Args:
            block: New block instance to add.

        Returns:
            str: Name of the block in the file.
        """
        self._blocks[block.name] = block
        return block.name

    def __iter__(self) -> Iterator[BaseBlock[Data]]:
        """
        Iterate over all blocks in the file and return them in insertion order.

        Returns:
            Iterator[BaseBlock]: Iterator over all blocks in the file.
        """
        return iter(self._blocks.values())

    def format(self) -> None:
        """Format all blocks in the file according to their formatters."""
        for block in self._blocks.values():
            block.format()

    def as_str(self) -> str:
        """
        Render the file as a string.

        Returns:
            str: Rendered file content.
        """
        self.format()
        return self._renderer.as_str(self)

    def as_stream(self) -> IO[bytes]:
        """
        Render the file as a stream.

        Returns:
            IO: Rendered file content.
        """
        self.format()
        return self._renderer.as_stream(self)

    def to_file(self, file_path: str) -> None:
        """
        Save the file to the provided path.

        Args:
            file_path: Path to save the file.
        """
        self.format()
        with Path(file_path).open("wb") as file, self.as_stream() as stream:
            file.write(stream.read())


class SimpleFile(
    BaseFile,
    WithPlainTextMixin,
):
    """
    Simple file representation.

    Contains some interfaces for file manipulation with known block types.
    """
