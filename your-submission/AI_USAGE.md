\# AI Usage



\## How AI was used



AI assistance was used as a critical thinking and implementation aid

throughout the audit.



The work was not treated as authoritative output. Claims were checked

against the provided starter code, benchmark logs, and measured

experiments before being included in the final analysis.



\## Part A



AI assistance was used to:



\- inspect the tokenizer benchmark implementation;

\- identify candidate measurement and implementation issues;

\- design experiments for whitespace splitting and denominator choice;

\- suggest a multilingual evaluation corpus;

\- help design comparisons between GPT-2 and XLM-R;

\- help calculate and interpret relative tokenizer metrics.



The resulting claims were verified by running the benchmark scripts locally

and recording the observed values.



In particular, the whitespace-splitting issue was not accepted based only

on inspection. It was tested on both the starter sample and the FLORES-200

corpus.



The denominator analysis was also experimentally verified using code-point,

grapheme-cluster, and UTF-8-byte denominators.



\## Part B



AI assistance was used to:



\- derive the KV-cache memory formula from the supplied model specification;

\- check the arithmetic for bytes per token and 4096-token sequence capacity;

\- interpret the benchmark columns;

\- derive output-only goodput;

\- identify the relationship between KV-cache utilization,

&#x20; preemptions, throughput, and latency;

\- propose a workload-specific concurrency/configuration recommendation.



The numerical conclusions were calculated from the supplied benchmark

log rather than assumed from general serving-system behavior.



\## Part C



AI assistance was used to:



\- compare the three proposed product options;

\- structure the Day-1 experiment;

\- define measurable success and kill criteria;

\- identify the limitation caused by native-speaker coverage;

\- help formulate the product decision memo.



No claim of measured rewriter quality or latency is made because the

rewriter was not actually run on the target A100 environment.



\## Human verification



I reviewed the generated analysis, ran the relevant Python experiments,

checked numerical calculations, and revised conclusions when experiments

did not support a stronger claim.



Unsupported claims were deliberately excluded.



For example, the original claim that Hindi would necessarily cost roughly

6x more to serve was not retained as a production conclusion because

tokenizer choice and denominator selection materially changed the result.



Similarly, the apparent long-context throughput improvement was

re-examined by separating aggregate prompt+generation throughput from

output-only generation throughput.



\## Principle



AI was used to accelerate exploration, coding, calculation, and

reasoning, while final conclusions were based on reproducible evidence

from the provided artifacts and experiments.

