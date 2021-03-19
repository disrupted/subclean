# Subclean

> Simple CLI to instantly enhance your movie & TV show subtitles.

## Installation

```
pip install subclean
```

## Example

```
$ subclean subtitle.srt
12:35:30.337 | INFO | Importing subtitle subtitle.srt
12:35:30.344 | INFO | BlacklistProcessor running
12:35:30.397 | INFO | SDHProcessor running
12:35:30.421 | INFO | DialogProcessor running
12:35:30.426 | INFO | ErrorProcessor running
12:35:30.458 | INFO | LineLengthProcessor running
12:35:30.466 | INFO | Saving subtitle subtitle_clean.srt
```

![before-after](https://github.com/disrupted/subclean/blob/main/docs/img/subclean-diff.png?raw=true)

## Usage

```
subclean [-h] [-v] [-o OUTPUT]
                   [--processors {LineLength,Dialog,Blacklist,SDH,Error}
                   [--regex REGEX] [--line-length LINE_LENGTH]
                   FILE

positional arguments:
  FILE                  Subtitle file to be processed

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase output verbosity
  -o OUTPUT, --output OUTPUT
                        Set output filename
  --overwrite           Overwrite input file
  --processors {LineLength,Dialog,Blacklist,SDH,Error}
                        Processors to run
                        (default: Blacklist SDH Dialog Error LineLength)
  --regex REGEX         Add custom regular expression to BlacklistProcessor
  --line-length LINE_LENGTH
                        Maximum total line length when concatenating short lines.
                        (default: 50)
```
