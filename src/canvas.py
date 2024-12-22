"""
Canvas module.

Useful to play with items you're currently working on.

Please, do not commit any changes in this file.
"""

from simple_text_renderer.blocks.txt import PlainTextData
from simple_text_renderer.file.factory import get_txt_file


def main() -> None:  # noqa: D103
    # Enter your code here
    def reverse_formatter(data: PlainTextData) -> PlainTextData:
        return PlainTextData(text=data.text[::-1])

    file = get_txt_file()
    file.content.add_plain_text("Hello, World!")
    file.content.add_plain_text("This is a test.", formatter=reverse_formatter)
    file.content.add_plain_text("This is also test.")
    print(file.as_str())


if __name__ == "__main__":
    main()
