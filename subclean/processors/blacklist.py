import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Self

from subclean.processors.base import LineProcessor

PATTERNS: tuple[str, ...] = (
    r"^[-_–*:.]+$",
    r"^\*|\*$",
    r"Addic7ed|Subscene|Podnapisi|Subtitles",
    r"Support us and become VIP member|remove all ads|Advertise your product or brand here|Hier könnte deine Werbung stehen",
    r"\b(rate this subtitle|Help other users to choose the best subtitles|Helfe anderen Usern die besten Untertitel auszuwählen)\b",
    r"Übersetzung:|Untertitel:",
    r"\b((sub(title)?s?|sync(e|')?d?|cleaned|corrected|rip(ped)?|improved|encod|resync|edit|caption|version|provided)(ed|ing)?\b\s((&|and|,)\s)?)+(by|for|at)\b",
    r"www\.|https?://|\.(org|link|com)",
    r"\[at\]",
    r"WEB[- ]?(DL|Rip)|HDTV|dTV",
    r"\bSDH\b|Season\s*\d+[\s-]+Episode\s*\d+|Episode\s+Title",
    r"greetings from roNy|missing words added by",
    r"300MBUNiTED|:{2,}|Free Online Movies|SharePirate.Com|Sub Upload Date|\bSync:",
    r"\b(WARNER BROS|Media Access Group|WGBH)\b",
)


def _compile(patterns: Iterable[str]) -> re.Pattern[str]:
    return re.compile("|".join(f"(?:{p})" for p in patterns), re.IGNORECASE)


DEFAULT_PATTERN = _compile(PATTERNS)


@dataclass(frozen=True, slots=True)
class Blacklist(LineProcessor):
    pattern: re.Pattern[str] = DEFAULT_PATTERN

    @classmethod
    def with_extra(cls, *patterns: str) -> Self:
        return cls(_compile((*PATTERNS, *patterns)))

    def matches(self, line: str) -> bool:
        return self.pattern.search(line) is not None

    def process_line(self, line: str, /) -> str | None:
        return None if self.matches(line) else line
