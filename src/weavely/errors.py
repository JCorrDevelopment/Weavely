from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from io import IOBase

    from weavely.blocks import Data


class WeavelyError(Exception, abc.ABC):
    """Base class for all exceptions raised by Weavely."""


class UnsupportedStreamTypeError(WeavelyError, NotImplementedError):
    """Raised in case a stream type is not supported by the Weavely."""

    def __init__(self, *args: Any, stream_type: type[IOBase], method: str) -> None:  # noqa: ANN401
        super().__init__(*args)
        self.stream_type = stream_type
        self.method = method


class WrongDataTypeError(WeavelyError, TypeError):
    """Raised in case a wrong data type provided to a Renderer or Formatter."""

    def __init__(self, *args: Any, data_type: type[Data], expected_data_types: tuple[type[Data], ...]) -> None:  # noqa: ANN401
        super().__init__(*args)
        self.data_type = data_type
        self.expected_data_types = expected_data_types


class CannotReplaceRendererError(WeavelyError, KeyError):
    """Raised in case a renderer cannot be replaced."""


class CannotReplaceFormatterError(WeavelyError, KeyError):
    """Raised in case a formatter cannot be replaced."""


class CannotDeleteFormatterError(WeavelyError, KeyError):
    """Raised in case a formatter cannot be deleted."""


class CannotDeleteRendererError(WeavelyError, KeyError):
    """Raised in case a renderer cannot be deleted."""


class RendererIsNotRegisteredError(WeavelyError, KeyError):
    """Raised in case a renderer is not registered in the renderer collection."""


class FormatterIsNotRegisteredError(WeavelyError, KeyError):
    """Raised in case a formatter is not registered in the formatter collection."""


class NotAStreamError(WeavelyError, TypeError):
    """Raised in case a provided object is not a stream."""


class RendererIsUnknownError(WeavelyError, TypeError):
    """Raised in case any renderer is not found for a provided block item."""


class DataIsMissingError(WeavelyError, ValueError):
    """Raised in case user do not specify enough information to create a data object for a block."""

    def __init__(self, *args: Any, data_type: type[Data], field: str, message: str | None = None) -> None:  # noqa: ANN401
        if not message:
            message = f"Field {field!r} is required for the data object {data_type!r}."
        super().__init__(message, *args)
        self.field = field
        self.data_type = data_type


class DataIsInvalidError(WeavelyError, ValueError):
    """Raised in case user provide invalid information to create a data object for a block."""

    def __init__(self, *args: Any, data_type: type[Data], field: str, reason: str, message: str | None = None) -> None:  # noqa: ANN401
        if not message:
            message = f"Field {field!r} is invalid for the data object {data_type!r}. Reason: {reason!r}"
        super().__init__(message, *args)
        self.field = field
        self.data_type = data_type
        self.reason = reason
