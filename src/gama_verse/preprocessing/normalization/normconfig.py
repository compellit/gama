"""Normalization configuration file for Galician XIX c. texts"""

import os
from pathlib import Path

# resources -------------------------------------

# The large files (language model and vocabularies) are not part of the package.
# They are read from the folder given by the GAMA_VERSE_DATA environment variable,
# or from ~/.cache/gama-verse by default (see gama-verse-download).
DATA_DIR = Path(os.environ.get("GAMA_VERSE_DATA", Path.home() / ".cache" / "gama-verse"))
IVDICO = DATA_DIR / "new_vocab_less_clitics.pkl"
IVDICO_ES = DATA_DIR / "aspell-es-expanded.txt.pkl"
LMPATH = DATA_DIR / "nos-127.klm.bin"
LANGUAGES = ("gl", "es")


# candidate generation --------------------------

# should no longer be needed to have a list for accented characters,
# this was ok for python 2 (TweetNorm task) as they needed to be treated differently to the rest
alphabet = ("bcdfghjklmnpqrstvwxyzaeiou", ["á", "é", "í", "ó", "ú", "ü", "ñ", "ç"])
accent_check_in_regexes = bool(1)

# To penalize edits that delete a vowel accent
# (consonants with diacritics like ç and ñ are not considered,
# they are not in the list of accented characters in editor.py)
# If set this to 0, it will not penalize
acc_ins_penalty = -0.5  # for now negative values penalize.

# lm scoring ------------------------------------

lm_window = 4
