from __future__ import annotations

import abc
from typing import IO, TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from simple_text_renderer.file import BaseFile


class BaseRenderer(abc.ABC):
    """
    Base class to describe a renderer.

    Idea of the renderer is to have an object which know how to render arbitrary data object into a specified format.
    It shouldn't know anything about the data itself, as well as it shouldn't be responsible for the formatting outside
    required for the rendering itself.
    """

    @abc.abstractmethod
    def as_str(self, file: BaseFile) -> str:
        """
        Render the file in a correct format into a string.

        Parameters:
            file: File object to render.

        Returns:
            str: String representation of the rendered file content.
        """

    @abc.abstractmethod
    def as_stream(self, file: BaseFile) -> IO[bytes]:
        """
        Render the file in a correct format into a stream.

        Parameters:
            file: File object to render.
        """

    @abc.abstractmethod
    def to_file(self, file: BaseFile, path: Path | str) -> None:
        """
        Render the file in a correct format and write it to the specified path.

        Parameters:
            file: File object to render.
            path: Path to write the file.
        """
