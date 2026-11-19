from pathlib import Path

# base dir = dossier où est ce fichier config.py
BASE_DIR = Path(__file__).resolve().parent

# data

word_bound_replacements = BASE_DIR / "data" / "replacements_w.txt"
text_level_replacements = BASE_DIR / "data" / "replacements_t.txt"

# IO
oudir = Path("out")
oufi = oudir / "scansion.tsv"
logdir = Path("logs")
indir = Path("input")

