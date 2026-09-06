\# Part B4 — Serving-Stack Metric



\## Recommended metric



Track the serving scheduler's \*\*KV-cache preemption counter\*\*,

represented by `preempted\_seqs` in the benchmark.



This metric directly captures whether sequences are being evicted or

preempted because the KV cache cannot accommodate the active workload.



\## Evidence



For the long-context workload:



| Batch | KV utilization | Preempted sequences |

|---:|---:|---:|

| 24 | 0.93 | 0 |

| 32 | 0.97 | 7 |

| 48 | 0.97 | 23 |



As concurrency enters the KV-cache saturation regime, preemptions

appear and throughput falls.



\## Expected value



For the recommended long-context concurrency cap of approximately

batch 24:



\*\*Expected preempted sequences = 0.\*\*



A non-zero preemption count should be treated as a capacity/scheduling

warning and investigated together with KV-cache utilization, TTFT,

and end-to-end latency.



\## Why this metric



GPU utilization alone would not directly identify the observed

failure mode. KV-cache preemption directly measures the resource

pressure responsible for the throughput and latency degradation.

