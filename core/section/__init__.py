from typing import List

from core.line import Line
from core.section.timing import SectionTiming, SrtSectionTiming


class Section:
    def __init__(self, timing: SectionTiming, lines: List[Line] = []):
        self.timing: SectionTiming = timing
        self.lines: List[Line] = lines

    def add_line(self, line: Line) -> None:
        self.lines.append(line)

    def remove_line(self, line: Line) -> bool:
        self.lines.remove(line)
        return self.is_empty()

    def pop_line(self, index: int) -> bool:
        self.lines.pop(index)
        return self.is_empty()

    def join(self) -> Line:
        return Line(" ".join(self.lines))

    def merge_lines(self) -> None:
        self.lines = [self.join()]

    def is_empty(self) -> bool:
        return sum(len(line) for line in self.lines) == 0

    def content(self) -> str:
        pass

    def __len__(self) -> int:
        return len(self.lines)


class SrtSection(Section):
    def __init__(self, timing: SrtSectionTiming, lines: List[Line] = []):
        super().__init__(timing, lines)

    def content(self) -> str:
        return "\n".join(self.lines)

    def __str__(self) -> str:
        return f"{self.timing}\n{self.content()}\n"
