from pathlib import Path
import unicodedata

LANGUAGES = {
    "eng": "eng_Latn.dev",
    "hin": "hin_Deva.dev",
    "kan": "kan_Knda.dev",
    "tam": "tam_Taml.dev",
}

CORPUS_DIR = Path("partA/corpus/flores200_dev")

for lang, filename in LANGUAGES.items():
    path = CORPUS_DIR / filename
    lines = path.read_text(encoding="utf-8").splitlines()

    changed = 0

    for line in lines:
        if unicodedata.normalize("NFC", line) != line:
            changed += 1

    print(f"{lang}: {changed}/{len(lines)} lines changed by NFC")