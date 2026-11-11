from collections.abc import Callable, Iterable
from dataclasses import dataclass, replace
from datetime import timedelta
from typing import Self

from subclean.text import visible_len


@dataclass(frozen=True, slots=True)
class Cue:
    start: timedelta
    end: timedelta
    lines: tuple[str, ...] = ()

    def with_lines(self, lines: Iterable[str]) -> Self:
        return replace(self, lines=tuple(lines))

    def map_lines(self, fn: Callable[[str], str | None]) -> Self:
        return self.with_lines(
            mapped for line in self.lines if (mapped := fn(line)) is not None
        )

    def is_empty(self) -> bool:
        return all(visible_len(line) == 0 for line in self.lines)

    @property
    def text(self) -> str:
        return "\n".join(self.lines)
