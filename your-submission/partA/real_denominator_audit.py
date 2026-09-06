from pathlib import Path
import tiktoken
import regex

LANGUAGES = {
    "eng": "eng_Latn.dev",
    "hin": "hin_Deva.dev",
    "kan": "kan_Knda.dev",
    "tam": "tam_Taml.dev",
}

CORPUS_DIR = Path("partA/corpus/flores200_dev")

tokenizer = tiktoken.get_encoding("gpt2")


def analyze(lines):
    total_tokens = 0
    total_codepoints = 0
    total_graphemes = 0
    total_bytes = 0

    for line in lines:
        line = line.lower()
        total_tokens += len(tokenizer.encode(line))
        total_codepoints += len(line)
        total_graphemes += len(regex.findall(r"\X", line))
        total_bytes += len(line.encode("utf-8"))

    return (
        total_tokens / total_codepoints,
        total_tokens / total_graphemes,
        total_tokens / total_bytes,
    )


print("language    tok/codepoint    tok/grapheme    tok/byte")
print("------------------------------------------------------")

for lang, filename in LANGUAGES.items():
    path = CORPUS_DIR / filename
    lines = path.read_text(encoding="utf-8").splitlines()

    codepoint, grapheme, byte = analyze(lines)

    print(f"{lang:<10} {codepoint:>13.3f} {grapheme:>14.3f} {byte:>10.3f}")