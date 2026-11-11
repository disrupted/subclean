import re
from collections.abc import Callable
from typing import ClassVar

from subclean import text
from subclean.processors.base import LineProcessor

type LineFix = Callable[[str], str]


def substitution(pattern: str, replacement: str) -> LineFix:
    compiled = re.compile(pattern)
    return lambda line: compiled.sub(replacement, line)


clean_dashes = substitution(r"^(</?i>)*([-‐]+)(\s+)?", r"\1- ")

fix_spaces = substitution(r"\b([.?!]+)([A-Z][a-z])", r"\1 \2")
_collapse_whitespace = substitution(r"\s+(</?i>)*\s*", r" \1")
_remove_space_before_punctuation = substitution(
    r"(?<!^-)(?<!\.{3})\s+([.,!?]+)(?!\d)", r"\1"
)
_collapse_space_after_punctuation = substitution(r"([.,!?]+)\s{2,}(?!$)", r"\1 ")
fix_hyphen = substitution(r"'’", "'")
fix_ampersand = substitution(r"&amp;", "&")
fix_quote = substitution(r"&quot;", '"')
fix_music = substitution(r"^#\s", "♪ ")

fix_styles = substitution(r"</?i>(\s*)</?i>", r"\1")


def trim_whitespace(line: str) -> str:
    return text.strip(_collapse_whitespace(line))


def fix_space_punctuation(line: str) -> str:
    return _collapse_space_after_punctuation(_remove_space_before_punctuation(line))


class Fixes(LineProcessor):
    fixes: ClassVar[tuple[LineFix, ...]] = ()

    def process_line(self, line: str, /) -> str:
        for fix in self.fixes:
            line = fix(line)
        return line


class Dialog(Fixes):
    fixes = (clean_dashes,)


class Error(Fixes):
    fixes = (
        fix_hyphen,
        fix_spaces,
        fix_space_punctuation,
        trim_whitespace,
        fix_ampersand,
        fix_quote,
        fix_music,
    )


class Style(Fixes):
    fixes = (fix_styles,)
