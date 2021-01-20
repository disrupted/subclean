import re
from typing import Callable, List

from core.section import Section
from core.subtitle import Subtitle


class Processor:
    def __init__(self, subtitle: Subtitle):
        self.subtitle = subtitle
        self.operations: List[Callable] = []

    def process(self) -> Subtitle:
        for i, section in enumerate(self.subtitle.sections):
            for j, line in enumerate(section.lines):
                for operation in self.operations:
                    line = operation(line)
                self.subtitle.sections[i].lines[j] = line
        return self.subtitle


class DialogProcessor(Processor):
    def __init__(self, subtitle: Subtitle):
        super().__init__(subtitle)
        self.operations: List[Callable] = [self.clean_dashes]

    @classmethod
    def clean_dashes(cls, line: str) -> str:
        return re.sub(r"^(<\/?i>)*([-‐]+)(\s+)?", r"\1- ", line)


class SDHProcessor(Processor):
    def __init__(self, subtitle: Subtitle):
        super().__init__(subtitle)
        self.operations: List[Callable] = [self.clean_hi]

    @classmethod
    def is_hi(cls, line: str) -> bool:
        return bool(
            cls.is_simple_hi(line) or cls.is_parentheses(line) or cls.is_music(line)
        )

    @classmethod
    def is_simple_hi(cls, line: str) -> bool:
        return bool(
            re.search(r"^[^a-hj-z.,;?!]*$", line)
            and re.search(r"[A-Z]{2,}|(<i>)?[♪]+(<\/i>)?", line)
        )

    @classmethod
    def is_parentheses(cls, line: str) -> bool:
        return bool(re.search(r"^([-‐\s<i>]+)?[(\[*][^\)\]]+[)\]*<\/i>]+$", line))

    @classmethod
    def is_music(cls, line: str) -> bool:
        return bool(
            re.search(
                r"^[- ♪]+\s?([-‐a-z,]+\s)*\b(music(al)?|song|track)\b\s?(((play|swell)(s|ing)|intensifies|crescendo|sting))?\b(\s?over\s(headphones|speakers))?\s?♪$",
                line,
            )
        )

    @classmethod
    def contains_hi(cls, line: str) -> bool:
        return bool(
            re.search(
                r"^([-\s<i>]+)?((\b[-\w.']+\s?#?\d?){1,2}(?!\.)([\[(][\w\s]*[\])])?:(?![\S])|[\[]+.*[\]:]+)(\s+)?|\s?[(\[*].*?[)\]*:]+\s?",
                line,
            )
        )

    @classmethod
    def clean_hi(cls, line: str) -> str:
        """Clean hearing impaired."""
        return re.sub(
            r"^([-\s<i>]+)?((\b[-\w.']+\s?#?\d?){1,2}(?!\.)([\[(][\w\s]*[\])])?:(?![\S])|[\[]+.*[\]:]+)(\s+)?",
            r"\1",
            line,
        )

    @classmethod
    def is_parenthesis_not_matching(cls, line: str) -> bool:
        return bool(
            re.search(r"[()\[\]]", line)
            and (
                line.count("(") != line.count(")") or line.count("[") != line.count("]")
            )
        )

    # def clean_parentheses(cls, line: str) -> str:
    #     """Clean parentheses ()[]."""
    #     return re.sub(r"\s?[(\[*].*?[)\]*:]+\s?", "", line)

    @classmethod
    def clean_section(cls, section: Section) -> Section:
        lines: List[str] = []
        for line in section.lines:
            if cls.is_hi(line) or cls.is_parenthesis_not_matching(line):
                continue
            elif cls.contains_hi(line):
                line = cls.clean_hi(line)
            lines.append(line)
        section.lines = lines
        return section

    def process(self) -> Subtitle:
        # Clean sections
        self.subtitle.sections = [self.clean_section(s) for s in self.subtitle.sections]
        # Remove empty sections
        self.subtitle.sections = [s for s in self.subtitle.sections if not s.is_empty()]
        return self.subtitle


class ErrorProcessor(Processor):
    def __init__(self, subtitle: Subtitle):
        super().__init__(subtitle)
        self.operations: List[Callable] = [
            self.fix_hyphen,
            self.fix_spaces,
            self.trim_whitespace,
            self.fix_ampersand,
            self.fix_quote,
            self.fix_music,
        ]

    @classmethod
    def fix_spaces(cls, line: str) -> str:
        """Add missing spaces between sentences."""
        return re.sub(r"\b([.?!]{1,2})([A-Z][a-z])", r"\1 \2", line)

    @classmethod
    def trim_whitespace(cls, line: str) -> str:
        return re.sub(r"\s{2,}", " ", line)

    @classmethod
    def fix_hyphen(cls, line: str) -> str:
        return re.sub(r"'’", "'", line)

    @classmethod
    def fix_ampersand(cls, line: str) -> str:
        return re.sub(r"&amp;", "&", line)

    @classmethod
    def fix_quote(cls, line: str) -> str:
        return re.sub(r"&quot;", '"', line)

    @classmethod
    def fix_music(cls, line: str) -> str:
        return re.sub(r"^#\s", "♪ ", line)
