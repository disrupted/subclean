#!/bin/bash
# useful to diff the contents of 2 SRT subtitle files

if [ ! -s "$1" ] || [ ! -s "$2" ] || [ "$1" == "$2" ]; then
    echo "usage: subdiff file1.srt file2.srt"
    exit 1
fi

_read_file() {
    rg '[^\d]|^\s*$' "$1"
}

diff -u <(_read_file "$1") <(_read_file "$2") | delta -s --wrap-max-lines unlimited

exit 0
