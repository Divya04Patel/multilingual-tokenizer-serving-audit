# Part C - Casual/Conversational Multilingual Output



## Decision



Choose **(b) a <=1B inference-time rewriter** as the primary experiment,

with **(c) prompt engineering as the baseline**. Do not commit to SFT

before measuring whether the smaller intervention is sufficient.



The rewriter is preferable under the three-week launch constraint because

it can be tested and rolled back independently of the main model. SFT may

eventually give better integrated quality, but it requires more data and

quality validation, while the available native-speaker review covers only

Hindi and Kannada.



## Assumptions and resource budget



The maximum A100-80GB resource available for the experiment is:



14 days x 24 h = 336 A100-hours.



The native-speaker reviewer is available for 10 h/week. Allocate

20 reviewer-hours across the first two weeks for the pilot, and

reserve up to 10 additional hours in week 3 for launch validation.



Use the first five engineering days as a go/no-go experiment rather than

spending the full compute budget before evidence is available.



## Day-1 experiment



Freeze a small smoke-test set covering Hindi, Kannada, Tamil, Telugu,

Bengali and Marathi. Generate:



1\. Main-model output using the best prompt-only baseline.

2\. The same output passed through a <=1B local rewriter.



Use the 8-example set initially to validate the evaluation pipeline.

Before making the go/no-go decision, expand the evaluation set to at

least 60 examples (10 per language).



For Hindi and Kannada, the native reviewer scores conversational quality

from 1 (very formal/textbook) to 5 (natural/conversational).



For all six languages, automatically check preservation of numbers and

other explicitly protected content, followed by manual review of sampled

outputs where possible.



Measure median added latency for the rewriter on the target deployment.



## Success threshold



Continue the rewriter only if, on the human-reviewed Hindi/Kannada

subset:



\- mean casualness score improves by >=20% relative to the prompt-only

&#x20; baseline;

\- meaning-preservation failures are <=5% on the expanded evaluation set;

\- median added latency is <=300 ms/request.



These are predefined decision thresholds, not measured results.



## Kill criterion



Stop the rewriter after **5 engineering days** if it produces less than

a **10% casualness improvement**, or if median added latency exceeds

**500 ms/request**. Do not ship based only on automated scores.



## Biggest caveat



Only Hindi and Kannada have native-speaker review. Tamil, Telugu, Bengali

and Marathi therefore have weaker launch evidence. A successful pilot

should trigger additional native-speaker validation before broad rollout.



## Production metric



Track \*\*casualness improvement at a fixed meaning-preservation rate,

segmented by language\*\*, together with rewriter latency. This avoids

optimizing style while silently changing the model's answer.

