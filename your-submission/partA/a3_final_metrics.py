from pathlib import Path
import unicodedata
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


def count_metrics(lines, encode):
    total_tokens = 0
    total_words = 0

    for line in lines:
        line = unicodedata.normalize("NFC", line).lower()
        total_tokens += len(encode(line))
        total_words += len(line.split())

    return total_tokens, total_words


def gpt2_encode(text):
    return gpt2.encode(text)


def xlmr_encode(text):
    return xlmr.encode(text, add_special_tokens=False)


print("A3 FINAL METRICS")
print()
print("language tokenizer total_tokens total_words tok_per_word tok_per_sentence")
print("--------------------------------------------------------------------------")

for lang, filename in LANGUAGES.items():
    path = CORPUS_DIR / filename
    lines = path.read_text(encoding="utf-8").splitlines()

    for tokenizer_name, encode in [
        ("GPT-2", gpt2_encode),
        ("XLM-R", xlmr_encode),
    ]:
        total_tokens, total_words = count_metrics(lines, encode)

        tok_per_word = total_tokens / total_words
        tok_per_sentence = total_tokens / len(lines)

        print(
            f"{lang:<8} "
            f"{tokenizer_name:<9} "
            f"{total_tokens:>11} "
            f"{total_words:>11} "
            f"{tok_per_word:>11.3f} "
            f"{tok_per_sentence:>16.2f}"
        )