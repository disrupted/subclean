import re

from subclean.processors.base import LineProcessor

_SIMPLE_CHARS = re.compile(r"^[^a-hj-z.,;?!]*$")
_SIMPLE_MARKERS = re.compile(r"[A-Z]{2,}|(<i>)?♪+(</i>)?")
_PARENTHESES_ONLY = re.compile(r"^([-‐\s<i>]+)?[(\[*][^)\]]+[)\]*</i>]+$")
_MUSIC = re.compile(
    r"""
    ^[-\ ♪<i>]*\s?
    ([-‐a-z,]+\s)*
    \b(music(al)?|song|track)\b\s?
    (((play|swell)(s|ing)|intensifies|crescendo|sting)|(fades\ (in|out)))?\b
    (\s?over\s(headphones|speakers))?
    [\s♪</i>]*$
    |vocalizing
    """,
    re.VERBOSE,
)
_SPEAKER = re.compile(
    r"^([-‐\s<i>]+)?((\b[-A-Za-z.']+\s?#?\d?){1,2}(?!\.)([\[(][\w\s]*[\])])?:(?!\w)|\[+.*[\]:]+)(</?i>)?\s*"
)
_PARENTHESES = re.compile(r"[(\[*].*?[)\]*:]+")
_BRACKETS = re.compile(r"[()\[\]]")


def is_simple_hi(line: str) -> bool:
    return bool(_SIMPLE_CHARS.search(line) and _SIMPLE_MARKERS.search(line))


def is_parentheses(line: str) -> bool:
    return _PARENTHESES_ONLY.search(line) is not None


def is_music(line: str) -> bool:
    return _MUSIC.search(line) is not None


def is_hi(line: str) -> bool:
    return is_simple_hi(line) or is_parentheses(line) or is_music(line)


def has_unbalanced_brackets(line: str) -> bool:
    return bool(_BRACKETS.search(line)) and (
        line.count("(") != line.count(")") or line.count("[") != line.count("]")
    )


def contains_hi(line: str) -> bool:
    return bool(_SPEAKER.search(line) or _PARENTHESES.search(line))


def clean_parentheses(line: str) -> str:
    return _PARENTHESES.sub("", line)


def clean_hi(line: str) -> str:
    return clean_parentheses(_SPEAKER.sub(r"\1\5", line))


class SDH(LineProcessor):
    def process_line(self, line: str, /) -> str | None:
        if is_hi(line) or has_unbalanced_brackets(line):
            return None
        return clean_hi(line) if contains_hi(line) else line
