from pathlib import Path

import pytest

from subclean import io
from subclean.cue import Cue

RESOURCES = Path(__file__).parent / "resources"


@pytest.fixture
def load():
    def _load(name: str) -> list[Cue]:
        return io.load(RESOURCES / name)

    return _load
