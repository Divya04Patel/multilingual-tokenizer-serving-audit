# Multilingual Tokenizer & Serving Stack Audit

Audit of the provided tokenizer benchmark and serving benchmark from **The Audit** assignment.

## Structure

- `your-submission/NOTEBOOK.md` — chronological audit notebook
- `your-submission/AI_USAGE.md` — AI usage and verification
- `your-submission/partA/` — multilingual corpus, tokenizer audit, and corrected metrics
- `your-submission/partB/` — KV-cache, throughput/goodput, and serving-stack analysis
- `your-submission/partC/` — casual multilingual rewriting experiment and product memo

## Key findings

- The original tokenizer benchmark contains a whitespace-splitting issue whose impact was measured on both the starter corpus and FLORES-200.
- Tokenizer choice materially changes cross-language tokenization results.
- Denominator choice can substantially change the apparent multilingual gap.
- The serving benchmark's reported throughput needs to be separated from output-only goodput for the long-context workload.
- The recommended serving configuration is based on observed preemption behavior in the supplied benchmark.
- For the product problem, an inference-time rewriter is proposed as the first experiment because it fits the launch timeline and available resources.

## Reproducibility

All reported experimental claims are backed by scripts and measured outputs included in `your-submission/`.

The analysis distinguishes measured results from assumptions and proposed experiments.
