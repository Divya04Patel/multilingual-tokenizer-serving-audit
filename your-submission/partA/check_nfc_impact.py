from pathlib import Path
import unicodedata
import tiktoken

LANGUAGES = {
    "eng": "eng_Latn.dev",
    "hin": "hin_Deva.dev",
    "kan": "kan_Knda.dev",
    "tam": "tam_Taml.dev",
}

CORPUS_DIR = Path("partA/corpus/flores200_dev")
tokenizer = tiktoken.get_encoding("gpt2")

for lang, filename in LANGUAGES.items():
    path = CORPUS_DIR / filename
    lines = path.read_text(encoding="utf-8").splitlines()

    raw_tokens = 0
    nfc_tokens = 0
    changed_token_lines = 0

    for line in lines:
        raw_count = len(tokenizer.encode(line.lower()))
        nfc_line = unicodedata.normalize("NFC", line)
        nfc_count = len(tokenizer.encode(nfc_line.lower()))

        raw_tokens += raw_count
        nfc_tokens += nfc_count

        if raw_count != nfc_count:
            changed_token_lines += 1

    print(
        f"{lang}: raw_tokens={raw_tokens}, "
        f"nfc_tokens={nfc_tokens}, "
        f"token_diff={nfc_tokens - raw_tokens}, "
        f"lines_with_token_change={changed_token_lines}"
    )