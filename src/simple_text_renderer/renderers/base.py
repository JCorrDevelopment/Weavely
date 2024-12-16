from __future__ import annotations

import abc
from typing import IO, TYPE_CHECKING, ClassVar

from std_utils.more_typing.undefined import UNDEFINED, is_undefined

from simple_text_renderer.blocks.base import BaseBlock, Data
from simple_text_renderer.renderers.mixins import RendererProtocol

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from simple_text_renderer.file import BaseFile


class FileRendererBase(abc.ABC):
    """
    Base class to describe a renderer.

    Idea of the renderer is to have an object which know how to render arbitrary data object into a specified format.
    It shouldn't know anything about the data itself, as well as it shouldn't be responsible for the formatting outside
    required for the rendering itself.
    """

    _DEFAULT_RENDERERS: ClassVar[dict[type[BaseBlock[Data]], RendererProtocol[Data]]] = UNDEFINED

    @classmethod
    def register(cls, renderer: RendererProtocol[Data], block_type: type[BaseBlock[Data]]) -> RendererProtocol[Data]:
        """
        Register a renderer for the specified block type.

        Can be used as a decorator, as well as a regular function call.

        Args:
            block_type (type[BaseBlock[Data]]): Block type to register the renderer for.
            renderer (RendererProtocol[Data]): Renderer to register.

        Returns:
            RendererProtocol[Data]: Provided renderer.

        Raises:
            ValueError: If the renderer for the specified block type is already registered.
        """
        if is_undefined(cls._DEFAULT_RENDERERS):
            cls._DEFAULT_RENDERERS = dict[type[BaseBlock[Data]], RendererProtocol[Data]]()

        if block_type in cls._DEFAULT_RENDERERS:
            msg = f"Renderer for {block_type.__name__} is already registered."
            raise ValueError(msg)

        cls._DEFAULT_RENDERERS[block_type] = renderer
        return renderer

    def __init__(self, *, renderers: Mapping[type[BaseBlock[Data]], RendererProtocol[Data]] | None = None) -> None:
        """
        Initialize FileRenderer object.

        Args:
            renderers (Mapping[type[BaseBlock[Data]], RendererProtocol[Data]] | None): Mapping of renderers to use for
                specific block types. Used to override the default renderers.
        """
        self._renderers = self._init_renderers(renderers or {})

    def _init_renderers(
        self, renderers: Mapping[type[BaseBlock[Data]], RendererProtocol[Data]]
    ) -> dict[type[BaseBlock[Data]], RendererProtocol[Data]]:
        """
        Initialize the renderers mapping.

        Combine the default renderers specified as `_DEFAULT_RENDERERS` with the provided renderers. Items provided
        by `__init__` method will override the default renderers.

        Args:
            renderers (Mapping[type[BaseBlock[Data]], RendererProtocol[Data]]): Provided renderers mapping.

        Returns:
            dict[type[BaseBlock[Data]], RendererProtocol[Data]]: Initialized renderers mapping.

        @public
        """
        if is_undefined(self._DEFAULT_RENDERERS):
            return dict(renderers)

        result = self._DEFAULT_RENDERERS.copy()
        result.update(renderers)
        return result

    @abc.abstractmethod
    def as_str(self, file: BaseFile) -> str:
        """
        Render the file in a correct format into a string.

        Args:
            file: File object to render.

        Returns:
            str: String representation of the rendered file content.
        """

    @abc.abstractmethod
    def as_stream(self, file: BaseFile) -> IO[bytes]:
        """
        Render the file in a correct format into a stream.

        Args:
            file: File object to render.
        """

    @abc.abstractmethod
    def to_file(self, file: BaseFile, path: Path | str) -> None:
        """
        Render the file in a correct format and write it to the specified path.

        Args:
            file: File object to render.
            path: Path to write the file.
        """

    def _render_block(self, block: BaseBlock[Data]) -> str:
        """
        Render the block data into a string representation.

        Args:
            block (BaseBlock[Data]): Block to render.

        Returns:
            str: Rendered block content.

        Raises:
            ValueError: If the block does not have a renderer and no default renderer is provided.

        @public
        """
        if block.renderer:
            return block.renderer(block)

        if renderer := self._renderers.get(type(block)):
            return renderer(block)
        msg = (
            f"This instance of {self.__class__.__name__} does not have a renderer for {type(block).__name__} blocks."
            "Please, register it as a default renderer for this block type, provide a renderer during initialization "
            "or specify specific renderer for the block."
        )
        raise ValueError(msg)
