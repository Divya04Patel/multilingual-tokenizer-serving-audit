\# Part B2 — Long-Context Throughput Anomaly



\## What the report claims



REPORT\_v0 states that at batch 16, long prompts achieve 1311 tok/s

versus 883 tok/s for short prompts, and concludes that longer prompts

give better GPU utilization.



This interpretation is incorrect because `reported\_tok\_s` includes

both prompt and generated tokens.



\## Evidence



For batch 16 with short prompts:



16 × (512 + 256) / 13.91

= 883.2 reported tok/s.



For batch 16 with long prompts:



16 × (3584 + 512) / 49.97

= 1311.4 reported tok/s.



However, output-only throughput is:



Short:

16 × 256 / 13.91

= 294.0 output tok/s.



Long:

16 × 512 / 49.97

= 164.6 output tok/s.



Thus long prompts do not improve generation throughput. The higher

reported tok/s comes from processing substantially more prompt tokens.



\## KV-cache saturation



For the long-context workload:



| Batch | reported tok/s | KV utilization | preempted sequences |

|---:|---:|---:|---:|

| 16 | 1311.4 | 0.62 | 0 |

| 24 | 1607.4 | 0.93 | 0 |

| 32 | 1384.0 | 0.97 | 7 |

| 48 | 1298.5 | 0.97 | 23 |



At batch 32 and 48, KV utilization is approximately saturated and

preemptions appear. Throughput falls while latency rises.



Therefore the long-context anomaly is explained by:

1\. `reported\_tok\_s` counting prompt + generated tokens.

2\. KV-cache pressure at higher concurrency causing preemption.



\## Proposed configuration change



For this 3584-prompt / 512-generation workload, cap long-context

concurrency at approximately batch 24 rather than allowing batches

32–48.



Batch 24 output goodput:



24 × 512 / 61.16

= 200.13 output tok/s.



Batch 48 output goodput:



48 × 512 / 151.41

= 162.04 output tok/s.



Batch 24 therefore provides approximately 23.5% higher output goodput

than batch 48 in this benchmark, while producing zero preemptions

versus 23 at batch 48.



\## Prediction



If the workload remains similar to this benchmark, enforcing a

long-context concurrency cap around 24 should avoid the observed

preemption regime and improve output goodput relative to batch 32–48.



This is a workload-specific prediction and should be validated with

production traffic before treating 24 as a universal optimal value.

