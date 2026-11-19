"""Command line interface: gama-verse [FILE] scans one poem and writes a TSV."""

from __future__ import annotations

import argparse
import csv
import sys

from . import __version__, preprocess, scan

COLUMNS = [
    "line",
    "original_text",
    "preprocessing",
    "metrical_syllables",
    "stressed_syllables",
    "no_extra_rhythmic",
    "line_type",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="gama-verse",
        description=(
            "Scan a Galician poem (one verse per line) and write the results as TSV "
            "to standard output. Reads standard input if no file is given."
        ),
    )
    parser.add_argument("file", nargs="?", help="text file with the poem")
    parser.add_argument(
        "--prepro-only",
        action="store_true",
        help="only write the preprocessed text, without scansion",
    )
    parser.add_argument("--version", action="version", version=f"gama-verse {__version__}")
    args = parser.parse_args(argv)

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    else:
        text = sys.stdin.read()

    if args.prepro_only:
        sys.stdout.write(preprocess(text))
        return 0

    writer = csv.DictWriter(sys.stdout, fieldnames=COLUMNS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(scan(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
