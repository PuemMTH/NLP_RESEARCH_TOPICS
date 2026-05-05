# Last Updated: 2026-05-06

# Source Synthesis: VLM Thai OCR Reference Deep Dive

This note expands references used in [/output/diagrams/vlm-thai-ocr-research-summary-2026-05-06.html](/output/diagrams/vlm-thai-ocr-research-summary-2026-05-06.html) and [/research/references/refs-vlm-thai-ocr-extension-2026-05.md](/research/references/refs-vlm-thai-ocr-extension-2026-05.md).

## Topic Map

| Group | Main references | Best use in this project |
|---|---|---|
| Thai-specific OCR/VLM | Typhoon OCR, ThaiOCRBench, Typhoon 2 | Primary Thai document OCR baseline and benchmark template |
| General document VLM | Qwen2.5-VL, mPLUG-DocOwl 1.5/2, InternVL | Strong open baselines for structured extraction and layout-heavy documents |
| Evaluation metrics | ANLS*, multi-layered evaluation, BERTScore | Replace WER/cosine-only evaluation with layered OCR reliability scoring |
| Multimodal product understanding | Zero-shot VLM classification, product deduplication, CLIP-style alignment | Upgrade SME product cleaning from text-only to image+text checks |
| Low-resource VLM | low-resource multimodal surveys, cross-lingual transfer | Justification for Thai-specific adaptation and small-data fine-tuning |

---

## Typhoon OCR

**Source**: <https://arxiv.org/abs/2601.14722>, <https://huggingface.co/typhoon-ai/typhoon-ocr-7b>

**Topic(s)**: Thai OCR, VLM document parsing, layout reconstruction, OCR post-correction

**Summary**: Typhoon OCR is an open Thai-English VLM for document extraction. The paper frames Thai OCR as difficult because of Thai script complexity, missing explicit word boundaries, and unstructured real-world documents. The model combines text transcription, layout reconstruction, and document-level structure in one framework.

**Key Points**:
- Strong fit for Stage 3+4+5 replacement: text recognition, post-correction, and structured extraction.
- The training pipeline is a useful template: traditional OCR output, VLM restructuring, and curated synthetic data.
- The Hugging Face model card warns that the model is task-specific, intended for provided prompts, and can hallucinate.
- Product/medical workflows should therefore use Typhoon OCR behind a verifier or validation stage, not as an unchecked final source of truth.

**Ideas / Gaps**:
- Test Typhoon OCR on SME product labels, because existing benchmark categories emphasize broader Thai document types.
- Use Typhoon OCR as a fallback only when modular OCR confidence or ANLS is low.
- Add field-level verifier for critical values after Typhoon OCR extraction.

---

## ThaiOCRBench

**Source**: <https://arxiv.org/abs/2511.04479>, <https://huggingface.co/datasets/typhoon-ai/ThaiOCRBench/blob/main/README.md>

**Topic(s)**: Thai OCR benchmark, VLM evaluation, document understanding

**Summary**: ThaiOCRBench is a Thai text-rich VLM benchmark with 2,808 human-annotated samples across 13 task categories. The Hugging Face dataset card lists fields `image`, `Task`, `question`, `answer`, and `category`, making it directly reusable as a template for an internal benchmark format.

**Key Points**:
- Categories include text recognition, table parsing, full-page OCR, chart parsing, key information extraction, document classification, handwritten extraction, document parsing, and VQA.
- The benchmark is designed for zero-shot evaluation of proprietary and open-source VLMs.
- Error analysis identifies language bias, structural mismatch, and hallucinated content.
- It avoids a single metric family; tasks use different metrics according to task type.

**Ideas / Gaps**:
- Build a smaller internal NECTEC benchmark using the same schema:
  - `image`
  - `task`
  - `question`
  - `answer`
  - `category`
  - `field_type`
  - `criticality`
- Add product-specific categories not covered by ThaiOCRBench:
  - product label OCR
  - ad vs. package classification
  - ingredient/key-value extraction
  - brand and unit preservation

---

## Typhoon 2

**Source**: <https://arxiv.org/abs/2412.13702>

**Topic(s)**: Thai LLM, Thai VLM, Thai document understanding

**Summary**: Typhoon 2 is a family of Thai-optimized text and multimodal models, including text, vision, audio, and safety components. Typhoon2-Vision is relevant because it improves Thai document understanding while retaining general visual capabilities.

**Key Points**:
- Typhoon2-Text can support LLM-as-a-Judge or LLM-as-a-Verifier experiments.
- Typhoon2-Vision can support ad/product-label classification and OCR quality auditing.
- Typhoon2-Safety is relevant if outputs include Thai cultural or sensitive content handling.

**Ideas / Gaps**:
- Compare Typhoon2-Text verifier vs. GPT-style verifier on product and OCR field verification.
- Use Typhoon2-Vision for zero-shot product-label vs. advertising-image classification before trying fine-tuning.

---

## Qwen2.5-VL

**Source**: <https://arxiv.org/abs/2502.13923>

**Topic(s)**: general VLM baseline, structured extraction, layout understanding

**Summary**: Qwen2.5-VL is a strong open VLM family used as a general-purpose baseline for OCR, document understanding, structured extraction, and visual reasoning. It is useful as a non-Thai-specific comparison model against Typhoon OCR and Typhoon2-Vision.

**Key Points**:
- Good baseline for zero-shot key-value extraction from forms, tables, and product labels.
- Useful for measuring whether Thai-specific fine-tuning is necessary.
- Should be evaluated under the same internal benchmark as Typhoon OCR, not only with ad hoc examples.

