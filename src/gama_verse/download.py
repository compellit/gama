"""gama-verse-download: download the large files (language model and vocabularies).

They are saved to the folder given by GAMA_VERSE_DATA, or ~/.cache/gama-verse.
"""

from __future__ import annotations

import sys
import urllib.request

from .preprocessing.normalization import normconfig

BASE_URL = "https://huggingface.co/compellit/gama-verse-data/resolve/main/"
FILES = [normconfig.LMPATH.name, normconfig.IVDICO.name, normconfig.IVDICO_ES.name]


def main() -> int:
    normconfig.DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        target = normconfig.DATA_DIR / name
        if target.exists():
            print(f"{target} already exists, skipped")
            continue
        print(f"Downloading {name} to {normconfig.DATA_DIR} ...")
        partial = target.with_name(name + ".part")
        urllib.request.urlretrieve(BASE_URL + name, partial)
        partial.rename(target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
