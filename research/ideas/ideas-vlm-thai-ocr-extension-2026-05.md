# Last Updated: 2026-05-05

# Ideas: VLM Extension for Thai OCR Pipeline (2026-05)

Context: NECTEC SME product data cleaning + medical OCR pipeline. Two existing modules:
- Module 1: tokenization (PyThaiNLP newmm), language filter, emoji filter, word frequency threshold, 700-char text-length classifier (ad/label vs. product image)
- Module 2: WER (PyThaiNLP-tokenized) + cosine similarity via SentenceTransformer

Reference file: [/research/references/refs-vlm-thai-ocr-extension-2026-05.md](/research/references/refs-vlm-thai-ocr-extension-2026-05.md)

---

## Idea 1 — Replace 700-Char Heuristic with VLM Zero-Shot Classifier (Module 1)

**Problem**: The 700-character threshold for separating ad images from product-label images is a hand-tuned heuristic. It will break on images with dense product text or sparse ad copy near the threshold.

**Proposed change**: Use a VLM (Typhoon2-Vision or Qwen2.5-VL-7B) with a contrastive prompt:
- Prompt: "Is this image primarily (A) a product label/packaging showing ingredients and specifications, or (B) an advertising image focused on lifestyle or marketing? Answer A or B."
- This is zero-shot — no labelled training data required.
- Fallback: use text-length threshold only when VLM confidence < 0.7.

**Evidence base**: CVPR 2024 contrastive VLM classification paper; ThaiOCRBench shows Typhoon OCR handles Thai document classification.

**Implementation path**: Swap the classifier step in Module 1. Add a `--classifier vlm` flag to the pipeline runner. Measure precision/recall on a held-out set of ~200 images with manual labels.

**Estimated effort**: Low (1–2 days POC). Model: `scb10x/typhoon2-qwen2vl-7b-vision-instruct` (HuggingFace).

---

## Idea 2 — Upgrade Module 2 WER to a 3-Layer Evaluation Stack

**Problem**: WER computed on PyThaiNLP newmm tokenization is tokenizer-relative (Thai ASR research shows the same system scores 13.6% WER under newmm vs. 8.2% under deepcut). Cosine similarity on generic SentenceTransformer embeddings does not capture OCR-domain accuracy (a wrong medical term can have high cosine similarity to a correct one if both appear in similar contexts).

**Proposed 3-layer stack**:

| Layer | Metric | Tool | What it catches |
|-------|--------|------|-----------------|
| L1 | CER (not WER) | jiwer / fastwer | Character-level transcription errors, safer for Thai |
| L2 | ANLS* | anls PyPI package | Tolerates minor OCR confusions; does not over-penalize correct answers with small edit distance |
| L3 | LLM-as-Judge | Typhoon2-Text or GPT-4o-mini | Semantic correctness; catches wrong medical terms that have high cosine sim |

**Why CER over WER**: CER is independent of tokenizer choice — counts character edits, not word-boundary-dependent token edits. This eliminates the newmm drift issue entirely.

**Why ANLS over cosine sim**: ANLS was designed for document VQA and is the standard in DocVQA/ThaiOCRBench. It tolerates known OCR errors (character substitutions) while still penalizing semantically wrong answers.

**Why LLM-as-Judge as top layer**: Cosine similarity can be fooled by embeddings that cluster medically similar but clinically different terms. An LLM judge can be prompted with a domain-specific rubric ("is the test name preserved exactly?", "is the numeric value correct?", "is the unit correct?").

**Implementation path**:
1. Add CER computation (drop WER or run both).
2. Integrate `anls` (pip available) for each field extraction result.
3. Add optional LLM-judge call (rate-limited, only on samples where L1/L2 disagree).

**Estimated effort**: 1 day for L1+L2, 2–3 days for L3 integration with prompt design.

---

## Idea 3 — VLM as Unified Stage 3+4+5 (OCR → Correction → Extraction)

