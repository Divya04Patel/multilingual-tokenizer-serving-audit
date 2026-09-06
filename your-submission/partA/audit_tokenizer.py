from pathlib import Path
import unicodedata
import tiktoken
import regex
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


def load_lines(filename):
    return (
        (CORPUS_DIR / filename)
        .read_text(encoding="utf-8")
        .splitlines()
    )


def count_tokens(tokenizer, text):
    if tokenizer == "GPT-2":
        return len(gpt2.encode(text))
    return len(xlmr.encode(text, add_special_tokens=False))


def analyze(lines, tokenizer):
    total_tokens = 0
    total_words = 0
    total_codepoints = 0
    total_graphemes = 0
    total_bytes = 0

    for line in lines:
        line = unicodedata.normalize("NFC", line.lower())

        total_tokens += count_tokens(tokenizer, line)
        total_words += len(line.split())
        total_codepoints += len(line)
        total_graphemes += len(regex.findall(r"\X", line))
        total_bytes += len(line.encode("utf-8"))

    n = len(lines)

    return {
        "tokens": total_tokens,
        "words": total_words,
        "sentences": n,
        "tok_per_word": total_tokens / total_words,
        "tok_per_sentence": total_tokens / n,
        "tok_per_codepoint": total_tokens / total_codepoints,
        "tok_per_grapheme": total_tokens / total_graphemes,
        "tok_per_byte": total_tokens / total_bytes,
    }


print("TOKENIZER AUDIT — FLORES-200 DEV")
print()
print("All languages: 997 aligned sentences")
print("Word denominator: corrected split()")
print()

print(
    "language tokenizer tokens words "
    "tok/word tok/sentence tok/codepoint tok/grapheme tok/byte"
)
print("-" * 85)

for lang, filename in LANGUAGES.items():
    lines = load_lines(filename)

    for tokenizer in ["GPT-2", "XLM-R"]:
        r = analyze(lines, tokenizer)

        print(
            f"{lang:<8} "
            f"{tokenizer:<9} "
            f"{r['tokens']:>8} "
            f"{r['words']:>8} "
            f"{r['tok_per_word']:>8.3f} "
            f"{r['tok_per_sentence']:>12.2f} "
            f"{r['tok_per_codepoint']:>14.3f} "
            f"{r['tok_per_grapheme']:>13.3f} "
            f"{r['tok_per_byte']:>9.3f}"
        )