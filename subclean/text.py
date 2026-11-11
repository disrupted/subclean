import re

_TAG = re.compile(r"<[^>]*>|\{[^}]*\}")
_OUTER_SPACE = re.compile(r"^(</?i>)*\s+|\s+(</?i>)*$")
_DIALOG = re.compile(r"^(</?i>)*-")


def strip_tags(line: str) -> str:
    return _TAG.sub("", line)


def visible_len(line: str) -> int:
    return len(strip_tags(line))


def strip(line: str) -> str:
    """Like str.strip, but also strips whitespace hidden behind <i> tags."""
    return _OUTER_SPACE.sub(r"\1\2", line)


def is_dialog(line: str) -> bool:
    return _DIALOG.match(line) is not None
