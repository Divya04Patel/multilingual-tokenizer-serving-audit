from pathlib import Path
import tiktoken
from transformers import AutoTokenizer

LANGUAGES = {
    "eng": "eng_Latn.dev",
    "hin": "hin_Deva.dev",
    "kan": "kan_Knda.dev",
    "tam": "tam_Taml.dev",
}

CORPUS_DIR = Path("partA/corpus/flores200_dev")

gpt2 = tiktoken.get_encoding("gpt2")
xlmr = AutoTokenizer.from_pretrained("xlm-roberta-base")


def fertility(lines, encode):
    total_tokens = 0
    total_words = 0

    for line in lines:
        line = line.lower()
        total_tokens += len(encode(line))
        total_words += len(line.split())

    return total_tokens / total_words


def gpt2_encode(text):
    return gpt2.encode(text)


def xlmr_encode(text):
    return xlmr.encode(text, add_special_tokens=False)


print("language    GPT-2    XLM-R")
print("--------------------------")

for lang, filename in LANGUAGES.items():
    path = CORPUS_DIR / filename
    lines = path.read_text(encoding="utf-8").splitlines()

    gpt2_fertility = fertility(lines, gpt2_encode)
    xlmr_fertility = fertility(lines, xlmr_encode)

    print(f"{lang:<10} {gpt2_fertility:>6.3f}   {xlmr_fertility:>6.3f}")