#!/usr/bin/env python3
import argparse

from core.parser import SubtitleParser
from core.subtitle import Subtitle
from processors.processor import Processors

DEFAULT_PROCESSORS = [
    Processors.Blacklist,
    Processors.SDH,
    Processors.Dialog,
    Processors.Error,
]


def main():
    argparser = argparse.ArgumentParser(description="Clean Subtitles")
    argparser.add_argument(
        "file",
        metavar="FILE",
        type=argparse.FileType("r"),
        help="Subtitle file to be processed",
    )
    argparser.add_argument(
        "-v", "--verbose", action="store_true", help="Increase output verbosity"
    )
    argparser.add_argument("-o", "--output", type=str, help="Set output filename")
    argparser.add_argument(
        "--processors",
        nargs="+",
        type=lambda processor: Processors[processor],
        choices=set(Processors),
        help="Processors to run",
        default=DEFAULT_PROCESSORS,
    )
    args = argparser.parse_args()

    subtitle: Subtitle = SubtitleParser.load(args.file.name)
    processors = [processor.value for processor in args.processors]
    for processor in processors:
        subtitle = processor(subtitle).process()
    subtitle.save(output_filepath=args.output)


if __name__ == "__main__":
    main()
