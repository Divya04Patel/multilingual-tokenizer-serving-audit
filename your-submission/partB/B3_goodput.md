\# Part B3 — Reported Throughput vs Honest Goodput



\## Misread column



The `reported\_tok\_s` column is not output-generation throughput.



It is calculated as:



batch\_size × (prompt\_len + gen\_len) / wall\_clock\_s



For the batch-24 long-context row:



24 × (3584 + 512) / 61.16

= 1607.4 tok/s.



Therefore `reported\_tok\_s` measures aggregate input + output token

processing rate.



\## Honest output goodput — method 1



Output tokens processed:



24 × 512 = 12,288 tokens.



Divide by wall-clock time:



12,288 / 61.16

= \*\*200.13 output tok/s\*\*.



\## Honest output goodput — method 2



The reported rate includes 4096 total tokens per request:



3584 + 512 = 4096.



The generated portion is:



512 / 4096 = 0.125.



Therefore:



1607.4 × 0.125

= \*\*200.93 output tok/s\*\*.



The small difference from 200.13 is caused by rounding of the

reported 1607.4 value. The wall-clock calculation is the more precise

result.



\## Correct interpretation



The report's approximately 1600 tok/s figure must not be interpreted

as approximately 1600 output tokens/s.



The honest generation goodput for this batch-24 long-context workload

is approximately \*\*200.13 output tok/s\*\*.



This distinction is important for capacity planning because prompt

processing and generated-token throughput have different operational

implications.