**Problem**: The current pipeline runs Stage 3 (OCR) → Stage 4 (post-correction) → Stage 5 (struct extraction) as three separate models. Each hand-off introduces error accumulation.

**Proposed change**: Use Typhoon OCR or Qwen2.5-VL as a single model that:
- Reads the document image
- Outputs structured markdown/JSON directly (text + layout + key-value in one pass)
- Eliminates inter-stage error propagation

**Evidence base**: Typhoon OCR V1.5 (2B params) outperforms its predecessor (7B) on BLEU/ROUGE-L/Levenshtein across Thai document types: financial reports, government forms, books, infographics, handwritten material.

**Key trade-off**:
- Modular pipeline (EasyOCR + ByT5): ~930 MB, fast, interpretable, controllable
- VLM unified (Typhoon OCR 2B): ~4–6 GB, slower, but handles layout natively

**Recommended hybrid**: Run modular pipeline as default. Add VLM as a fallback triggered when Stage 4 post-correction confidence is below a threshold (e.g., ANLS score < 0.6 on self-verification).

**Estimated effort**: 3–5 days for POC with Typhoon OCR on the existing test set.

---

## Idea 4 — VLM for Semantic OCR Evaluation (Module 2 Replacement Path)

**Problem**: Module 2 uses SentenceTransformer cosine similarity as a semantic quality score. Generic multilingual embeddings are not calibrated for Thai medical/product domain.

**Proposed approach A — BERTScore with WangchanBERTa**:
- Replace cosine similarity with token-level BERTScore using WangchanBERTa as the encoder.
- WangchanBERTa is already in the pipeline (Stage 4 post-correction). Reuse for evaluation.
- BERTScore with domain-matched encoder outperforms generic cosine sim for in-domain text.

**Proposed approach B — Typhoon2-Text as LLM judge**:
- Prompt: "Hypothesis: [OCR output]. Reference: [ground truth]. Are they semantically equivalent for medical/product record purposes? Score 0–5 and explain."
- Captures domain-specific correctness that embeddings miss.
- Expensive: suitable for sample-level auditing, not per-document production scoring.

**Proposed approach C — CLIP-based product image–text alignment score**:
- For Module 1 (product images), use CLIP or SigLIP to score alignment between product image and extracted OCR text.
- Low score = OCR text doesn't match image content = likely extraction error.
- Acts as an automatic OCR quality signal without ground truth.

**Estimated effort**: Approach A: 1 day. Approach B: 2 days (prompt engineering + rate-limit handling). Approach C: 2 days POC.

---

## Idea 5 — ThaiOCRBench as Internal Evaluation Framework

**Problem**: No standardized benchmark exists internally at NECTEC for measuring OCR quality across pipeline variants.

**Proposed action**: Adapt ThaiOCRBench methodology to the NECTEC product/medical domain:
- Collect 200–500 images across categories: product labels, prescription forms, lab results, government ID sections.
- Annotate with ground-truth text + key-value fields.
- Run all pipeline variants (OCR-only, OCR+ByT5, OCR+WangchanBERTa, VLM-unified) against this benchmark.
- Score with the 3-layer stack from Idea 2.

**Outcome**: A reusable internal benchmark that can track regressions when models are updated.

**Evidence base**: ThaiOCRBench design (2,808 samples, 13 task categories, 4 metric families) is a proven template.

**Estimated effort**: 2–3 weeks to collect + annotate + run evaluation pipeline.

---

## Idea 6 — Low-Resource Fine-Tuning of Typhoon OCR for Medical Domain

**Problem**: Typhoon OCR is trained on general Thai documents. Medical forms (lab results, prescriptions, referral letters) have domain-specific layouts and vocabulary not covered in general training.

**Proposed approach**: Fine-tune Typhoon OCR V1.5 (2B) using LoRA on a small set of annotated Thai medical documents.
- Collect 100–300 page images with ground-truth Markdown/JSON annotations.
- Fine-tune with LoRA on the vision encoder + language model jointly.
- Evaluate with field-level F1 and term-preservation rate.

