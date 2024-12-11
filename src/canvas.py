"""
Canvas module.

Useful to play with items you're currently working on.

Please, do not commit any changes in this file.
"""

import textwrap

from simple_text_renderer.blocks.text import PlainText
from simple_text_renderer.file import SimpleFile
from simple_text_renderer.renderers.txt import TxtRenderer


def long_text_wrapper(data: PlainText) -> PlainText:
    data.text = "\n".join(textwrap.wrap(data.text, width=120))
    return data


def main() -> None:  # noqa: D103
    # Enter your code here
    file = SimpleFile(renderer=TxtRenderer())
    file.add_plain_text("Hello, World!")
    file.add_plain_text("Hello, World again!\nAre you waiting for this? :)", formatters=())
    file.add_plain_text(
        (
            "In the fast-paced world of technology and innovation, the boundaries of possibility seem to expand with "
            "each passing day. New discoveries, tools, and techniques emerge constantly, reshaping industries and "
            "society at large. From artificial intelligence to quantum computing, the future appears both exciting "
            "and daunting. While some fear the rapid pace of change, others see it as an opportunity to solve some "
            "of humanity's greatest challenges. The intersection of creativity and technology is where the magic "
            "happens, fostering solutions that were once thought to be the stuff of science fiction. However, with "
            "these advancements come new responsibilities. Ethical concerns around privacy, autonomy, and the impact "
            "on jobs and society must be carefully considered. As we navigate this brave new world, collaboration, "
            "education, and thoughtful regulation will play crucial roles in ensuring that technology serves the "
            "greater good. The journey is just beginning, and only time will reveal how it will shape our future."
        ),
        formatters=(long_text_wrapper,),
    )
    file.to_file("output.txt")


if __name__ == "__main__":
    main()
