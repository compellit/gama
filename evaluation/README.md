# Evaluation

`evaluate_scansion.py` evaluates Gama's scansion against a manually annotated test set. It reports per-line accuracy in exact stress-pattern match and meter match (number of metrical syllables), and stress-pattern accuracy for lines with each metrical license (synalepha, dialepha, syneresis, dieresis...).

Each poem is preprocessed and scanned separately, with `gama_verse.scan()`, so the scansion context (neighbouring lines) comes from the same poem.

## Test data

The test data are not in this repository. They can be shared upon request. A small amount of the material comes from unpublished editions of 19th-century text. We accessed these data under a reuse agreement with the data owners which does not allow us to redistribute publicly.

The test set has 800 lines from 34 poems. The annotation criteria are described in [`gama-sym`](https://github.com/compellit/gama-sym/blob/main/src/scansion/eval/data/annotation-criteria.md).

Two files are needed:

- `gl_scansion_gold_test_010_corr.tsv`: one row per line, with columns `text` (original line), `nbrMetSyll` (number of metrical syllables) and `stressPattern` (stressed positions, e.g. `2 6 10`)
- `merged_df_test_010.tsv`: the same lines in the same order, with poem IDs (`workId`), metrical syllabification with license annotations (`metSylls`) and other metadata

## Reproducing the published results

After installing `gama-verse` and downloading its data (see the main [README](../README.md)), run from the repository root:

```bash
python evaluation/evaluate_scansion.py gl_scansion_gold_test_010_corr.tsv --metadata merged_df_test_010.tsv -o scansion_eval.tsv
```

The script needs `pandas`, besides `gama-verse`. With `-o`, the per-line results are written to a TSV file.

Output:

```
Lines: 800, poems: 34
Stress pattern accuracy:   705/800 (88.12%)
Meter accuracy:            779/800 (97.38%)

Stress pattern accuracy for lines with each metrical license:
  has_synalepha                  337/397 (84.89%)
  has_dialepha                    26/ 32 (81.25%)
  has_syneresis                   27/ 36 (75.00%)
  has_dieresis                     3/  6 (50.00%)
  has_slph_across_punctuation     27/ 30 (90.00%)
  has_complex_slph                10/ 12 (83.33%)
  has_no_diphth_across_word_b     19/ 24 (79.17%)
```

These are the results of the best configuration on the test set in Ruiz Fabo, Moreau and Alonso Pérez (2026), Table 1 (88.1% stress-pattern match, 97.4% meter match). The predicted stress pattern is the same as in that evaluation for each of the 800 lines.

The same system and test set are used as the symbolic baseline in Ruiz Fabo, Alonso Pérez, Rodríguez Fernández and Gamallo (2026). The stress-pattern accuracy there, 89.88% (Table 3), was obtained after correcting preprocessing errors by hand; without the corrections, it is 88.12% (Section 6), as above. The meter accuracy, 97.38%, is the same in both cases. The results per metrical license (Table 4) are also the same as above.

## References

Pablo Ruiz Fabo, Pauline Moreau, Anxo Alonso Pérez. (2026). Automatic Metrical Scansion of Galician Poetry: First Results. *Proceedings of PROPOR - 17th International Conference on Computational Processing of Portuguese*.

Pablo Ruiz Fabo, Anxo Alonso Pérez, Pablo Rodríguez Fernández, Pablo Gamallo. (2026). Automatic Metrical Scansion of Poetry in a Low-Resource Setting. In *Proceedings of Shaping Multilingual, Multimodal AI for the Social Sciences and Humanities (LLMs4SSH) @ LREC 2026*, pp. 114–125. ELRA. https://doi.org/10.63317/4pzd6u7388jm
