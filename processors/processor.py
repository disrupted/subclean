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

    def clean_dashes(self, line: str) -> str:
        return re.sub(r"^(<\/?i>)*([-‐]+)(\s+)?", r"\1- ", line)


class SDHProcessor(Processor):
    def __init__(self, subtitle: Subtitle):
        super().__init__(subtitle)
        self.operations: List[Callable] = [self.clean_hi]

    def is_hi(self, line: str) -> bool:
        return bool(
            self.is_simple_hi(line) or self.is_parentheses(line) or self.is_music(line)
        )

    def is_simple_hi(self, line: str) -> bool:
        return bool(
            re.search(r"^[^a-hj-z.,;?!]*$", line)
            and re.search(r"[A-Z]{2,}|(<i>)?[♪]+(<\/i>)?", line)
        )

    def is_parentheses(self, line: str) -> bool:
        return bool(re.search(r"^([-‐\s<i>]+)?[(\[*][^\)\]]+[)\]*<\/i>]+$", line))

    def is_music(self, line: str) -> bool:
        return bool(
            re.search(
                r"^[- ♪]+\s?([-‐a-z,]+\s)*\b(music(al)?|song|track)\b\s?(((play|swell)(s|ing)|intensifies|crescendo|sting))?\b(\s?over\s(headphones|speakers))?\s?♪$",
                line,
            )
        )

    def contains_hi(self, line: str) -> bool:
        return bool(
            re.search(
                r"^([-\s<i>]+)?((\b[-\w.']+\s?#?\d?){1,2}(?!\.)([\[(][\w\s]*[\])])?:(?![\S])|[\[]+.*[\]:]+)(\s+)?|\s?[(\[*].*?[)\]*:]+\s?",
                line,
            )
        )

    def clean_hi(self, line: str) -> str:
        """Clean hearing impaired."""
        return re.sub(
            r"^([-\s<i>]+)?((\b[-\w.']+\s?#?\d?){1,2}(?!\.)([\[(][\w\s]*[\])])?:(?![\S])|[\[]+.*[\]:]+)(\s+)?",
            r"\1",
            line,
        )

    # def clean_parentheses(self, line: str) -> str:
    #     """Clean parentheses ()[]."""
    #     return re.sub(r"\s?[(\[*].*?[)\]*:]+\s?", "", line)

    def clean_section(self, section: Section) -> Section:
        lines: List[str] = []
        for line in section.lines:
            if self.is_hi(line):
                continue
            elif self.contains_hi(line):
                line = self.clean_hi(line)
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

    def fix_spaces(self, line: str) -> str:
        """Add missing spaces between sentences."""
        return re.sub(r"\b([.?!]{1,2})([A-Z][a-z])", r"\1 \2", line)

    def trim_whitespace(self, line: str) -> str:
        return re.sub(r"\s{2,}", " ", line)

    def fix_hyphen(self, line: str) -> str:
        return re.sub(r"'’", "'", line)

    def fix_ampersand(self, line: str) -> str:
        return re.sub(r"&amp;", "&", line)

    def fix_quote(self, line: str) -> str:
        return re.sub(r"&quot;", '"', line)

    def fix_music(self, line: str) -> str:
        return re.sub(r"^#\s", "♪ ", line)
