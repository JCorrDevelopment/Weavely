"""
Module contains factory functions for creating predefined SimpleFile objects for the most common use cases.

You may use those items instead of populating everything on you own from scratch.
"""

__all__ = [
    "get_empty_file",
    "get_txt_file",
]

from simple_text_renderer.blocks.txt import PlainTextData

from ..formatters.txt import TextWrapFormatter
from ..renderers.txt import PlainTextRenderer
from .file import SimpleFile


def get_empty_file() -> SimpleFile:
    """
    Get an empty SimpleFile object.

    Returns:
        SimpleFile: Empty file object.
    """
    return SimpleFile()


def get_txt_file() -> SimpleFile:
    """
    Get an SimpleFile object useful for writing of plain text files.

    It contains standard formatters and renderers for text data representation.

    Returns:
        SimpleFile: SimpleFile object with text data support.
    """
    simple_file = SimpleFile()
    simple_file.set_renderer(PlainTextData, PlainTextRenderer())
    simple_file.set_formatter(PlainTextData, TextWrapFormatter())
    return simple_file