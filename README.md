# Gama

Galician Metrical Analyzer · 🦌

Metrical scansion of Galician poetry. For each line of a poem, Gama gives the number of metrical syllables, the stressed syllables and the line type (e.g. *endecasílabo melódico puro*).

Scansion has two steps:

1. **Preprocessing**: spelling normalization (useful for texts that predate the current orthographic norm, using a KenLM language model and vocabularies) and other changes to prepare the text for scansion (e.g. identifying lexically unstressed words like most articles, using the Stanza tagger for part-of-speech cues).
2. **Scansion**: our Galician adaptation of [Jumper](https://github.com/grmarco/jumper) (Marco Remón & Gonzalo 2021).


## Installation

Requires Python 3.10 or later. Development and testing are done on Linux (on Windows, you can use WSL).

```bash
git clone https://github.com/compellit/gama
cd gama
pip install .
```

Some large files (the language model and the vocabularies, about 870 MB) are not part of the package. To download them:

```bash
gama-verse-download
```

They are saved to `~/.cache/gama-verse`. To use a different folder, set the `GAMA_VERSE_DATA` environment variable (for both the download and the analysis).

Stanza's Galician model is downloaded automatically the first time it is needed.

## Usage

### Command line

Input files have one poem each, with one line of verse per line:

```bash
gama-verse poem.txt
```

The result is a tab-separated table on standard output, with one row per line of verse. For example, for this poem fragment (`poem.txt`):

```
Aquel romor de cántigas e risas,
Ir, vir, algarear;
Aquel falar de cousas que pasaron
Y outras que pasarán;
```

| file | line | original_text | preprocessing | metrical_syllables | stressed_syllables | regular_pattern | line_type |
|---|---|---|---|---|---|---|---|
| poem.txt | 1 | Aquel romor de cántigas e risas, | Aquel romor de cántigas e risas, | 11 | 2 4 6 10 | 2 4 6 10 | Endecasílabo heroico corto |
| poem.txt | 2 | Ir, vir, algarear; | Ir, vir, algarear; | 7 | 1 2 6 | 2 6 | Heptasílabo heroico puro |
| poem.txt | 3 | Aquel falar de cousas que pasaron | Aquel falar de cousas que pasaron | 11 | 2 4 6 10 | 2 4 6 10 | Endecasílabo heroico corto |
| poem.txt | 4 | Y outras que pasarán; | E outras que pasarán; | 7 | 1 6 | 1 6 | Heptasílabo enfático |

Columns:

- `preprocessing`: the text after preprocessing, which is the input to scansion
- `metrical_syllables`: number of metrical syllables
- `stressed_syllables`: positions of the stressed syllables
- `regular_pattern`: closest regular pattern within the inventory in Jauralde Pou (2020), *Métrica española*
- `line_type`: the line type, following the classification in Jauralde (2020)

Several files can be given, and a directory stands for the `.txt` files in it:

```bash
gama-verse poems/ > scansion.tsv
```

Without a path, the poem is read from standard input. With `--prepro-only`, only the preprocessed text is written.

Loading the language model and the tagger takes a while, but it is done once per command, not once per poem, so analysing many poems in one command is much faster than one command per poem.

### Python

```python
import gama_verse

poem = "Cando penso que te fuches,\nnegra sombra que me asombras,"
for row in gama_verse.scan(poem):
    print(row["metrical_syllables"], row["stressed_syllables"], row["line_type"])

print(gama_verse.preprocess(poem))
```

`scan` returns one dict per line of verse, with the same keys as the command line columns (except `file`). The resources are loaded on the first call and reused afterwards.

## License

The scansion module (`src/gama_verse/gumper/gumper.py`) is based on Jumper, which is used with its authors' permission. The rest is licensed under GPLv3. See [LICENSE](LICENSE).

## Citation

For the implementation in this repository:

> Pablo Ruiz Fabo, Anxo Alonso Pérez, Xabier Suárez Cordero (2026). Gama: Galician Metrical Analyzer. 

For the approach:

> Pablo Ruiz Fabo, Pauline Moreau, Anxo Alonso Pérez. (2026). Automatic Metrical Scansion of Galician Poetry: First Results. *Proceedings of PROPOR - 17th International Conference on Computational Processing of Portuguese*

The version described in that paper is at [`gama-sym`](https://github.com/compellit/gama-sym). This package contains a later version of the code, the one used by the web interface at https://prf2.org/galapagos/.