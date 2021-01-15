import logging
from pathlib import Path

from core.subtitle import Subtitle, SubtitleFormat


class SubtitleParser:
    def load(self, filepath: str) -> Subtitle:
        p = Path(filepath)
        if p.suffix not in SubtitleFormat.values():
            raise NotImplementedError
        logging.info(f"importing subtitle {filepath}")
        handler = SubtitleFormat.get_handler(p.suffix)
        return handler(filepath)
