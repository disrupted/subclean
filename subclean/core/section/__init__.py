from __future__ import annotations

from subclean.core.line import Line
from subclean.core.section.timing import SectionTiming, SrtSectionTiming


class Section:
    def __init__(self, timing: SectionTiming, lines: list[Line] | None = None):
        self.timing: SectionTiming = timing
        self.lines: list[Line] = lines if lines is not None else []

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
        return "\n".join(self.lines)

    def __repr__(self) -> str:
        return self.content()

    def __len__(self) -> int:
        return len(self.lines)


class SrtSection(Section):
    def __init__(self, timing: SrtSectionTiming, lines: list[Line] | None = None):
        super().__init__(timing, lines)

    def __str__(self) -> str:
        return f"{self.timing}\n{self.content().strip()}\n"
