from __future__ import annotations

import io
from functools import singledispatchmethod
from io import StringIO
from pathlib import Path
from typing import IO, TYPE_CHECKING, cast, overload

from simple_text_renderer.blocks.text import PlainTextBlock

from .base import BaseRenderer

if TYPE_CHECKING:
    from simple_text_renderer.blocks.base import TBaseBlock
    from simple_text_renderer.file import BaseFile


class TxtRenderer(BaseRenderer):
    """
    Default renderer for the TXT file format.

    This renderer is used to render the data object into a string or a stream of bytes, which can be written
    as a plain .txt file.
    """

    def __init__(self, *, delimiter: str = "\n") -> None:
        self._delimiter = delimiter

    def as_str(self, file: BaseFile) -> str:
        """
        Convert the provided file object into a string descring all the data.

        Parameters:
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

        Parameters:
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

        Parameters:
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

        Parameters:
            stream (io.IOBase): a stream to write the message to. May be any IOBase subclass.
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

        Parameters:
            file (BaseFile): File object to render.
            path (Path | str): Path to save the rendered file.
        """
        if isinstance(path, str):
            path = Path(path)
        with path.open("wb") as f:
            f.write(self.as_stream(file).read())

    def _render_block(self, block: TBaseBlock) -> str:
        match block:
            case PlainTextBlock():
                return block.data.text
            case _:
                msg = f"Unsupported block type: {block.__class__.__name__}"
                raise TypeError(msg)
