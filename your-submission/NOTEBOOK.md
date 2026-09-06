\# The Audit - Lab Notebook



\## Purpose



Audit the starter tokenizer and serving benchmark before using its

conclusions for routing or capacity decisions.



The notebook records the main hypotheses, experiments, measured results,

and revisions. Proposed values are explicitly separated from measured

results.



\---



\# Part A - Tokenizer Audit



\## A0 - Reproduce the starter result



\### Hypothesis



The starter benchmark's Hindi fertility result should reproduce from the

provided script and sample corpus.



\### Experiment



Command:



&#x20;   python fertility.py --corpus eng=corpus\_sample/eng\_sample.txt --corpus hin=corpus\_sample/hin\_sample.txt --tokenizer gpt2



\### Result



Starter output:



\- English fertility: 1.27 tok/word

\- Hindi fertility: 7.45 tok/word

\- Hindi/English fertility ratio: 5.89x



\### Revision



The result reproduced, but reproduction alone does not establish that the

metric is suitable for routing or cost decisions. I next audited the

implementation and denominator.



\---



\## A1 - Audit whitespace word counting



\### Hypothesis



`split(" ")` may incorrectly count multiple consecutive spaces as empty

words.



\### Experiment



Compared the starter calculation using `split(" ")` against Python

`split()` on the starter sample.



\### Result



English:



\- old fertility: 1.265206

\- corrected fertility: 1.283063

\- change: +1.41%

\- word count: 79 -> 78



Hindi:



\- old fertility: 7.448452

\- corrected fertility: 7.598452

\- change: +2.01%

\- word count: 62 -> 61



\### Revision



This is a genuine implementation bug, although its effect on the toy

corpus is small. I then tested whether the effect changes on a larger

multilingual corpus.



\---



\## A2 - Build a real multilingual evaluation corpus



\### Hypothesis



The 10-line English/Hindi sample is too small to support a multilingual

routing decision.



\### Experiment



Used the FLORES-200 dev split with 997 aligned sentences for:



\- English (`eng\_Latn`)

\- Hindi (`hin\_Deva`)

\- Kannada (`kan\_Knda`)

\- Tamil (`tam\_Taml`)



The files were checked for UTF-8 validity, blank lines, and alignment.



\### Result



All four files contain 997 lines. The corpus provides two Dravidian

languages as required by the assignment.



Raw-corpus hygiene observations included repeated internal spaces,

especially in Kannada, which makes the whitespace bug worth testing on

the real corpus.



\### Revision



Use FLORES-200 rather than the starter toy corpus for the corrected

comparison.



\---



\## A3 - Measure the whitespace bug on FLORES-200



\### Hypothesis



The `split(" ")` bug may have a larger effect when the corpus contains

more repeated spaces.



\### Experiment



Compared buggy `split(" ")` and corrected `split()` on all four FLORES

files.



\### Result



| Language | Buggy fertility | Fixed fertility | Change |

|---|---:|---:|---:|

| English | 1.274 | 1.274 | 0.00% |

| Hindi | 7.779 | 7.787 | +0.11% |

| Kannada | 21.450 | 22.686 | +5.76% |

| Tamil | 24.465 | 24.619 | +0.63% |



Kannada word count changed from 16,319 to 15,430.



\### Revision



The bug is real and language/corpus dependent. Kannada's 5.76% change

is large enough that corrected splitting must be used for the final

comparison.



\---



\## A4 - Audit the denominator



\### Hypothesis



`tok/char` may not be a universally comparable notion of character

cost.



\### Experiment



Measured GPT-2 token counts using:



\- Unicode code points

\- Unicode grapheme clusters

\- UTF-8 bytes



on the starter sample.



\### Result



| Language | tok/codepoint | tok/grapheme | tok/byte |

|---|---:|---:|---:|

| English | 0.225636 | 0.225636 | 0.225636 |

| Hindi | 1.579108 | 2.449732 | 0.598992 |



Hindi/English ratio:



\- code point: about 7.00x

\- grapheme: about 10.86x

\- byte: about 2.66x



\### Revision



The denominator materially changes the headline number. The starter

`tok/char` metric is specifically code-point based and should not be

presented as though it were interchangeable with graphemes or bytes.



This is a conceptual measurement problem, not a claim that code-point

counting itself is invalid.



\---



\## A5 - Compare parallel-sentence denominator



\### Hypothesis



For aligned multilingual text, tokens per aligned sentence may be a

more useful controlled comparison than tokens per whitespace word.



\### Experiment



Measured GPT-2 tokens per sentence and tokens per word on the 997-line

FLORES corpus.



\### Result



The final corrected GPT-2 sentence-level comparison produced:



\- English: 26.78 tok/sentence

\- Hindi: 192.43 tok/sentence

\- Kannada: 351.05 tok/sentence

\- Tamil: 398.38 tok/sentence



Relative to English:



\- Hindi: 7.19x

\- Kannada: 13.11x

\- Tamil: 14.88x



\### Revision



Sentence-level normalization answers a different question from word

fertility. It is useful for comparing aligned text, but production

