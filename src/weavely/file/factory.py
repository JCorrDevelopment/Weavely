"""
Module contains factory functions for creating predefined SimpleFile objects for the most common use cases.

You may use those items instead of populating everything on you own from scratch.
"""

__all__ = [
    "get_empty_file",
    "get_txt_file",
]

from weavely.blocks.txt import PlainTextData, TitleData

from ..formatters.txt import TextWrapFormatter, TitleCapitalizationFormatter
from ..renderers.txt import PlainTextRenderer, TitleRenderer
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
    simple_file.set_renderer(TitleData, TitleRenderer())
    simple_file.set_formatter(TitleData, TitleCapitalizationFormatter())
    return simple_file
