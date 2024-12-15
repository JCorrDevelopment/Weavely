from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any, Self

from std_utils.more_typing.undefined import DOC_UNDEFINED, is_undefined

from .base import BaseBlock, Data

if TYPE_CHECKING:
    from collections.abc import Sequence

    from simple_text_renderer.formatters.base import FormatterProtocol


@dataclasses.dataclass
class PlainText(Data):
    """
    Data class for plain text block.

    Contains a single string with plain text.
    """

    text: str


class PlainTextBlock(BaseBlock[PlainText]):
    """
    Block for plain text.

    Contains a single string with plain text. Can be used to represent any text data.
    """

    @classmethod
    def by_content(
        cls,
        *,
        name: str | None = None,
        formatters: Sequence[FormatterProtocol[PlainText]] = (),
        text: str = DOC_UNDEFINED,
        **kwargs: Any,  # noqa: ANN401, ARG003
    ) -> Self:
        """
        Create a plain text block by provided text.

        Args:
            name (str | None): Optional name of the block. Used to reference the block in the file. If None, the block
                will generate it based on the class name and some randomized suffix.
            formatters (Sequence[FormatterProtocol[PlainText]]): Collection of formatters that can be applied to the
                data object. Note that formatters are applied in the order they are provided.
            text (str): Plain text block parameters.
            kwargs: Not required. Specified for the seek of good code practices.

        Returns:
            PlainTextBlock: Created plain text block.

        Raises:
            ValueError: If text is not provided.
        """
        if is_undefined(text):
            msg = "Text is required for PlainTextBlock creation."
            raise ValueError(msg)
        return cls(PlainText(text=text), name=name, formatters=formatters)