routing should ultimately use actual request token counts on the target

model/workload.



\---



\## A6 - Check line-average versus corpus-wide calculation



\### Hypothesis



Averaging per-line fertility may differ from calculating total tokens

divided by total words.



\### Experiment



Compared both methods on the starter sample.



\### Result



English:



\- line average: 1.283063

\- corpus ratio: 1.269231

\- difference: 1.09%



Hindi:



\- line average: 7.598452

\- corpus ratio: 7.524590

\- difference: 0.98%



\### Revision



The methods differ, but the observed effect is only about 1% on this

sample. This is not a primary flaw for the audit.



\---



\## A7 - Test NFC normalization



\### Hypothesis



Unicode normalization may change some text representations and therefore

token counts.



\### Experiment



Compared raw and NFC-normalized FLORES lines.



\### Result



NFC changed:



\- 0 English lines

\- 90 Hindi lines

\- 109 Kannada lines

\- 2 Tamil lines



Token totals changed by:



\- English: 26,696 -> 26,696 (0.00%)

\- Hindi: 191,616 -> 191,855 (+0.125%)

\- Kannada: 350,049 -> 349,998 (-0.015%)

\- Tamil: 397,195 -> 397,189 (-0.002%)



\### Revision



NFC normalization is defensible preprocessing. It changes some Unicode

representations, but the measured token-count impact is very small.



It should not be presented as a bug.



\---



\## A8 - Compare tokenizer families



\### Hypothesis



If the large Indic fertility values are caused mainly by the script,

different tokenizers should show similarly poor behavior.



\### Experiment



Compared corrected fertility using:



\- GPT-2 tokenizer

\- XLM-R tokenizer



on the same normalized FLORES corpus with the same word denominator.



\### Result



| Language | GPT-2 | XLM-R |

|---|---:|---:|

| English | 1.274 | 1.408 |

| Hindi | 7.797 | 1.489 |

| Kannada | 22.683 | 2.568 |

| Tamil | 24.618 | 2.424 |



Relative to English:



GPT-2:



\- Hindi: 6.12x

\- Kannada: 17.80x

\- Tamil: 19.32x



XLM-R:



\- Hindi: 1.06x

\- Kannada: 1.82x

\- Tamil: 1.72x



\### Revision



Tokenizer choice has a very large effect. This directly contradicts the

starter report's claim that the problem is simply a property of the

script and that any tokenizer will struggle.



The comparison is still not a direct serving-cost comparison because

GPT-2 and XLM-R are different model/tokenizer families.



\---



\## A9 - Consolidated corrected metrics



The final audit uses:



\- FLORES-200 dev

\- 997 aligned sentences

\- NFC normalization

\- lowercase preprocessing

\- corrected whitespace splitting

\- GPT-2 and XLM-R



Final tokens per sentence:



| Language | GPT-2 | XLM-R |

|---|---:|---:|

| English | 26.78 | 29.58 |

| Hindi | 192.43 | 36.75 |

| Kannada | 351.05 | 39.74 |

| Tamil | 398.38 | 39.23 |



\### Interpretation



The starter report's 5.89x Hindi serving-cost conclusion is not supported

by the corrected multilingual experiment.



The strongest evidence is that tokenizer choice changes Indic tokenization

by several-fold.



\### Routing revision



For controlled multilingual benchmarking, tokens per aligned sentence is

a useful denominator.



For production routing/capacity, use actual input and output tokens per

request on the target model, segmented by language and workload, together

with latency and cost.



\---



\# Part B - Serving Audit



\## B1 - KV-cache arithmetic



\### Hypothesis



The model specification should allow an exact calculation of KV-cache

bytes per token and approximate full-length sequence capacity.



\### Calculation



Per layer:



&#x20;   2 x KV\_heads x head\_dim x bytes\_per\_fp16



&#x20;   = 2 x 8 x 128 x 2

&#x20;   = 4,096 bytes/token/layer



Across 28 layers:



&#x20;   4,096 x 28

&#x20;   = 114,688 bytes/token



Therefore:



&#x20;   114,688 bytes/token

&#x20;   = 112 KiB/token



For a 4096-token sequence:



&#x20;   114,688 x 4096

&#x20;   = 469,762,048 bytes

&#x20;   = 448 MiB



GPU memory budget:



&#x20;   24 GiB x 0.92 = 22.08 GiB



Subtracting approximately 1.6 GB of non-KV runtime overhead leaves about

20.6 GiB for KV cache.



Therefore the theoretical full 4096-token capacity is approximately:



&#x20;   20.6 GiB / 448 MiB

&#x20;   \~= 47 sequences



\### Revision



The arithmetic predicts roughly 47 full-length sequences, but real serving

capacity also depends on allocator behavior, workload mix, and runtime

overhead.



\---



\## B2 - Long-context throughput anomaly



\### Hypothesis



The reported increase in tok/s for long prompts may be caused by the

throughput metric counting prompt tokens as well as generated tokens.



\### Experiment



For batch 16:



Short workload:



