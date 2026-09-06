\# Part B1 — KV Cache Capacity



\## Given model specification



\- Layers: 28

\- KV heads: 8

\- Head dimension: 128

\- KV cache precision: FP16 = 2 bytes

\- GPU memory: 24 GB

\- gpu\_memory\_utilization: 0.92

\- Non-KV runtime overhead: \~1.6 GB

\- max\_model\_len: 4096



\## KV bytes per token



Each token stores K and V:



2 × 8 KV heads × 128 head dimension × 2 bytes FP16

= 4,096 bytes per layer per token.



Across 28 layers:



4,096 × 28 = 114,688 bytes/token



Therefore:



\*\*KV cache = 114,688 bytes/token = 112 KiB/token.\*\*



\## KV memory for one 4096-token sequence



114,688 × 4096

= 469,762,048 bytes

= 448 MiB

≈ 0.470 GB decimal.



\## Estimated concurrent capacity



Usable GPU memory:



24 GiB × 0.92 = 22.08 GiB



Approximate non-KV overhead:



1.6 GB ≈ 1.49 GiB



Estimated KV budget:



22.08 − 1.49 = 20.59 GiB



Therefore:



20.59 GiB / 448 MiB ≈ 47



So approximately \*\*47 full 4096-token sequences\*\* fit in the estimated

KV budget.



\## Check against benchmark



The benchmark's long-context rows reach approximately 0.93 KV-cache

utilization at batch 24 and 0.97 at batches 32 and 48.



This is consistent with the calculation: although approximately 47

4096-token sequences could fit under the simplified full-sequence

estimate, actual serving also has allocation/scheduling overhead and the

benchmark requests have 3584 prompt + 512 generated tokens, so the

observed KV utilization should not be interpreted as an exact

47-sequence capacity test.



\## Conclusion



The KV cache is approximately \*\*112 KiB per token\*\*, and the simplified

memory calculation gives approximately \*\*47 full 4096-token sequences\*\*

within the estimated KV budget. Actual safe concurrency must be

validated using the serving system's measured KV utilization and

preemption behavior.

