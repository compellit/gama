"""gama-verse: metrical scansion of Galician poetry (GAMA, Galician Metrical Analyzer).

Two steps:

- :func:`preprocess` normalizes the spelling (useful for texts that predate the
  current orthographic norm) and prepares the text for scansion.
- :func:`scan` preprocesses the text and runs Gumper, our Galician adaptation of
  Jumper (Marco Remón & Gonzalo 2021), on it.

The language model, the vocabularies and the stanza tagger are loaded once per
Python process, by :func:`load_resources`, on the first call.
"""

from __future__ import annotations

import functools
from types import SimpleNamespace

__version__ = "0.1.0"
__all__ = ["load_resources", "preprocess", "scan"]


@functools.lru_cache(maxsize=None)
def load_resources() -> SimpleNamespace:
    """Load the language model, the vocabularies and the stanza tagger.

    The first call loads them (this takes a while) and later calls return the
    same objects, so they are loaded only once per Python process.
    """
    import stanza
    from stanza import DownloadMethod

    from .preprocessing.normalization import lm_manager, normalizer
    from .preprocessing.normalization import normconfig as ncf

    return SimpleNamespace(
        nglm=lm_manager.KenLMManager(),
        nlp=stanza.Pipeline(
            lang="gl",
            package="treegal",
            processors="tokenize,pos",
            download_method=DownloadMethod.REUSE_RESOURCES,
        ),
        nmlzr=normalizer.Normalizer(ncf),
        nmlzr_es=normalizer.Normalizer(ncf, lang="es"),
    )


def preprocess(text: str) -> str:
    """Preprocess a poem (one line per verse) for scansion.

    Uses the same settings as the GAMA web app: orthographic preprocessing,
    normalization, destressing of unstressed words, Spanish-word handling and
    possessives.
    """
    from .preprocessing.prepro import scansion_prepro_main

    res = load_resources()
    outstr, *_ = scansion_prepro_main(
        text,
        None,
        res.nglm,
        res.nlp,
        res.nmlzr,
        res.nmlzr_es,
        preprocess=True,
        destress=True,
        spanishfy=True,
        possessives=True,
        batch_id="001",
        normalize=True,
    )
    return outstr


def scan(text: str) -> list[dict]:
    """Preprocess a poem and scan it. Returns one dict per line.

    Keys: ``line``, ``original_text``, ``preprocessing``, ``metrical_syllables``,
    ``stressed_syllables``, ``regular_pattern`` (stressed syllables without
    extrarhythmic stresses) and ``line_type``.
    """
    from .gumper import client
    from .gumper import config as gcf

    _raw, _html, results = client.main(gcf, text, preprocess(text))
    return results