&#x20;   16 x (512 + 256) / 13.91

&#x20;   = 883.2 tok/s



Output-only throughput:



&#x20;   16 x 256 / 13.91

&#x20;   \~= 294.0 output tok/s



Long workload:



&#x20;   16 x (3584 + 512) / 49.97

&#x20;   = 1311.4 tok/s



Output-only throughput:



&#x20;   16 x 512 / 49.97

&#x20;   \~= 164.6 output tok/s



\### Result



The long workload has higher reported aggregate tok/s but lower output

generation throughput.



The long-context rows also show:



| Batch | Reported tok/s | KV util | Preemptions |

|---:|---:|---:|---:|

| 16 | 1311.4 | 0.62 | 0 |

| 24 | 1607.4 | 0.93 | 0 |

| 32 | 1384.0 | 0.97 | 7 |

| 48 | 1298.5 | 0.97 | 23 |



\### Revision



The apparent long-context throughput improvement is primarily a metric

interpretation issue. At higher batches, KV saturation and preemption

also degrade throughput and latency.



A sensible long-context operating point is around batch 24 for this

specific workload.



This is a workload-specific recommendation, not a universal batch-size

limit.



\---



\## B3 - Correct reported throughput and goodput



\### Hypothesis



The `reported\_tok\_s` column may be incorrectly interpreted as output

generation throughput.



\### Experiment



For batch 24, prompt 3584, generation 512:



&#x20;   batch = 24

&#x20;   wall clock = 61.16 s

&#x20;   reported\_tok\_s = 1607.4



Direct output goodput:



&#x20;   24 x 512 / 61.16

&#x20;   \~= 200.13 output tok/s



Using reported throughput:



&#x20;   1607.4 x 512 / (3584 + 512)

&#x20;   \~= 200.9 output tok/s



The small difference is caused by rounding in the logged reported\_tok\_s.



\### Revision



The report should describe 1607.4 as aggregate prompt+output processing

throughput, not output generation throughput.



The honest batch-24 long output goodput is approximately 200 output tok/s.



The claim that batch 48 should reach approximately 3200 tok/s is not

supported: the observed batch-48 value is 1298.5 aggregate tok/s, with

23 preempted sequences.



\---



\## B4 - Serving metric



\### Proposed metric



Track a serving scheduler \*\*KV-cache preemption counter\*\*.



\### Expected evidence



For the existing benchmark:



\- batch 24: 0 preempted sequences

\- batch 32: 7

\- batch 48: 23



This metric directly exposes the failure mode that aggregate throughput

can hide.



\---



\# Part C - Product Decision



\## Hypothesis



A small inference-time rewriter may provide a faster and more reversible

way to improve conversational style than modifying the main model.



\## Decision



Use option (b), a <=1B inference-time rewriter, as the primary experiment,

with prompt engineering as the baseline.



Do not claim that the rewriter is already successful because it has not

been run on the target A100 environment.



\## Constraints



Maximum compute resource:



&#x20;   14 days x 24 hours = 336 A100-hours



Native reviewer capacity:



&#x20;   10 hours/week x 2 weeks = 20 reviewer-hours



Reviewer coverage is limited to Hindi and Kannada.



\## Day-1 experiment



Compare:



1\. Main model with prompt-only conversational instruction.

2\. Main model output passed through a <=1B local rewriter.



Evaluate:



\- conversational quality

\- meaning preservation

\- added latency



Use the six target languages:



\- Hindi

\- Kannada

\- Tamil

\- Telugu

\- Bengali

\- Marathi



\## Decision thresholds



Proposed success threshold:



\- >=20% relative improvement in mean casualness score on the

&#x20; human-reviewed Hindi/Kannada subset

\- <=5% meaning-preservation failures

\- <=300 ms median added latency



Proposed kill criterion:



Stop after five engineering days if casualness improvement is below

10%, or median added latency exceeds 500 ms.



These are proposed thresholds, not measured results.



\## Biggest caveat



Only Hindi and Kannada have native-speaker review. Evidence for the other

four languages is therefore weaker and requires additional validation

before broad rollout.



\---



\# Final Audit Conclusions



1\. The starter whitespace counting implementation contains a real bug.

2\. The `tok/char` metric is specifically code-point based and should not

&#x20;  be treated as interchangeable with other denominators.

3\. Tokenizer choice materially changes Indic tokenization.

4\. The starter report's script-only explanation is not supported by the

&#x20;  corrected tokenizer comparison.

5\. The 5.89x Hindi serving-cost claim cannot be inferred from the starter

&#x20;  benchmark alone.

6\. `reported\_tok\_s` includes both prompt and generated tokens.

7\. Long-context aggregate tok/s therefore does not mean higher generation

&#x20;  throughput.

8\. KV-cache saturation and preemption explain the degradation at high

&#x20;  long-context batch sizes.

9\. The batch-24 long workload produces about 200 output tokens/s.

10\. Production decisions should use target-model input/output tokens per

&#x20;   request, latency, cost, and serving saturation metrics rather than a

&#x20;   single tokenizer fertility number.

