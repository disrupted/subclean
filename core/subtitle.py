import logging
from enum import Enum
from pathlib import Path
from typing import Callable, List, Optional, Set

from core.section import Section, SrtSection
from core.section.timing import SrtSectionTiming

ENCODINGS = [
    "utf-8-sig",
    "iso-8859-1",
]


class Subtitle:
    def __init__(self, filepath: str):
        self.filepath: str = filepath
        self.encoding: Optional[str] = self.load()
        self.file: List[str]
        self.sections: List[Section] = []

    def load(self) -> Optional[str]:
        for e in ENCODINGS:
            try:
                with open(self.filepath, "r", encoding=e) as f:
                    f.readlines()
                    f.seek(0)
                    return e
            except UnicodeDecodeError:
                logging.error("UnicodeDecodeError for encoding %s" % e)
        return None

    def parse(self):
        pass

    def add_section(self, section: Section):
        self.sections.append(section)

    def pop_section(self, index: int):
        self.sections.pop(index)

    def print(self):
        for section in self.sections:
            print(section)

    def save(self, output_filepath: Optional[str] = None):
        pass


class SrtSubtitle(Subtitle):
    def __init__(self, filepath: str):
        super().__init__(filepath)

    def __parse_timing(self, input: str) -> SrtSectionTiming:
        start_time, end_time = input.split(" --> ")
        return SrtSectionTiming(start_time, end_time)

    def parse(self):
        with open(self.filepath, "r", encoding=self.encoding) as f:
            lines: List[str] = list(line.strip() for line in f) + [""]

        for line in lines:
            # empty line (end of section) or index number (begin of section)
            if not line or line.isdigit():
                continue
            # timing
            elif " --> " in line:
                timing = self.__parse_timing(line)
                section = SrtSection(timing)
                self.sections.append(section)
            # content
            else:
                self.sections[-1].add_line(line)

    def save(self, output_filepath: Optional[str] = None):
        if output_filepath is None:
            p = Path(self.filepath)
            output_filepath = f"{p.stem}_output{p.suffix}"
        with open(output_filepath, "w") as out_f:
            for index, section in enumerate(self.sections, start=1):
                out_f.write(f"{index}\n{section}\n")


class FakeSubtitle(Subtitle):
    def __init__(self):
        pass


class SubtitleFormat(Enum):
    def __init__(self, ext, handler):
        self.ext: str = ext
        self.handler: Callable[Subtitle] = handler

    @classmethod
    def get_handler(self, ext: str) -> Callable:
        return list(e.handler for e in self if e.ext == ext)[0]

    @classmethod
    def values(self) -> Set[str]:
        return set(e.ext for e in self)

    SRT = (".srt", SrtSubtitle)
