import re
from collections.abc import Sequence
from datetime import timedelta

from subclean.cue import Cue

_TIMESTAMP = r"(\d+):(\d{2}):(\d{2})[,.](\d{3})"
_TIMING = re.compile(rf"{_TIMESTAMP}\s*-->\s*{_TIMESTAMP}")


def _timedelta(hours: str, minutes: str, seconds: str, millis: str) -> timedelta:
    return timedelta(
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds),
        milliseconds=int(millis),
    )


def _timestamp(value: timedelta) -> str:
    total_ms = value // timedelta(milliseconds=1)
    seconds, ms = divmod(total_ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"


class SrtFormat:
    def parse(self, text: str, /) -> list[Cue]:
        cues: list[Cue] = []
        timing: tuple[timedelta, timedelta] | None = None
        lines: list[str] = []

        def flush() -> None:
            if timing is not None:
                cues.append(Cue(*timing, tuple(lines)))

        rows = [row.strip() for row in text.splitlines()]
        for i, row in enumerate(rows):
            if match := _TIMING.match(row):
                flush()
                groups = match.groups()
                timing = (_timedelta(*groups[:4]), _timedelta(*groups[4:]))
                lines = []
            elif not row or self._is_index(rows, i):
                continue
            elif timing is not None:
                lines.append(row)
        flush()
        return cues

    def dump(self, cues: Sequence[Cue], /) -> str:
        return "".join(
            f"{index}\n{_timestamp(cue.start)} --> {_timestamp(cue.end)}\n{cue.text}\n\n"
            for index, cue in enumerate(cues, start=1)
        )

    @staticmethod
    def _is_index(rows: Sequence[str], i: int) -> bool:
        return (
            rows[i].isdigit() and i + 1 < len(rows) and bool(_TIMING.match(rows[i + 1]))
        )
