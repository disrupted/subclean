#!/usr/bin/env python3
import argparse
import logging

from core.parser import SubtitleParser
from core.subtitle import Subtitle

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
    subtitle.print()
    subtitle.save()


if __name__ == "__main__":
    main()
