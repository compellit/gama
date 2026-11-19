"""Command line interface: gama-verse [PATH ...] scans poems and writes a TSV.

Each file is one poem. A directory stands for the .txt files in it.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from . import __version__, preprocess, scan

COLUMNS = [
    "file",
    "line",
    "original_text",
    "preprocessing",
    "metrical_syllables",
    "stressed_syllables",
    "no_extra_rhythmic",
    "line_type",
]


def input_files(paths: list[str]) -> list[Path]:
    """Return the files to process: directories are replaced by their .txt files."""
    files = []
    for path in map(Path, paths):
        if path.is_dir():
            files.extend(sorted(path.glob("*.txt")))
        else:
            files.append(path)
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="gama-verse",
        description=(
            "Scan Galician poems (one verse per line, one poem per file) and write the "
            "results as TSV to standard output. A directory stands for the .txt files "
            "in it. Reads standard input if no path is given."
        ),
    )
    parser.add_argument("paths", nargs="*", help="text files with one poem each, or directories")
    parser.add_argument(
        "--prepro-only",
        action="store_true",
        help="only write the preprocessed text, without scansion",
    )
    parser.add_argument("--version", action="version", version=f"gama-verse {__version__}")
    args = parser.parse_args(argv)

    if args.paths:
        poems = [(str(f), f.read_text(encoding="utf-8")) for f in input_files(args.paths)]
    else:
        poems = [("-", sys.stdin.read())]

    if args.prepro_only:
        for _name, text in poems:
            sys.stdout.write(preprocess(text))
        return 0

    writer = csv.DictWriter(sys.stdout, fieldnames=COLUMNS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for name, text in poems:
        for row in scan(text):
            writer.writerow({"file": name, **row})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
