from __future__ import annotations

import argparse

from subclean.processors.processor import DEFAULT_PROCESSORS, Processors

from . import __version__


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean Subtitles")
    parser.add_argument(
        "file",
        nargs="+",
        metavar="FILE",
        type=argparse.FileType("r"),
        help="Subtitle file to be processed",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        help="Increase output verbosity",
        dest="log_level",
        const="DEBUG",
        default="INFO",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s " + __version__,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-o", "--output", type=str, help="Set output filename")
    group.add_argument("--overwrite", action="store_true", help="Overwrite input file")
    parser.add_argument(
        "--processors",
        nargs="+",
        type=lambda processor: Processors[processor],
        choices=set(Processors),
        help=f"Processors to run (default: {' '.join([processor.name for processor in DEFAULT_PROCESSORS])})",
        default=DEFAULT_PROCESSORS,
    )
    parser.add_argument(
        "--regex", type=str, help="Add custom regular expression to BlacklistProcessor"
    )
    parser.add_argument(
        "--line-length",
        type=int,
        help="Maximum total line length when concatenating short lines. (default: 50)",
    )
    return parser.parse_args(args)
