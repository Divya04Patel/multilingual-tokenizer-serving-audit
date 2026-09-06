\# Part A2 — Tokenizer Audit



\## Dataset



FLORES-200 dev, using 997 aligned sentences for:

\- English (`eng\_Latn`)

\- Hindi (`hin\_Deva`)

\- Kannada (`kan\_Knda`)

\- Tamil (`tam\_Taml`)



Preprocessing follows the starter script: UTF-8 decoding, NFC normalization,

lowercasing, and non-empty lines.



\## Finding 1 — Real code bug: `split(" ")`



The starter code uses `line.split(" ")` to count words. Repeated spaces

therefore create empty strings and inflate the denominator.



Experiment:



&#x20;   python partA\\split\_bug\_impact.py



Measured GPT-2 fertility on the full FLORES-200 dev corpus:



| Language | Buggy | Fixed | Change |

|---|---:|---:|---:|

| English | 1.274 | 1.274 | 0.00% |

| Hindi | 7.779 | 7.787 | +0.11% |

| Kannada | 21.450 | 22.686 | +5.76% |

| Tamil | 24.465 | 24.619 | +0.63% |



Kannada is most affected: 16,319 words with the buggy split versus

15,430 with `split()`, producing a 5.76% fertility change.



Conclusion: this is a genuine implementation bug, but its magnitude is

language/corpus dependent.



\## Finding 2 — Conceptual problem: denominator changes the headline



"Tokens per character" in the starter code is actually tokens per Unicode

code point because Python's `len(str)` counts Unicode code points.



On the FLORES corpus, GPT-2 produced:



| Language | tok/codepoint | tok/grapheme | tok/byte |

|---|---:|---:|---:|

| English | 0.213 | 0.213 | 0.213 |

| Hindi | 1.529 | 2.328 | 0.595 |

| Kannada | 2.653 | 4.052 | 0.979 |

| Tamil | 2.718 | 4.205 | 0.996 |



These are different measurements, not interchangeable definitions of

"tokenization cost."



Therefore the original `tok/char` column should not be presented as a

universal language-neutral serving-cost metric.



\## Finding 3 — Tokenizer choice materially changes the conclusion



We compared GPT-2 with XLM-R using the same 997-sentence corpus and the

same corrected word denominator.



| Language | GPT-2 tok/word | XLM-R tok/word |

|---|---:|---:|

| English | 1.274 | 1.408 |

| Hindi | 7.797 | 1.489 |

| Kannada | 22.683 | 2.568 |

| Tamil | 24.618 | 2.424 |



Relative to English, GPT-2 gives approximately 6.12x Hindi, 17.80x Kannada,

and 19.32x Tamil fertility. XLM-R gives approximately 1.06x, 1.82x, and

1.72x respectively.



This directly contradicts the v0 claim that Indic difficulty is simply

a property of the script. Tokenizer design has a very large effect.



\## Finding 4 — Suspicious-looking preprocessing step that is fine



The starter applies NFC Unicode normalization.



Experiment:



&#x20;   python partA\\check\_nfc.py

&#x20;   python partA\\check\_nfc\_impact.py



NFC changed 0/997 English lines, 90/997 Hindi lines, 10/997 Kannada lines,

and 2/997 Tamil lines.



GPT-2 token totals changed by:

\- English: 0

\- Hindi: +239 tokens

\- Kannada: -51 tokens

\- Tamil: -6 tokens



NFC is therefore not a bug merely because it changes some Unicode

representations. It is a defensible normalization step, and its measured

token-count impact is small relative to the overall corpus.



\## Assessment of REPORT\_v0



The statement that the tok/char metric "agrees" with fertility is not

supported: on the original sample, the Hindi/English ratios were 5.89x

by fertility versus 7.00x by code point.



More importantly, the statement that Hindi's tokenization problem is

caused by its script and that "any tokenizer will struggle" is not

supported by the tokenizer comparison above.



The recommendation to budget approximately 6x serving cost for Hindi

cannot be justified from this benchmark alone.

