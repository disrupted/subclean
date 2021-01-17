#!/usr/bin/env python3
import argparse
import logging

from core.parser import SubtitleParser
from core.subtitle import Subtitle
from processors.processor import DialogProcessor, ErrorProcessor, SDHProcessor

logging.basicConfig(format="%(levelname)s %(message)s", level=logging.DEBUG)

DEFAULT_PROCESSORS = [SDHProcessor, DialogProcessor, ErrorProcessor]


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
    for processor in DEFAULT_PROCESSORS:
        subtitle = processor(subtitle).process()
    subtitle.print()
    subtitle.save()


if __name__ == "__main__":
    main()
