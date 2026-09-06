\# Part A — Leadership Memo: Tokenizer Audit



\## Executive finding



The original tokenizer report should not be used for routing or capacity

decisions. Its "6x Hindi cost" conclusion is driven by a narrow toy corpus,

a flawed word-count implementation, and metrics whose denominators vary

substantially across languages.



On 997 aligned FLORES-200 dev sentences:



| Language | GPT-2 tok/sentence | XLM-R tok/sentence |

|---|---:|---:|

| English | 26.78 | 29.58 |

| Hindi | 192.43 | 36.75 |

| Kannada | 351.05 | 39.74 |

| Tamil | 398.38 | 39.23 |



Relative to English, GPT-2 expands to 7.19x Hindi, 13.11x Kannada and

14.88x Tamil. XLM-R reduces these ratios to 1.24x, 1.34x and 1.33x.



This shows that tokenizer design, not script alone, is a major determinant

of multilingual token expansion.



\## Audit findings



The starter code uses `split(" ")`, which counts empty strings created by

repeated spaces. On the full corpus this changed GPT-2 fertility by 5.76%

for Kannada, versus 0.11% Hindi, 0.63% Tamil and 0.00% English.



The reported "tok/char" metric is actually tokens per Unicode code point.

On the same corpus, GPT-2 Hindi is 1.529 tok/codepoint but 2.328

tok/grapheme and 0.595 tok/byte. These are different measurements and

should not be treated as interchangeable cost metrics.



The NFC normalization step is defensible rather than a bug. Its measured

token-count effect was small relative to the corpus: +239 Hindi tokens,

\-51 Kannada tokens and -6 Tamil tokens, with no English change.



\## Routing recommendation



Do \*\*not\*\* route Indic traffic or allocate capacity using the original

"6x Hindi" number.



Select the tokenizer/model combination using measured production

performance. The audit strongly favors evaluating multilingual/Indic-aware

tokenization because XLM-R dramatically reduces cross-language token

expansion relative to GPT-2.



For controlled benchmarking, tokens per aligned sentence is the preferred

cross-language denominator because the sentences are parallel. It should

not, however, be interpreted as a direct production-cost estimate.



\## Production metric



The primary production metric should be:



\*\*input tokens/request + output tokens/request, segmented by language,

model/tokenizer, and workload type.\*\*



Pair this with \*\*p50/p95 latency and cost per request\*\*. This directly

measures the quantities that affect capacity and customer cost.



\## Biggest caveat



GPT-2 and XLM-R are different model/tokenizer families. Their absolute

token counts therefore cannot be converted directly into a model-cost

comparison. The tokenizer audit establishes that the original conclusion

is not robust; final routing decisions require measurement on the actual

deployed model and serving stack.

