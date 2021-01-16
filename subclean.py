#!/usr/bin/env python3
import argparse
import logging

from core.parser import SubtitleParser
from core.subtitle import Subtitle
from processors.processor import DialogProcessor, SDHProcessor

logging.basicConfig(format="%(levelname)s %(message)s", level=logging.DEBUG)


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
    # processor = DialogProcessor(subtitle)
    # subtitle = processor.process()
    processors = [SDHProcessor, DialogProcessor]
    for processor in processors:
        p = processor(subtitle)
        subtitle = p.process()
    # subtitle.print()
    subtitle.save()


if __name__ == "__main__":
    main()
