# Last Updated: 2026-05-06

# References: LLM as a Verifier (2026-05)

## Core Verification and Factuality Papers

### Chain-of-Verification Reduces Hallucination in Large Language Models
- **Source**: <https://www.research-collection.ethz.ch/entities/publication/dc36c61e-6ae8-4483-8d69-4f57ee0b2229>
- **Venue**: Findings of ACL 2024
- **Summary**: Chain-of-Verification drafts an answer, creates verification questions, answers them independently, and then produces a verified final answer. Useful pattern for OCR correction: generate correction first, then verify critical fields independently before accepting it.
- **Relevance**: Supports a staged correction-then-verification design for Thai OCR.

### Long-form factuality in large language models / SAFE
- **Source**: <https://papers.nips.cc/paper_files/paper/2024/hash/937ae0e83eb08d2cb8627fe1def8c751-Abstract-Conference.html>
- **Venue**: NeurIPS 2024
- **Summary**: SAFE breaks a long answer into individual facts, searches evidence, and judges whether each fact is supported. This maps directly to OCR field verification: decompose an extraction into fields and check each field against OCR/image evidence.
- **Relevance**: Blueprint for evidence-grounded verification rather than generic scoring.

### FactBench and VERIFY
- **Source**: <https://huggingface.co/papers/2410.22257>
- **Year**: 2024
- **Summary**: VERIFY evaluates factuality by considering verifiability and categorizing content as supported, unsupported, or undecidable based on retrieved evidence. FactBench provides hallucination prompts across many topics.
- **Relevance**: The supported/unsupported/undecidable label set is a strong fit for OCR field verification.

### Language Models Hallucinate, but May Excel at Fact Verification
- **Source**: <https://aclanthology.org/2024.naacl-long.62/>
- **Venue**: NAACL 2024
- **Summary**: Studies LLMs as fact verifiers and finds that verification quality depends heavily on evidence quality. The paper also reports weaker performance on numeral-related entity types such as cardinal and ordinal values.
- **Relevance**: Important warning for OCR because product and medical documents contain many numeric fields and units.

## Verifier Models and Verifier-as-Reward Direction

### CompassVerifier
- **Source**: <https://huggingface.co/papers/2508.03686>
- **Year**: 2025
- **Summary**: Presents answer verification as both an evaluation protocol and a reward signal for model optimization.
- **Relevance**: Useful framing if the project later trains a small local verifier for Thai OCR outputs.

### PAG: Policy as Generative Verifier
- **Source**: <https://arxiv.org/abs/2506.10406>
- **Year**: 2025
- **Summary**: Alternates between policy and verifier roles, revising only when verification detects an error.
- **Relevance**: Useful design pattern for selective OCR post-correction: revise only unsupported fields, not the whole text.

## Hallucination Detection Tools

### HaluCheck
- **Source**: <https://colab.ws/articles/10.1016/j.eswa.2025.126712>
- **Year**: 2025
- **Summary**: Introduces explainable hallucination detection with evidence-based sentence checking and visual display of hallucination likelihood. Reports that tailored fact-checking can outperform generic LLM-as-a-Judge.
- **Relevance**: Supports building explicit OCR verifier prompts and evidence spans instead of relying on generic judge scores.

### Fact-checking LLM output via token-level uncertainty
- **Source**: <https://huggingface.co/papers/2403.04696>
- **Year**: 2024
- **Summary**: Uses token-level uncertainty for hallucination detection and fact-checking.
- **Relevance**: Potential extension: combine OCR confidence scores with LLM verification confidence.

