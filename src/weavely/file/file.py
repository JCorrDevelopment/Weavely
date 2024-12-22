from __future__ import annotations

from io import BytesIO, IOBase, StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, NoReturn, cast, overload

from weavely.content import Content
from weavely.errors import RendererIsUnknownError
from weavely.formatters.base import FileFormatter, IBlockFormatter
from weavely.renderers.base import FileRenderer, IBlockRenderer

if TYPE_CHECKING:
    from weavely.blocks import Data


class SimpleFile:
    """
    General representation of a file as an idea.

    Responsible for adding, modifying and removing data blocks from the file. As well, it orchestrates the document
    rendering process.

    Blocks are stored inside the file object as a dictionary where the key is the block name and the value is the
    block object itself. This allows to simple block reference, as well as it guarantees block insertion order.
    """

    def __init__(
        self,
        formatter: FileFormatter | None = None,
        renderer: FileRenderer | None = None,
        *,
        encoding: str = "utf-8",
        delimiter: str = "\n",
    ) -> None:
        """
        Args:
            formatter (FileFormatter): Formatter object to format the file.
            renderer (FileRenderer): Renderer object to render the file.
            encoding (str): Encoding of the file content. Default is UTF-8.
            delimiter (str): Delimiter to separate blocks in the file content. Default is newline.
        """  # noqa: D205
        self._content = Content()
        self._formatter = formatter or FileFormatter()
        self._renderer = renderer or FileRenderer()
        self._encoding = encoding
        self._delimiter = delimiter

    def set_renderer(self, data_type: type[Data], renderer: IBlockRenderer, *, replace: bool = False) -> None:
        """
        Set the default renderer for the specified data type.

        Args:
            data_type (type[Data]): Data type to set the renderer for.
            renderer (IBlockRenderer[Data]): Renderer object to set.
            replace (bool): Flag to replace the existing renderer if it is already set. Default is False.

        Raises:
            KeyError: If the renderer is already set and the `replace` flag is not set.
        """
        if data_type in self._renderer and not replace:
            msg = (
                f"Renderer for data type {data_type.__name__!r} is already set. Use `replace=True` if you want "
                f"to replace it intentionally."
            )
            raise KeyError(msg)
        self._renderer[data_type] = renderer

    def set_formatter(self, data_type: type[Data], formatter: IBlockFormatter, *, replace: bool = False) -> None:
        """
        Set the default formatter for the specified data type.

        Args:
            data_type (type[Data]): Data type to set the formatter for.
            formatter (IBlockFormatter): Formatter object to set.
            replace (bool): Flag to replace the existing formatter if it is already set. Default is False.

        Raises:
            KeyError: If the formatter is already set and the `replace` flag is not set.
        """
        if data_type in self._formatter and not replace:
            msg = (
                f"Formatter for data type {data_type.__name__!r} is already set. Use `replace=True` if you want "
                f"to replace it intentionally."
            )
            raise KeyError(msg)
        self._formatter[data_type] = formatter

    def get_renderer(self, data_type: type[Data]) -> IBlockRenderer | None:
        """
        Return the renderer object for the specified data type.

        Args:
            data_type (type[Data]): Data type to get the renderer for.

        Returns:
            IBlockRenderer | None: Renderer object for the specified data type.
                If the renderer is not set, returns None.
        """
        return self._renderer.get(data_type, None)

    def get_formatter(self, data_type: type[Data]) -> IBlockFormatter | None:
        """
        Return the formatter object for the specified data type.

        Args:
            data_type (type[Data]): Data type to get the formatter for.

        Returns:
            IBlockFormatter | None: Formatter object for the specified data type.
                If the formatter is not set, returns None.
        """
        return self._formatter.get(data_type, None)

    def remove_renderer(self, data_type: type[Data]) -> IBlockRenderer | None:
        """
        Remove the default renderer for the specified data type.

        Args:
            data_type (type[Data]): Data type to remove the renderer for.

        Returns:
            IBlockRenderer | None: Removed renderer object.
        """
        return self._renderer.pop(data_type, None)

    def remove_formatter(self, data_type: type[Data]) -> IBlockFormatter | None:
        """
        Remove the default formatter for the specified data type.

        Args:
            data_type (type[Data]): Data type to remove the formatter for.

        Returns:
            IBlockFormatter | None: Removed formatter object.
        """
        return self._formatter.pop(data_type, None)

    @property
    def encoding(self) -> str:
        """
        Get the encoding of the file content.

        Returns:
            str: Encoding of the file content.
        """
        return self._encoding

    @property
    def content(self) -> Content:
        """
        Get the content of the file.

        Returns:
            Content: File content object.
        """
        return self._content

    def as_str(self) -> str:
        """
        Render the file content into a string representation.

        Returns:
            str: String representation of the file content.
        """
        return self._as_stream(StringIO()).getvalue()

    def as_stream(self) -> BytesIO:
        """
        Render document content into a bytes stream.

        Returns:
            BytesIO: Bytes stream with the file content.
        """
        return self._as_stream(BytesIO())

    @overload
    def _as_stream(self, stream: StringIO) -> StringIO: ...

    @overload
    def _as_stream(self, stream: BytesIO) -> BytesIO: ...

    @overload
    def _as_stream(self, stream: Any) -> NoReturn: ...  # noqa: ANN401

    def _as_stream(self, stream: Any) -> StringIO | BytesIO:
        """
        Populate provided stream with the rendered file content.

        Args:
            stream (IOBase): Stream to write the rendered file content.

        Returns:
            IOBase: Stream with the rendered file content written.

        Raises:
            NotImplementedError: If the stream type is not supported.
            TypeError: If the stream is not of type IOBase.

        """  # noqa: DOC502
        match stream:
            case StringIO() | BytesIO():
                for i, block in enumerate(self._content, start=1):
                    data = self._format(block.data, block.formatter)
                    rendered = self._render(data, block.renderer)
                    self._write_to_stream(stream, rendered, write_delimiter=i < len(self._content))
            case IOBase():
                self._raise_not_supported_stream_type(stream, "_as_stream")
            case _:
                self._raise_not_a_stream(stream)

        return stream

    @overload
    def _write_to_stream(self, stream: StringIO, rendered: str, *, write_delimiter: bool = True) -> StringIO: ...

    @overload
    def _write_to_stream(self, stream: BytesIO, rendered: str, *, write_delimiter: bool = True) -> BytesIO: ...

    @overload
    def _write_to_stream(self, stream: Any, rendered: str, *, write_delimiter: bool = True) -> NoReturn: ...  # noqa: ANN401

    def _write_to_stream(self, stream: Any, rendered: str, *, write_delimiter: bool = True) -> StringIO | BytesIO:
        """
        Write the rendered block content to the provided stream.

        Args:
            stream (IOBase): Stream to write the rendered block content.
            rendered (str): Rendered block content.
            write_delimiter (bool): Flag to write the delimiter after the block content. Default is True.

        Returns:
            IOBase: Stream with the rendered block content written.

        Raises:
            NotImplementedError: If the stream type is not supported.
            TypeError: If the stream is not of type IOBase.
        """  # noqa: DOC502
        match stream:
            case StringIO():
                stream.write(rendered)
                if write_delimiter:
                    stream.write(self._delimiter)
            case BytesIO():
                stream.write(rendered.encode(self._encoding))
                if write_delimiter:
                    stream.write(self._delimiter.encode(self._encoding))
            case IOBase():
                self._raise_not_supported_stream_type(stream, "_write_to_stream")
            case _:
                self._raise_not_a_stream(stream)

        return cast("StringIO | BytesIO", stream)

    def _raise_not_supported_stream_type(self, stream: IOBase, method: str) -> NoReturn:
        supported_types: tuple[type[IOBase], ...] = (StringIO, BytesIO)
        msg = (
            f"Unsupported stream type {type(stream).__name__!r}. Contact the library maintainers to add official "
            f"support for the stream type. If you need this for you project, "
            f"consider inheriting the SimpleFile class and implementing {method!r} method.\n"
            f"Supported stream types: {", ".join(f"{item.__name__}" for item in supported_types)}"
        )
        raise NotImplementedError(msg)

    def _raise_not_a_stream(self, value: Any) -> NoReturn:  # noqa: ANN401
        msg = f"The `stream` expected to be of type {IOBase.__name__}, got type {type(value).__name__}."
        raise TypeError(msg)

    def to_file(self, path: Path | str) -> Path:
        """
        Write document content to a provided file by the path.

        Returns:
            Path: Path to the file with the rendered content.
        """
        if isinstance(path, str):
            path = Path(path)

        with path.open("wb") as file:
            file.write(self.as_stream().read())
            file.seek(0)

        return path

    def _format(self, data: Data, formatter: IBlockFormatter | None) -> Data:
        """
        Format the block data according to the formatter rules.

        Args:
            data (Data): Block object to format.
            formatter (IBlockFormatter | None): Formatter object to format the block

        Returns:
            Data: Block object with formatted data.
        """
        if formatter:
            return formatter(data)

        if default_formatter := self._formatter.get(type(data)):
            return default_formatter(data)

        return data

    def _render(self, data: Data, renderer: IBlockRenderer | None) -> str:
        """
        Render the block content into a string representation.

        Args:
            data (Data): Block data object to render.
            renderer (IBlockRenderer[Data] | None): Renderer object to render the block into a specific format

        Returns:
            str: String representation of the block content.

        Raises:
            RendererIsUnknownError: If the block data cannot be rendered.
        """
        if renderer:
            return renderer(data)
        if default_renderer := self.get_renderer(type(data)):
            return default_renderer(data)
        msg = (
            f"Data {data!r} cannot be rendered. {self.__class__.__name__!r} not block does "
            f"not have a renderer for specified data type."
        )
        raise RendererIsUnknownError(msg)
