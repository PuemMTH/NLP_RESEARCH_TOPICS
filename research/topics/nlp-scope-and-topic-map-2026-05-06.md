# Last Updated: 2026-05-06

# NLP Scope and Topic Map

This note separates the NLP scope into clear topic groups and marks which directions are most relevant to the NECTEC SME/OCR work.

## Scope Layers

```text
NLP
├── A. Core Text NLP
├── B. Information Extraction and Structured NLP
├── C. LLM-era NLP
├── D. Multimodal and Document AI
├── E. Thai / Low-Resource NLP
├── F. Evaluation, Verification, and Safety
└── G. Deployment and Efficiency
```

## A. Core Text NLP

Classic text processing tasks where the input is text and the output is a label, cleaned text, tokens, or transformed text.

| Subtopic | Example tasks | Fit with current work |
|---|---|---|
| Tokenization | Thai word segmentation with PyThaiNLP `newmm` | Direct baseline for SME product names and WER |
| Text cleaning | regex filtering, emoji/symbol removal, normalization | Direct baseline from NECTEC SME product work |
| Text classification | product category, ad vs. product text, spam/noise filtering | Good near-term extension |
| Text similarity | SentenceTransformer cosine similarity, duplicate detection | Direct baseline for OCR semantic evaluation |
| Summarization | document/product description summarization | Lower priority unless needed for reports |

**Best local angle**: Thai product-name normalization and noisy text cleaning.

## B. Information Extraction and Structured NLP

Tasks that convert unstructured text into entities, fields, relations, tables, or schema-aligned JSON.

| Subtopic | Example tasks | Fit with current work |
|---|---|---|
| Named Entity Recognition | brand, product, ingredient, medicine, lab test | Strong fit |
| Key-value extraction | test name/value/unit, product size/price/unit | Strong fit |
| Relation extraction | product-ingredient, test-value-unit relations | Medium-high fit |
| Table extraction | lab result table, nutrition facts, product specs | Strong fit with Document AI |
| Schema validation | required fields, unit consistency, range checks | Strong fit with verifier work |

**Best local angle**: Thai OCR field extraction with critical field validation.

## C. LLM-era NLP

Tasks where an LLM performs generation, judgment, correction, planning, or tool use.

| Subtopic | Example tasks | Fit with current work |
|---|---|---|
| LLM post-correction | correct OCR text while preserving protected terms | Strong fit |
| LLM-as-a-Judge | score OCR output quality | Strong fit, but should not stand alone |
| LLM-as-a-Verifier | supported / unsupported / uncertain with evidence | Highest fit for reliability |
| Agentic workflows | route OCR, call tools, retry failed fields | Medium fit after core POC |
| Prompt/rubric design | structured JSON scoring and field checks | Strong fit |

**Best local angle**: evidence-grounded LLM verifier for Thai OCR/product data.

## D. Multimodal and Document AI

NLP tasks where text is tied to images, layout, tables, or visual document structure.

| Subtopic | Example tasks | Fit with current work |
|---|---|---|
| OCR | EasyOCR, PaddleOCR, GOT-OCR, Typhoon OCR | Existing core |
| Layout detection | DocLayout-YOLO, table/region detection | Existing core |
| VLM document parsing | Typhoon OCR, Qwen2.5-VL, DocOwl | Strong extension |
| OCR-free document understanding | direct image-to-answer/document JSON | Medium-high extension |
| Image-text alignment | product image matches OCR/product text | Strong SME extension |
| Visual classification | product label vs. advertisement image | Strong SME extension |

**Best local angle**: modular OCR as default, VLM fallback for unsupported/uncertain fields.

## E. Thai / Low-Resource NLP

Language-specific work where Thai script, tokenization, mixed Thai-English text, and limited annotated data are central.

| Subtopic | Example tasks | Fit with current work |
|---|---|---|
| Thai tokenization | PyThaiNLP `newmm`, tokenizer comparison | Direct baseline |
| Thai OCR metrics | WER vs. CER vs. ANLS for Thai | High-value research gap |
| Thai product text | SME product names, units, promotions | Direct NECTEC fit |
| Thai medical/product lexicons | protected terms, unit dictionaries | Strong verifier/correction fit |
| Low-resource adaptation | LoRA/fine-tuning with small data | Later-stage extension |

