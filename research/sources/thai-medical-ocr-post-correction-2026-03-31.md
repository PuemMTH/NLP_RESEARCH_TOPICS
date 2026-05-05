# Last Updated: 2026-03-31

---
### Typhoon OCR
**Source**: https://arxiv.org/abs/2601.14722
**Topic(s)**: thai-ocr, vision-language-models, low-resource-nlp
**Summary**: Typhoon OCR presents an open Thai-and-English vision-language OCR model targeted at difficult real-world Thai documents. The paper highlights Thai-specific challenges such as script complexity and no explicit word boundaries, and proposes a multi-stage data pipeline with OCR/VLM restructuring and synthetic data. Reported results indicate competitive performance with lower compute cost.
**Key Points**:
- Thai-centric training pipeline and document extraction objectives.
- Unified handling of transcription + layout reconstruction.
- Compact inference-efficient variant (V1.5) for easier deployment.
**Referenced / Related**:
- Thai document extraction benchmarks and synthetic data methods.
**Ideas / Gaps**: Need validation on Thai medical documents specifically (prescriptions, lab reports, DICOM overlays).

---
### MeDocVL
**Source**: https://arxiv.org/abs/2602.06402
**Topic(s)**: medical-ocr, medical-document-parsing, multimodal-information-extraction
**Summary**: MeDocVL targets medical document OCR/parsing where layout complexity, domain terms, and noisy labels hurt standard OCR and generic VLMs. It combines label refinement with hybrid post-training (SFT + RL) for robust, precise query-driven extraction. The reported benchmark focus is medical invoices with noisy supervision.
**Key Points**:
- Strong emphasis on field-level exact extraction reliability.
- Noise-aware training strategy aligns with real hospital data conditions.
- Suggests a blueprint for structured extraction after OCR.
**Referenced / Related**:
- Medical invoice parsing and VIE benchmarks.
**Ideas / Gaps**: Transferability to Thai-language medical documents remains an open question.

---
### OCR Error Post-Correction with LLMs: No Free Lunches
**Source**: https://arxiv.org/abs/2502.01205
**Topic(s)**: post-ocr-correction, llm-evaluation, low-resource-nlp
**Summary**: This study evaluates open-weight LLMs for OCR post-correction and reports mixed outcomes: gains for English CER, but not practically sufficient for Finnish. It explores tuning, quantization, segment length, and continuation choices, showing that post-correction quality is highly setup-dependent.
**Key Points**:
- LLM post-correction can help, but not uniformly across languages.
- Engineering choices materially change correction quality.
- Reinforces need for language/domain-specific evaluation.
**Referenced / Related**:
- CER-focused OCR post-correction benchmarks.
**Ideas / Gaps**: Thai medical text may need explicit lexicon constraints and terminology-aware decoding.

---

## Topic Map (Round Snapshot)
- thai-ocr: Typhoon OCR
- medical-ocr: MeDocVL
- post-ocr-correction: No Free Lunches
- low-resource-nlp: Typhoon OCR, No Free Lunches

---

## POC Log

### 2026-05-06 — VLM Zero-Shot Image Classifier

**POC folder**: `poc/vlm-zero-shot-classifier/`
**Model**: `scb10x/typhoon2-qwen2vl-7b-vision-instruct` (Typhoon2-Vision, Thai-optimised Qwen2-VL-7B)
**Fallback**: `Qwen/Qwen2.5-VL-7B-Instruct`

**Goal**: Replace the hardcoded 700-char OCR text-length threshold for classifying SME product images as "ad/label" vs "product" with a direct VLM zero-shot classifier.

**Pipeline stage**: Stage 2 (Layout/Routing) — sits before OCR, routes images to appropriate processing path.

**Results on synthetic samples**:
- `sample_product.png` (33 chars): VLM → "product" (conf=0.95) | 700-char rule → "product" | AGREE
- `sample_ad_label.png` (795 chars): VLM → "advertisement" (conf=0.95) | 700-char rule → "advertisement" | AGREE

**Thai language notes**: Typhoon2-Vision is Thai-aware and correctly interpreted Thai promotional text in the label image. Confidence self-reporting is not calibrated probability — tune the 0.7 threshold on real labelled data.

**VRAM**: RTX 5070 (11.5 GB) → use `--load-4bit` (~6-8 GB). BF16 default requires ~15 GB.

**Key files**:
- `poc/vlm-zero-shot-classifier/poc_runner.py`
- `poc/vlm-zero-shot-classifier/generate_sample.py`
- `poc/vlm-zero-shot-classifier/run.sh`
