import re
from typing import Callable, List

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
                self.subtitle.sections[i].lines[j] = self.clean_dashes(line)
        return self.subtitle


class DialogProcessor(Processor):
    def __init__(self, subtitle: Subtitle):
        super().__init__(subtitle)
        self.operations: List[Callable] = [self.clean_dashes]

    def clean_dashes(self, line: str) -> str:
        return re.sub(r"^(<\/?i>)*([-‐]+)(\s+)?", r"\1- ", line)


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
