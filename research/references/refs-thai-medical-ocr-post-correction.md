# Last Updated: 2026-03-31

# Reference Mining: Thai Medical OCR + Post-correction

Sources queried: arXiv search pages for "thai ocr", "medical ocr", "post-ocr correction" (accessed 2026-03-31)

---

## Priority References (Top Relevance)

| Paper | Link | Why it matters for your work |
|---|---|---|
| Typhoon OCR: Open Vision-Language Model For Thai Document Extraction (2026) | https://arxiv.org/abs/2601.14722 | Thai-focused OCR/VLM design, layout reconstruction, compact deployment-friendly model. |
| MeDocVL: A Visual Language Model for Medical Document Understanding and Parsing (2026) | https://arxiv.org/abs/2602.06402 | Medical document parsing under noisy annotations; query-driven extraction and robust post-training strategy. |
| OCR Error Post-Correction with LLMs in Historical Documents: No Free Lunches (2025) | https://arxiv.org/abs/2502.01205 | Practical limits and trade-offs of LLM post-correction; useful for setting realistic baselines and evaluation plans. |

---

## Secondary References from Same Search Sweep

- PreP-OCR: A Complete Pipeline for Document Image Restoration and Enhanced OCR Accuracy (ACL 2025): https://arxiv.org/abs/2505.20429
- RoundTripOCR: Data Generation for Post-OCR Correction in Low-Resource Devanagari Languages: https://arxiv.org/abs/2412.15248
- NeKo: Cross-Modality Post-Recognition Error Correction with Tasks-Guided MoE LM (ACL Industry 2025): https://arxiv.org/abs/2411.05945
- Reference-Based Post-OCR Processing with LLM for Diacritic Text: https://arxiv.org/abs/2410.13305
- Efficient Medical VIE via Reinforcement Learning: https://arxiv.org/abs/2506.13363

---

## Practical Search Queries for Next Iteration

- "thai clinical ocr dataset"
- "thai medical report information extraction benchmark"
- "ocr post correction llm low resource language cer wer"
- "dicom burned-in text de-identification ocr"
- "medical document VLM field-level exact match"

---

## Suggested Evaluation Axes

- OCR stage: CER, WER, field-level exact match
- Post-correction stage: CER delta, term-preservation rate for medical entities
- Safety/compliance: PHI leakage rate, de-identification recall on burned-in text
- Efficiency: latency per page/report, GPU/CPU memory footprint
