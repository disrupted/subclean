import argparse
import logging
import sys
from collections.abc import Sequence
from pathlib import Path

from subclean import __version__, io
from subclean.formats import UnsupportedFormatError
from subclean.processors import PROCESSORS, Options, Processor, build, run

logger = logging.getLogger("subclean")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="subclean", description="Clean subtitles")
    parser.add_argument(
        "files", nargs="+", metavar="FILE", type=Path, help="subtitle file to process"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity"
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    output = parser.add_mutually_exclusive_group()
    output.add_argument(
        "-o", "--output", type=Path, help="output file (single input only)"
    )
    output.add_argument("--overwrite", action="store_true", help="overwrite input file")
    parser.add_argument(
        "--processors",
        nargs="+",
        choices=list(PROCESSORS),
        default=list(PROCESSORS),
        metavar="NAME",
        help=f"processors to run, in order (default: {' '.join(PROCESSORS)})",
    )
    parser.add_argument(
        "--regex",
        action="append",
        default=[],
        help="additional blacklist regex, can be repeated",
    )
    parser.add_argument(
        "--line-length",
        type=int,
        default=Options().max_line_length,
        help="maximum length when merging short lines (default: %(default)s)",
    )
    args = parser.parse_args(argv)
    if args.output and len(args.files) > 1:
        parser.error("--output can only be used with a single input file")
    return args


def output_path(path: Path, args: argparse.Namespace) -> Path:
    if args.overwrite:
        return path
    return args.output or path.with_stem(f"{path.stem}_clean")


def clean_file(
    path: Path, output: Path, processors: Sequence[tuple[str, Processor]]
) -> None:
    io.save(output, run(io.load(path), processors))


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stderr,
    )
    processors = build(
        args.processors,
        Options(extra_patterns=tuple(args.regex), max_line_length=args.line_length),
    )
    failed = False
    for path in args.files:
        try:
            clean_file(path, output_path(path, args), processors)
        except (OSError, UnsupportedFormatError) as e:
            logger.error("%s: %s", path, e)
            failed = True
    if failed:
        sys.exit(1)
