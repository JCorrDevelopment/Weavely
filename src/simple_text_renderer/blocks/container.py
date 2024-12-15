from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any, Self

from .base import BaseBlock, Data, TBaseBlock

if TYPE_CHECKING:
    from collections.abc import Sequence

    from simple_text_renderer.formatters.base import FormatterProtocol


@dataclasses.dataclass(slots=True)
class ContainerData(Data):
    """
    Default data class for a container block.

    Contains a list of blocks of container block in the order they should be rendered. In fact, it may contain
    any arbitrary blocks, including other container blocks.

    Useful for creating a blocks' hierarchy.
    """

    blocks: dict[str, BaseBlock[Data]] = dataclasses.field(default_factory=dict[str, BaseBlock[Data]])
    """
    Dictionary representing blocks in the container.

    Key is the name of the block, when value is the block itself.
    """


class Container(BaseBlock[ContainerData]):
    """Block that contains a group of other blocks."""

    @classmethod
    def by_content(
        cls,
        *,
        name: str | None = None,
        formatters: Sequence[FormatterProtocol[ContainerData]] = (),
        blocks: Sequence[TBaseBlock] = (),
        **kwargs: Any,  # noqa: ANN401, ARG003
    ) -> Self:
        """
        Create a container block by provided blocks.

        Args:
            name (str): name of the block. Used to reference the block in the file. If None, the block
                will generate it based on the class name and some randomized suffix.
            formatters (Sequence[FormatterProtocol[ContainerData]]): Collection of formatters that can be applied to the
                data object.
            blocks (Sequence[TBaseBlock]): Blocks to add to the container.
            kwargs: Not required. Specified for the seek of good code practices.

        Returns:
            Container: Created container block.
        """
        blocks_map = {block.name: block for block in blocks}
        return cls(ContainerData(blocks=blocks_map), name=name, formatters=formatters)

    def add_block(self, block: BaseBlock[Data]) -> str:
        """
        Add a new block to the container.

        Args:
            block: New block instance to add.

        Returns:
            str: Name of the block in the container.
        """
        self._data.blocks[block.name] = block
        return block.name

    def remove_block(self, block_name: str) -> None:
        """
        Remove a block from the container by its name.

        Args:
            block_name: Name of the block to remove.

        Raises:
            KeyError: If the block with the provided name is not found.
        """
        if block_name not in self._data.blocks:
            msg = f"Block with name '{block_name}' not found in the container."
            raise KeyError(msg)
        del self._data.blocks[block_name]
