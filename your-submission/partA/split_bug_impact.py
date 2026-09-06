from pathlib import Path
import tiktoken

LANGUAGES = {
    "eng": "eng_Latn.dev",
    "hin": "hin_Deva.dev",
    "kan": "kan_Knda.dev",
    "tam": "tam_Taml.dev",
}

CORPUS_DIR = Path("partA/corpus/flores200_dev")
tokenizer = tiktoken.get_encoding("gpt2")


def calculate(lines, use_buggy_split):
    total_tokens = 0
    total_words = 0

    for line in lines:
        line = line.lower()
        total_tokens += len(tokenizer.encode(line))

        if use_buggy_split:
            total_words += len(line.split(" "))
        else:
            total_words += len(line.split())

    return total_tokens / total_words, total_words


print("language  old_fertility  fixed_fertility  change_pct  old_words  fixed_words")
print("----------------------------------------------------------------------------")

for lang, filename in LANGUAGES.items():
    path = CORPUS_DIR / filename
    lines = path.read_text(encoding="utf-8").splitlines()

    old_fertility, old_words = calculate(lines, True)
    fixed_fertility, fixed_words = calculate(lines, False)

    change_pct = (fixed_fertility / old_fertility - 1) * 100

    print(
        f"{lang:<9}"
        f"{old_fertility:>13.3f}"
        f"{fixed_fertility:>16.3f}"
        f"{change_pct:>12.2f}%"
        f"{old_words:>11}"
        f"{fixed_words:>12}"
    )