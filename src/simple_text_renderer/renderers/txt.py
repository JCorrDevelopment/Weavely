from __future__ import annotations

import io
from functools import singledispatchmethod
from io import StringIO
from pathlib import Path
from typing import IO, TYPE_CHECKING, cast, overload

from .base import FileRendererBase

if TYPE_CHECKING:
    from collections.abc import Mapping

    from simple_text_renderer.blocks.base import BaseBlock, Data
    from simple_text_renderer.file import BaseFile

    from .mixins import RendererProtocol


class TxtFileRenderer(FileRendererBase):
    """
    Default renderer for the TXT file format.

    This renderer is used to render the data object into a string or a stream of bytes, which can be written
    as a plain .txt file.

    Args:
        delimiter (str): Delimiter to use between blocks. Default is newline.
    """

    def __init__(
        self, *, renderers: Mapping[type[BaseBlock[Data]], RendererProtocol[Data]] | None = None, delimiter: str = "\n"
    ) -> None:
        """
        Initialize TxtFileRenderer object.

        Args:
            renderers (Mapping[type[BaseBlock[Data]], RendererProtocol[Data]] | None): Mapping of renderers to use for
            specific block types. Used to override the default renderers.
            delimiter (str): Delimiter to use between blocks. Default is newline
        """
        super().__init__(renderers=renderers)
        self._delimiter = delimiter

    def as_str(self, file: BaseFile) -> str:
        """
        Convert the provided file object into a string describing all the data.

        Args:
            file (BaseFile): File object to render.

        Returns:
            str: Rendered string.
        """
        string_io = StringIO()
        for block in file:
            string_io.write(self._render_block(block))
            string_io.write("\n")
        stream = cast("StringIO", self._as_stream(file, StringIO()))
        return stream.getvalue()

    def as_stream(self, file: BaseFile) -> IO[bytes]:
        """
        Convert the provided file object into a stream.

        Args:
            file (BaseFile): File object to render.

        Returns:
            IO[bytes]: Stream object containing the rendered data.
        """
        return self._as_stream(file, io.BytesIO())

    @overload
    def _as_stream(self, file: BaseFile, stream: IO[str]) -> IO[str]: ...

    @overload
    def _as_stream(self, file: BaseFile, stream: IO[bytes]) -> IO[bytes]: ...

    def _as_stream(self, file: BaseFile, stream: IO[str] | IO[bytes]) -> IO[str] | IO[bytes]:
        """
        Convert provided file object into an arbitrary stream.

        Args:
            file (BaseFile): file object to render.
            stream (IO[T]): the stream to write the rendered data to.

        Returns:
            IO[T]: stream object containing the rendered data.

        """
        for block in file:
            self._write_message(stream, self._render_block(block), file.encoding)
            self._write_message(stream, self._delimiter, file.encoding)
        stream.seek(0)
        return stream

    @singledispatchmethod
    def _write_message(self, stream: IO[str] | IO[bytes], message: str, encoding: str = "utf-8") -> None:
        """
        Write the message to the stream.

        Args:
            stream (io.IOBase): a stream to write the message to. It may be any IOBase subclass.
            message (str): the message to write.
            encoding (str): the encoding to use when writing the message. Defaults to "utf-8".

        Raises:
            TypeError: if the stream type is not supported.

        """
        if isinstance(stream, io.TextIOBase):
            to_write = message
        elif isinstance(stream, io.BufferedIOBase):
            to_write = message.encode(encoding)
        else:
            msg = f"Unsupported stream type: {type(stream).__name__}"
            raise TypeError(msg)

        stream.write(to_write)

    def to_file(self, file: BaseFile, path: Path | str) -> None:
        """
        Save the rendered file to the specified path.

        Args:
            file (BaseFile): File object to render.
            path (Path | str): Path to save the rendered file.
        """
        if isinstance(path, str):
            path = Path(path)
        with path.open("wb") as f:
            f.write(self.as_stream(file).read())
