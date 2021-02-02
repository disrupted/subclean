from typing import List, Optional

from core.section.timing import SectionTiming, SrtSectionTiming


class Section:
    def __init__(self, timing: SectionTiming, lines: Optional[List[str]] = None):
        self.timing: SectionTiming = timing
        self.lines: List[str] = lines if lines is not None else []

    def add_line(self, line: str):
        self.lines.append(line)

    def remove_line(self, line: str) -> bool:
        self.lines.remove(line)
        return self.is_empty()

    def pop_line(self, index: int) -> bool:
        self.lines.pop(index)
        return self.is_empty()

    def is_empty(self) -> bool:
        return sum(len(line) for line in self.lines) == 0

    def content(self) -> str:
        pass


class SrtSection(Section):
    def __init__(self, timing: SrtSectionTiming, lines: Optional[List[str]] = None):
        super().__init__(timing, lines)

    def content(self) -> str:
        return "\n".join(self.lines)

    def __str__(self) -> str:
        return f"{self.timing}\n{self.content()}\n"
