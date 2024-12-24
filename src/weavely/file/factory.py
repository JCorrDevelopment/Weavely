"""
Module contains factory functions for creating predefined SimpleFile objects for the most common use cases.

You may use those items instead of populating everything on you own from scratch.
"""

__all__ = [
    "get_empty_file",
    "get_markdown_file",
    "get_txt_file",
]


from ..blocks.heading import Heading
from ..blocks.paragraph import Paragraph
from ..renderers.heading import HeadingMarkdownRenderer, HeadingPlainTextRenderer
from ..renderers.paragraph import WrappedParagraphRenderer
from .file import SimpleFile, WeavelyFile


def get_empty_file() -> SimpleFile:
    """
    Get an empty WeavelyFile object.

    Returns:
        WeavelyFile: Empty file object.
    """
    return SimpleFile()


def get_markdown_file() -> WeavelyFile:
    """
    Get an WeavelyFile object useful for writing of Markdown files.

    Returns:
        WeavelyFile: WeavelyFile object with Markdown data support.
    """
    simple_file = WeavelyFile()
    simple_file.set_renderer(Heading, HeadingMarkdownRenderer())
    simple_file.set_renderer(Paragraph, WrappedParagraphRenderer())
    return simple_file


def get_txt_file() -> WeavelyFile:
    """
    Get an WeavelyFile object useful for writing of plain text files.

    It contains standard formatters and renderers for text data representation.

    Returns:
        WeavelyFile: WeavelyFile object with text data support.
    """
    simple_file = WeavelyFile()
    simple_file.set_renderer(Heading, HeadingPlainTextRenderer())
    simple_file.set_renderer(Paragraph, WrappedParagraphRenderer())
    return simple_file