**Ideas / Gaps**:
- Compare Qwen2.5-VL 7B vs. Typhoon OCR/Typhoon2-Vision on:
  - Thai product label OCR
  - key-value extraction
  - handwritten/noisy text
  - Thai-English mixed layout

---

## mPLUG-DocOwl 1.5 and DocOwl2

**Sources**: <https://arxiv.org/abs/2403.12895>, <https://arxiv.org/abs/2409.03420>

**Topic(s)**: OCR-free document understanding, structure learning, multi-page documents

**Summary**: DocOwl 1.5 emphasizes unified structure learning for OCR-free document understanding across documents, webpages, tables, charts, and natural images. DocOwl2 extends this line to high-resolution multi-page document understanding by compressing high-resolution pages into fewer visual tokens.

**Key Points**:
- DocOwl 1.5 is most relevant to complex layout understanding and table/chart structure.
- DocOwl2 is relevant if the project expands from single product/document images to multi-page PDFs.
- Their technical contribution is not Thai-specific, but the structure-learning framing is useful for Thai forms and tables.

**Ideas / Gaps**:
- Use DocOwl-style structure learning as conceptual backing for why layout-aware evaluation matters.
- If local deployment is the goal, benchmark latency and memory before adopting OCR-free multi-page models.

---

## ANLS*

**Source**: <https://arxiv.org/abs/2402.03848>

**Topic(s)**: document evaluation metric, generative model evaluation, OCR/VQA scoring

**Summary**: ANLS* extends Average Normalized Levenshtein Similarity for evaluating generative document-processing outputs across classification and information extraction tasks. It is positioned as a drop-in replacement compatible with ANLS while supporting more complex generated outputs.

**Key Points**:
- Better fit than WER for field extraction because it tolerates small OCR errors without requiring exact word segmentation.
- Useful for Thai because WER depends on tokenizer choice.
- Works best as part of a layered metric stack, not alone.

**Ideas / Gaps**:
- Use CER for raw transcription, ANLS/ANLS* for field string similarity, and verifier labels for critical field correctness.
- Add field criticality: an ANLS score can be acceptable for non-critical text but not for dosage/unit fields.

---

## Multi-Layered Evaluation with LLMs as Judges

**Source**: <https://aclanthology.org/2025.coling-main.408.pdf>

**Topic(s)**: evaluation stack, LLM-as-a-Judge, metric fusion

**Summary**: This COLING 2025 paper argues that lexical metrics, semantic metrics, and LLM judges each have trade-offs. Its key project-relevant idea is a layered evaluation design that routes easy cases through cheaper deterministic metrics and reserves LLM judging for harder cases.

**Key Points**:
- Supports a cost-aware evaluation cascade.
- OCR evaluation can use the same idea:
  - Layer 1: exact match/CER/rules
  - Layer 2: ANLS/BERTScore
  - Layer 3: LLM judge or verifier for disagreement/critical fields

**Ideas / Gaps**:
- Add routing logic: call LLM verifier only when CER and ANLS disagree, confidence is low, or the field is high severity.

---

## Zero-Shot VLM Classification with Contrastive Text Descriptions

**Source**: <https://openaccess.thecvf.com/content/CVPR2024/papers/Saha_Improved_Zero-Shot_Classification_by_Adapting_VLMs_with_Text_Descriptions_CVPR_2024_paper.pdf>

**Topic(s)**: VLM classification, prompt engineering, product image filtering

**Summary**: This work improves zero-shot VLM classification by adapting classes with text descriptions. The directly useful idea is to give contrastive descriptions for ambiguous classes instead of short labels only.

**Key Points**:
- Better than asking only "product or ad?" because SME images can be ambiguous.
- Prompt classes should describe visual intent:
  - product package / label / ingredient / specification
  - advertisement / promotion / lifestyle / claim-heavy poster

**Ideas / Gaps**:
- Build a prompt set with Thai and English descriptions.
- Evaluate whether Typhoon2-Vision or Qwen2.5-VL is more stable for Thai product images.

---

## Multimodal Thai / CLIP-Style Embeddings

**Sources**: <https://huggingface.co/patomp/thai-light-multimodal-clip-and-distill>, <https://huggingface.co/tomaarsen/jina-clip-v2>

**Topic(s)**: image-text alignment, product data cleaning, multilingual retrieval

**Summary**: The original research note marked a "Thai CLIP gap". A more precise statement is that public Thai/multilingual image-text embedding options exist, but they are not yet validated for noisy SME product-label OCR. The Thai-light multimodal model is tied to Thai MS COCO-style captions, while Jina CLIP v2 is multilingual and supports 89 languages, but remains general-purpose rather than product/OCR-specific.

**Key Points**:
- Thai-light multimodal CLIP/distill models are possible lightweight candidates for image-text alignment.
- Jina CLIP v2 is a stronger multilingual embedding baseline and supports image-text retrieval.
- Neither should be assumed reliable for Thai product OCR without domain testing.

**Ideas / Gaps**:
- Reframe the research gap as:
  - "Thai product-label image-text alignment remains under-validated."
- POC:
  - compute image-text alignment between product image and OCR text
  - compare Thai-light, Jina CLIP v2, and Typhoon2-Vision judgment
  - measure against human labels for match / mismatch

---

## Research Decision

The most practical next research line is not "replace OCR with VLM" immediately. The stronger path is:

1. Build an internal benchmark slice inspired by ThaiOCRBench.
2. Upgrade Module 2 evaluation from WER/cosine to CER + ANLS + verifier.
3. Add VLM fallback for low-confidence or unsupported fields.
4. Test Typhoon OCR and Qwen2.5-VL as competing Stage 3+4+5 systems.
5. Only then consider LoRA fine-tuning on product/medical documents.

