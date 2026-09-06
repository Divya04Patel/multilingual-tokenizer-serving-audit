\# Part C — Day-1 Experiment



\## Objective



Test whether a small local inference-time rewriter (<=1B parameters)

can make the main model's outputs more conversational while preserving

meaning.



\## Baselines



\### Baseline A — Prompt engineering



Ask the main model to directly produce conversational output.



\### Treatment B — Inference-time rewriter



Generate the normal main-model response first, then pass it through a

<=1B local rewriter instructed to make the response conversational

without changing facts, numbers, names, or intent.



\## Evaluation set



The initial pilot contains 8 examples across six target languages:



\- Hindi

\- Kannada

\- Tamil

\- Telugu

\- Bengali

\- Marathi



Hindi and Kannada examples are the languages available for human

reviewer validation.



\## Metrics



\### 1. Casualness



A human reviewer scores output from 1 to 5:



1 = very formal/textbook

5 = natural conversational language



The Hindi/Kannada reviewer compares baseline and rewriter outputs.



\### 2. Meaning preservation



Check whether facts, numbers, names, and intent remain unchanged.



Any factual or semantic change is a failure.



\### 3. Latency



Measure additional median latency introduced by the rewriter on the

target A100 deployment.



\## Proposed success threshold



Select the rewriter for further rollout only if:



\- casualness improves by at least 20% relative to the prompt-only

&#x20; baseline on the human-reviewed Hindi/Kannada subset;

\- meaning-preservation failures are <=5%;

\- median added latency is <=300 ms/request.



These are decision thresholds, not measured results.



\## Kill criterion



Stop the rewriter experiment after five engineering days if it fails

to achieve at least a 10% casualness improvement on the evaluation

set, or if median added latency exceeds 500 ms/request.



\## Day-1 procedure



1\. Freeze the evaluation examples.

2\. Generate prompt-only baseline outputs.

3\. Generate rewriter outputs.

4\. Run automated preservation checks.

5\. Have the reviewer score Hindi and Kannada outputs for casualness.

6\. Measure rewriter latency on the target deployment.

7\. Compare against the predefined thresholds.



\## Deployment decision



If the thresholds are met, continue with the rewriter as a reversible

inference-time layer and expand human review before launch.



If they are not met, do not ship the rewriter. Reassess prompt

engineering or a supervised fine-tuning approach using the evidence

from the experiment.

