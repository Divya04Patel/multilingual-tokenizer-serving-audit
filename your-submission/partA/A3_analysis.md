\# Part A3 — Corrected Cross-Language Comparison



\## Evaluation setup



Corpus: FLORES-200 dev, 997 aligned sentences each for English, Hindi,

Kannada, and Tamil.



Tokenizers:

\- GPT-2 (`tiktoken` gpt2)

\- XLM-R (`xlm-roberta-base`)



The same corpus, preprocessing, and sentence alignment are used for both

tokenizers. Word counting uses Python `split()` rather than the buggy

`split(" ")`.



\## Corrected results



\### Tokens per word



| Language | GPT-2 | XLM-R |

|---|---:|---:|

| English | 1.274 | 1.408 |

| Hindi | 7.797 | 1.489 |

| Kannada | 22.683 | 2.568 |

| Tamil | 24.618 | 2.424 |



\### Tokens per aligned sentence



| Language | GPT-2 | XLM-R |

|---|---:|---:|

| English | 26.78 | 29.58 |

| Hindi | 192.43 | 36.75 |

| Kannada | 351.05 | 39.74 |

| Tamil | 398.38 | 39.23 |



\### Relative to English



| Language | GPT-2 sentence ratio | XLM-R sentence ratio |

|---|---:|---:|

| Hindi | 7.19x | 1.24x |

| Kannada | 13.11x | 1.34x |

| Tamil | 14.88x | 1.33x |



\## Interpretation



Tokenizer choice dominates the result.



GPT-2 produces extremely high token counts for the Dravidian languages,

especially Kannada and Tamil. XLM-R produces much smaller cross-language

differences.



Importantly, XLM-R is not simply better because it produces fewer tokens

for every language: its English token/word value is higher than GPT-2's

(1.408 versus 1.274). Its advantage is specifically its much more balanced

multilingual tokenization.



Therefore the original report's conclusion that Indic tokenization

difficulty is primarily an inherent property of the script is not supported.



\## Which single number should drive routing/cost?



For this benchmark, use \*\*tokens per aligned sentence\*\* rather than

tokens per word or tokens per character as the primary cross-language

comparison.



Reason:



1\. The FLORES sentences are translations of aligned source material.

2\. Every language therefore has the same number of benchmark sentences.

3\. Word boundaries and character representations vary substantially

&#x20;  across languages and scripts.

4\. Tokens per sentence directly measures how many model tokens the same

&#x20;  translated unit consumes.



For actual production routing and capacity planning, the final operational

metric should be \*\*actual input/output tokens per request on the target

model\*\*, together with measured latency and cost. The benchmark's

tokens-per-sentence value is a controlled proxy, not a substitute for

production telemetry.



\## Routing implication



Do not route Indic traffic based on the v0 claim of "6x Hindi cost."



The benchmark shows that the tokenizer/model combination is the major

driver. An Indic/multilingual tokenizer can reduce the apparent

cross-language token expansion dramatically.



A routing decision should therefore be based on measured production

tokens/request and serving performance for the actual model/tokenizer pair,

rather than on Unicode character counts or a single English-vs-Hindi

fertility ratio.



\## Main caveat



GPT-2 and XLM-R are different tokenizer/model families, so their absolute

token counts should not be interpreted as a direct prediction of serving

cost across different models.



The comparison demonstrates tokenizer sensitivity and cross-language

tokenization behavior. Production cost must be measured using the tokenizer

and model actually deployed.