**Best local angle**: tokenizer-independent Thai OCR evaluation with CER/ANLS/verifier.

## F. Evaluation, Verification, and Safety

This group measures whether outputs are correct, reliable, grounded, and safe enough for downstream use.

| Subtopic | Example tasks | Fit with current work |
|---|---|---|
| Lexical metrics | CER, WER | Existing baseline, improve with CER |
| Document metrics | ANLS, key-value F1, TED for tables | Strong upgrade |
| Semantic metrics | SentenceTransformer, BERTScore | Existing and upgrade path |
| Verifier metrics | false-pass rate, unsupported-field F1, abstention quality | Highest reliability contribution |
| Safety validation | PHI leakage, critical field review, hallucination risk | Strong medical/product safety angle |

**Best local angle**: cost-aware evaluation cascade with verifier for critical fields.

## G. Deployment and Efficiency

System-level NLP work: speed, memory, routing, fallback, cost, and reproducibility.

| Subtopic | Example tasks | Fit with current work |
|---|---|---|
| Model routing | when to call VLM vs. modular OCR | Strong practical contribution |
| Lightweight pipelines | DocLayout-YOLO + OCR + small LM | Existing core |
| Quantization | reduce VLM memory | Later-stage engineering |
| Benchmark automation | repeatable eval report for each model | Strong near-term POC |
| Human-in-the-loop | review uncertain fields | Strong verifier deployment story |

**Best local angle**: VLM fallback router driven by evaluation/verifier signals.

## Recommended Topic Separation for This Project

### Track 1 — Thai OCR Evaluation and Verification

**Core question**: How can Thai OCR output be evaluated reliably beyond WER?

Includes:
- CER / WER comparison for Thai
- ANLS / BERTScore
- LLM-as-a-Judge
- LLM-as-a-Verifier
- critical field false-pass rate

Best POC:
- `poc/ocr-evaluation-cascade/`

### Track 2 — Thai Product / SME Data Cleaning

**Core question**: Can NLP+VLM improve noisy SME product data cleaning and image filtering?

Includes:
- product-name normalization
- brand/unit/quantity preservation
- product label vs. advertisement classification
- image-text alignment
- product deduplication

Best POC:
- `poc/vlm-product-image-classifier/`

### Track 3 — Document AI / VLM Fallback

**Core question**: When should the system use a heavy VLM instead of a lightweight OCR pipeline?

Includes:
- modular OCR pipeline
- Typhoon OCR / Qwen2.5-VL comparison
- VLM fallback router
- evidence-grounded acceptance checks

Best POC:
- `poc/vlm-fallback-router/`

### Track 4 — Internal Benchmark

**Core question**: How can NECTEC measure progress across OCR, product, and VLM variants?

Includes:
- ThaiOCRBench-inspired schema
- product-label benchmark
- ad/package classification benchmark
- key-value extraction benchmark
- medical-like privacy-safe benchmark

Best POC:
- `poc/internal-ocrbench-builder/`

## Priority Recommendation

| Priority | Track | Why |
|---|---|---|
| 1 | Thai OCR Evaluation and Verification | Directly extends existing WER/cosine work and produces a clear research contribution |
| 2 | Internal Benchmark | Makes every later experiment defensible |
| 3 | Thai Product / SME Data Cleaning | Directly connects to NECTEC SME module |
| 4 | Document AI / VLM Fallback | Practical system contribution once metrics and benchmark exist |

## What Is In Scope vs. Out of Scope

### In Scope

- Thai OCR evaluation
- OCR post-correction
- product-name cleaning
- product/ad image classification
- field extraction and verification
- VLM fallback for document understanding
- benchmark creation

### Lower Priority / Out of Scope for Now

- general chatbot building
- generic summarization without OCR/product connection
- broad LLM agent frameworks unless used for OCR routing
- robotics/VLA unless the project intentionally switches away from OCR/SME work
- full medical diagnosis or clinical decision support

## One-Sentence Scope

**This project's strongest NLP scope is Thai document/product understanding: cleaning noisy Thai text, extracting structured fields from OCR/VLM outputs, and verifying critical facts with tokenizer-aware metrics and evidence-grounded LLM/VLM checks.**

