#!/usr/bin/env python3
import argparse
import logging
import os
from enum import Enum
from typing import List, Optional, Set

ENCODINGS = [
    "utf-8-sig",
    "iso-8859-1",
]

logging.basicConfig(format="%(levelname)s %(message)s", level=logging.DEBUG)


class Subtitle:
    def __init__(self, filepath: str):
        self.filepath: str = filepath
        self.encoding: Optional[str] = self.load()
        self.file: List[str]
        self.sections: List[SrtSection] = []

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

    def print(self):
        for section in self.sections:
            print(section)

    def save(self, output_filepath: Optional[str] = None):
        pass


class SrtSectionTiming:
    def __init__(self, start_time: str, end_time: str):
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self) -> str:
        return f"{self.start_time} --> {self.end_time}"


class SrtSection:
    def __init__(self, timing: SrtSectionTiming, lines: Optional[List[str]] = None):
        self.timing: SrtSectionTiming = timing
        self.lines: List[str] = lines if lines is not None else []

    def add_line(self, line: str):
        self.lines.append(line)

    def content(self) -> str:
        return "\n".join(self.lines)

    def __str__(self) -> str:
        return f"{self.timing}\n{self.content()}\n"


class SrtSubtitle(Subtitle):
    def __init__(self, filepath: str):
        super().__init__(filepath)

    def __parse_timing(self, input: str) -> SrtSectionTiming:
        start_time, end_time = input.split(" --> ")
        return SrtSectionTiming(start_time, end_time)

    def parse(self):
        with open(self.filepath, "r", encoding=self.encoding) as f:
            in_f: List[str] = list(line.strip() for line in f) + [""]

        section: SrtSection = None
        for line in in_f:
            # index number
            if line.isdigit():
                continue
            # timing
            elif " --> " in line:
                timing = self.__parse_timing(line)
                section = SrtSection(timing)
            # empty line, that means end of a block
            elif not line:
                self.sections.append(section)
            # content
            else:
                section.add_line(line)

    def save(self, output_filepath: Optional[str] = None):
        if output_filepath is None:
            fname, fext = os.path.splitext(self.filepath)
            output_filepath = f"{fname}_output{fext}"
        with open(output_filepath, "w") as out_f:
            for index, section in enumerate(self.sections, start=1):
                out_f.write(f"{index}\n{section}\n")


class SubtitleFormat(Enum):
    def __init__(self, ext, handler):
        self.ext: str = ext
        self.handler: Subtitle = handler

    @classmethod
    def get_handler(self, ext: str) -> List[Subtitle]:
        return list(e.handler for e in self if e.ext == ext)[0]

    @classmethod
    def values(self) -> Set[str]:
        return set(e.ext for e in self)

    SRT = (".srt", SrtSubtitle)


class SubtitleParser:
    def load(self, filepath: str) -> Subtitle:
        fname, fext = os.path.splitext(filepath)
        if fext not in SubtitleFormat.values():
            raise NotImplementedError
        logging.info(f"importing subtitle {filepath}")
        handler = SubtitleFormat.get_handler(fext)
        return handler(filepath)


def main():
    argparser = argparse.ArgumentParser(description="Clean Subtitles")
    argparser.add_argument(
        "file",
        metavar="FILE",
        type=argparse.FileType("r"),
        help="the subtitle file to be processed",
    )
    args = argparser.parse_args()

    parser = SubtitleParser()
    subtitle: Subtitle = parser.load(args.file.name)
    subtitle.parse()
    subtitle.print()
    subtitle.save()


if __name__ == "__main__":
    main()
