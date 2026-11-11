from collections.abc import Sequence
from typing import Protocol

from subclean.cue import Cue


class Processor(Protocol):
    def __call__(self, cues: Sequence[Cue], /) -> list[Cue]: ...


class LineProcessor(Processor, Protocol):
    """Processor that handles each line independently; returning None drops the line."""

    def process_line(self, line: str, /) -> str | None: ...

    def __call__(self, cues: Sequence[Cue], /) -> list[Cue]:
        return [cue.map_lines(self.process_line) for cue in cues]
