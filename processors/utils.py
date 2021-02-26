import re


def remove_styles(line: str) -> str:
    return re.sub(r"<\/?i>", "", line)
