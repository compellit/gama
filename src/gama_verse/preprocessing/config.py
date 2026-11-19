# Syllabification configuration file

from pathlib import Path

# IO

config_dir = Path(__file__).resolve().parent
data_dir = config_dir / "data"

text_level_replacements = data_dir / "replacements_text.tsv"
syllable_replacements = data_dir / "syllabification_postprocessing.tsv"
syllable_replacements_for_g2s = data_dir / "syllabification-exceptions.lst"
words_with_hyphen_to_keep = data_dir / "hyphens_to_keep.txt"  # unused

batch_cumulog = "batch_log.txt"
