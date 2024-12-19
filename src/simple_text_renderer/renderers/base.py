from __future__ import annotations

import dataclasses

from simple_text_renderer.blocks.base import BaseBlock, TData
from simple_text_renderer.renderers.mixins import IBlockRenderer


@dataclasses.dataclass(slots=True)
class FileRenderer:
    """
    Base class for a collection of default renderers used by the `File` object.

    When any block is rendered, it uses the following order to select the renderer:
        1. If the block has a specific renderer, it will be used.
        2. Otherwise, the default renderer will be used.
        3. If no renderer is found, raises RendererIsUnknownError exception.
    """

    renderers: dict[type[BaseBlock[TData]], IBlockRenderer] = dataclasses.field(
        default_factory=dict[type[BaseBlock[TData]], IBlockRenderer],
    )
    """
    Dictionary of default block renderers used by the `File` object.

    Key is a block data type, value is a block renderer object.
    Block renderer object must implement the `IBlockRenderer` protocol. So it may be a callable class inheriting from
    the `BlockRendererBase` class, or any function that repeat IBlockRenderer protocol.
    """