**Evidence base**:
- Cross-lingual transfer paper (ACM MM 2023): visually-derived supervision bridges annotation scarcity.
- Low-resource VLM survey (ScienceDirect 2026): instruction tuning on translated/synthetic data is effective.
- Typhoon OCR's multi-stage synthetic data construction pipeline is a template for generating pseudo-labels cheaply.

**Risk**: Medical annotation requires clinical review. Use pharmacy-grade product labels as a lower-risk starting point.

**Estimated effort**: 4–6 weeks (data collection + annotation + LoRA fine-tuning + evaluation).

---

## Idea 7 — Multimodal Product Data Cleaning (Module 1 Overhaul)

**Problem**: Module 1 processes text extracted from product images through a sequential pipeline (tokenize → filter → frequency → classify). It treats image and text as separate signals.

**Proposed change**: Jointly encode image + text using CLIP or BLIP-2:
- Compute image–text alignment score. Low score = product description does not match the image (data quality issue).
- Use joint embedding for downstream classification instead of text-only features.
- Replace word-frequency threshold with VLM-based relevance scoring ("does this word appear to be a product ingredient/specification?").

**Evidence base**: Multimodal product deduplication paper (macro F1 = 0.90 with joint embeddings). BiLens framework (ScienceDirect 2025) validated on e-commerce product understanding.

**Thai-specific note**: CLIP models (ViT-L/14) have limited Thai text understanding. Use Typhoon2-Vision or a CLIP model fine-tuned on Thai e-commerce data for better alignment scores.

**Estimated effort**: 3–5 days for CLIP-based alignment scoring POC; 2–3 weeks for full joint-embedding classifier.

---

## Priority Ranking (by effort vs. expected impact)

| Priority | Idea | Effort | Expected Impact |
|----------|------|--------|-----------------|
| 1 | Idea 2 — 3-layer evaluation stack (CER + ANLS + LLM-judge) | Low (2–3 days) | High — fixes known WER bias immediately |
| 2 | Idea 1 — VLM zero-shot ad/label classifier | Low (1–2 days) | Medium-High — removes the fragile heuristic |
| 3 | Idea 4A — BERTScore with WangchanBERTa | Low (1 day) | Medium — in-domain semantic eval upgrade |
| 4 | Idea 3 — VLM as unified Stage 3+4+5 | Medium (3–5 days) | High — eliminates inter-stage error accumulation |
| 5 | Idea 5 — Internal ThaiOCRBench adaptation | Medium (2–3 weeks) | High long-term — creates reusable benchmark |
| 6 | Idea 7 — Multimodal Module 1 overhaul | Medium (1–3 weeks) | Medium — needs Thai CLIP or domain fine-tuning |
| 7 | Idea 6 — LoRA fine-tune Typhoon OCR for medical | High (4–6 weeks) | Highest — publishable, domain-specific contribution |

---

## Open Questions / Gaps Identified

1. **Thai CLIP gap**: No publicly available CLIP model fine-tuned on Thai product-image + Thai text pairs. Building this would be a publishable contribution.
2. **WER vs. CER tradeoff for Thai**: No paper specifically compares CER and WER as OCR metrics for Thai, accounting for the character complexity (vowel stacking, tone marks). Worth a short study.
3. **Constrained LLM-judge**: Using an unconstrained LLM judge risks hallucinating medical term corrections. A constrained judge (with lexicon lock, similar to Stage 4 post-correction) has not been published for Thai medical domain.
4. **Typhoon OCR on product labels**: Typhoon OCR benchmarks focus on financial reports, government forms, books. Performance on SME product labels (messy layouts, multilingual, varied fonts) is unknown.
5. **Tokenizer-agnostic WER**: A character-based alternative to WER for Thai that accounts for vowel placement (above/below/left/right) rather than simple character count has not been formalized in literature.
