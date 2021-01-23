from pathlib import Path
from typing import Callable

from loguru import logger

from core.subtitle import Subtitle, SubtitleFormat


class SubtitleParser:
    def load(self, filepath: str) -> Subtitle:
        p = Path(filepath)
        if p.suffix not in SubtitleFormat.values():
            raise NotImplementedError
        logger.info("importing subtitle {}", filepath)
        handler: Callable = SubtitleFormat.get_handler(p.suffix)
        subtitle: Subtitle = handler(filepath)
        return subtitle
