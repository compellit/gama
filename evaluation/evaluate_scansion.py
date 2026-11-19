"""Evaluate gama-verse scansion against a gold standard.

Usage:
    python evaluation/evaluate_scansion.py GOLD [--metadata METADATA] [-o OUTPUT.tsv]

GOLD is a TSV or an .xlsx workbook (sheet "dataAll") with one row per line of
verse and these columns:

- ``text`` or ``origText``: the original line
- ``nbrMetSyll``: gold number of metrical syllables
- ``stressPattern``: gold stressed positions, e.g. "2 6 10"
- ``workId`` (optional): poem ID. Lines are scanned one poem at a time, so that
  the scansion context (neighbouring lines) comes from the same poem. Without
  this column, the whole file is scanned as one poem.
- ``metSylls`` (optional): gold metrical syllabification. If present, accuracy
  is also given for lines with each metrical license (synalepha, dieresis...).

The optional ``workId`` and ``metSylls`` columns can also come from a separate
METADATA file (TSV or .xlsx, same format), with the same lines in the same order.

Two measures, as in Ruiz Fabo et al. (2026):

- stress pattern accuracy: the predicted stressed positions equal the gold ones
- meter accuracy: the predicted number of metrical syllables equals the gold one

Requires pandas (and openpyxl for .xlsx), besides gama-verse.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

import gama_verse

# Metrical licenses in the gold syllabification (metSylls column)
LICENSE_FEATURES = {
    "has_synalepha": lambda m: "_" in m,
    "has_dialepha": lambda m: "÷" in m,
    "has_syneresis": lambda m: "^" in m,
    "has_dieresis": lambda m: "#" in m,
    "has_slph_across_punctuation": lambda m: re.search(r"_[,;:.!?¿¡]+_", m) is not None,
    # synalepha over a one-letter word (e.g. "de_a_o"); [^\W\d_] is a letter
    "has_complex_slph": lambda m: re.search(r"_(?:[^\W\d_]|\+)_", m) is not None,
    "has_no_diphth_across_word_b": lambda m: re.search(
        r"[aeiouáéíóúâêîôûàèìòùëïy][,;:.!?¿¡ ]* '?[aeiouáéíóúâêîôûàèìòùëïy]", m
    ) is not None,
}


def read_table(path: Path) -> pd.DataFrame:
    if path.suffix == ".xlsx":
        df = pd.read_excel(path, sheet_name="dataAll", keep_default_na=False)
    else:
        df = pd.read_csv(path, sep="\t", quoting=3, keep_default_na=False)
    return df.rename(columns={"origText": "text"})


def read_gold(path: Path, metadata_path: Path | None = None) -> pd.DataFrame:
    df = read_table(path)
    if metadata_path:
        md = read_table(metadata_path)
        assert len(md) == len(df), "gold and metadata have different numbers of lines"
        for col in ("workId", "metSylls"):
            if col in md.columns:
                df[col] = md[col].values
    if "workId" not in df.columns:
        df["workId"] = "poem"
    return df


def scan_by_poem(gold: pd.DataFrame) -> pd.DataFrame:
    """Scan each poem and return the predicted syllables and stresses, one row per line."""
    rows = []
    for _work_id, poem in gold.groupby("workId", sort=False):
        text = "\n".join(str(t).strip() for t in poem["text"])
        result = gama_verse.scan(text)
        assert len(result) == len(poem), f"{len(result)} lines scanned for {len(poem)} gold lines"
        for idx, row in zip(poem.index, result):
            rows.append(
                {
                    "idx": idx,
                    "preprocessing": row["preprocessing"],
                    "predMetSyll": str(row["metrical_syllables"]),
                    "predStressPattern": row["stressed_syllables"],
                }
            )
    return pd.DataFrame(rows).set_index("idx").sort_index()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("gold", type=Path, help="gold TSV or .xlsx (sheet dataAll)")
    parser.add_argument("--metadata", type=Path, help="workId and metSylls columns, if not in GOLD")
    parser.add_argument("-o", "--output", type=Path, help="per-line results (TSV)")
    args = parser.parse_args()

    gold = read_gold(args.gold, args.metadata)
    df = gold.join(scan_by_poem(gold))
    df["stressMatch"] = (df["predStressPattern"] == df["stressPattern"].astype(str).str.strip()).astype(int)
    df["meterMatch"] = (df["predMetSyll"] == df["nbrMetSyll"].astype(str).str.strip()).astype(int)

    total = len(df)
    print(f"Lines: {total}, poems: {df['workId'].nunique()}")
    for col, label in [("stressMatch", "Stress pattern accuracy"), ("meterMatch", "Meter accuracy")]:
        print(f"{label + ':':<26} {df[col].sum()}/{total} ({df[col].mean():.2%})")

    if "metSylls" in df.columns:
        print("\nStress pattern accuracy for lines with each metrical license:")
        for feature, test in LICENSE_FEATURES.items():
            sub = df[df["metSylls"].astype(str).map(test)]
            if len(sub):
                print(f"  {feature:<30} {sub['stressMatch'].sum():>3}/{len(sub):>3} ({sub['stressMatch'].mean():.2%})")

    if args.output:
        cols = ["workId", "text", "preprocessing", "nbrMetSyll", "predMetSyll", "meterMatch",
                "stressPattern", "predStressPattern", "stressMatch"]
        df[cols].to_csv(args.output, sep="\t", index=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
