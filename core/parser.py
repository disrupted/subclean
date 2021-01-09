import logging
import os

from core.subtitle import Subtitle, SubtitleFormat


class SubtitleParser:
    def load(self, filepath: str) -> Subtitle:
        fname, fext = os.path.splitext(filepath)
        if fext not in SubtitleFormat.values():
            raise NotImplementedError
        logging.info(f"importing subtitle {filepath}")
        handler = SubtitleFormat.get_handler(fext)
        return handler(filepath)
