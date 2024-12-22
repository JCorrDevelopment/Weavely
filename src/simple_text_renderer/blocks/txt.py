from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any, Self

from simple_text_renderer.blocks import BaseBlock, Data
from simple_text_renderer.errors import DataIsMissingError

if TYPE_CHECKING:
    from simple_text_renderer.formatters.base import IBlockFormatter
    from simple_text_renderer.renderers.base import IBlockRenderer


@dataclasses.dataclass(slots=True)
class PlainTextData(Data):
    """
    Data class for containing plain text data.

    Attributes:
        text (str): Plain text data.
    """

    text: str


class PlainText(BaseBlock[PlainTextData]):
    """Block containing plain text data."""

    @classmethod
    def by_data(
        cls,
        *,
        name: str | None = None,
        formatter: IBlockFormatter | None = None,
        renderer: IBlockRenderer | None = None,
        **data: Any,  # noqa: ANN401
    ) -> Self:
        """
        Create a new PlainText block by providing the text data.

        Args:
            name (str | None): Name of the block. If not specified, it will be generated automatically.
            formatter (IBlockFormatter | None): Specific formatter to use for this block.
            renderer (IBlockRenderer[Data] | None): Specific renderer to use for this block.
            **data (Any): Number of keyword arguments to initialize the block data. Must contain the `text` key.

        Keyword Args:
            text (str): Plain text data.

        Returns:
            PlainText: New PlainText block object.

        Raises:
            DataIsMissingError: If the `text` key is not present in the `data` dictionary.
        """
        if "text" not in data:
            msg = "`**data` dictionary must contain the `text` key."
            raise DataIsMissingError(msg)
        return cls(PlainTextData(text=data["text"]), name=name, formatter=formatter, renderer=renderer)
