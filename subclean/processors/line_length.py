from collections.abc import Iterator, Sequence
from dataclasses import dataclass

from subclean import text
from subclean.cue import Cue
from subclean.processors.base import Processor


def split_dialog(lines: Sequence[str]) -> list[list[str]]:
    chunks: list[list[str]] = []
    for i, line in enumerate(lines):
        if i == 0 or text.is_dialog(line):
            chunks.append([line])
        else:
            chunks[-1].append(line)
    return chunks


@dataclass(frozen=True, slots=True)
class LineLength(Processor):
    max_length: int = 50

    def merge(self, lines: Sequence[str]) -> Iterator[str]:
        for chunk in split_dialog(lines):
            merged = " ".join(chunk)
            if len(chunk) > 1 and text.visible_len(merged) < self.max_length:
                yield merged
            else:
                yield from chunk

    def __call__(self, cues: Sequence[Cue], /) -> list[Cue]:
        return [cue.with_lines(self.merge(cue.lines)) for cue in cues]
