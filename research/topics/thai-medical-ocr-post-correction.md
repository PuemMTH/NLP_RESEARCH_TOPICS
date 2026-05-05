# Last Updated: 2026-05-06 (VLM Thai OCR deep research indexed)

# Topic: Thai Medical OCR + Post-correction

## Included Sources
- thai-medical-ocr-post-correction-2026-03-31.md
- [/research/ideas/experiment-plan-thai-medical-ocr-2026-03-31.md](/research/ideas/experiment-plan-thai-medical-ocr-2026-03-31.md)
- [/research/ideas/draft-proposal-thai-medical-ocr-masters-2026-03-31.md](/research/ideas/draft-proposal-thai-medical-ocr-masters-2026-03-31.md)
- [/research/diagrams/pipeline-thai-medical-ocr-modular.md](/research/diagrams/pipeline-thai-medical-ocr-modular.md)
- [/research/diagrams/system-comparison-ocr-abcd.md](/research/diagrams/system-comparison-ocr-abcd.md)
- [/research/references/refs-ocr-pipeline-papers-2026-04.md](/research/references/refs-ocr-pipeline-papers-2026-04.md)
- [/research/references/refs-cited-by-ocr-pipeline-papers-2026-04.md](/research/references/refs-cited-by-ocr-pipeline-papers-2026-04.md)
- [/research/references/refs-vlm-thai-ocr-extension-2026-05.md](/research/references/refs-vlm-thai-ocr-extension-2026-05.md)
- [/research/ideas/ideas-vlm-thai-ocr-extension-2026-05.md](/research/ideas/ideas-vlm-thai-ocr-extension-2026-05.md)
- [/research/topics/nlp-scope-and-topic-map-2026-05-06.md](/research/topics/nlp-scope-and-topic-map-2026-05-06.md)

## Topic Summary
This topic connects Thai OCR model design, medical-document extraction requirements, and post-OCR correction reliability. It is highly aligned with practical pipeline work involving FastAPI services, OCR processing, and medical data constraints.

## NLP Scope Link

The broader NLP scope is separated in [/research/topics/nlp-scope-and-topic-map-2026-05-06.md](/research/topics/nlp-scope-and-topic-map-2026-05-06.md). The strongest project scope is Thai document/product understanding: cleaning noisy Thai text, extracting structured fields from OCR/VLM outputs, and verifying critical facts with tokenizer-aware metrics and evidence-grounded LLM/VLM checks.

## Subtopics
- Thai script-aware OCR and layout reconstruction
- Medical visual information extraction (field-level exactness)
- LLM-based post-correction under low-resource constraints
- Evaluation and deployment trade-offs (quality vs compute)

## Open Threads
- Build a Thai medical OCR benchmark slice (reports/prescriptions/scans)
- Compare OCR-only vs OCR+LLM post-correction with strict medical term preservation
- Test PHI-safe processing and de-identification impact on OCR quality
- Extend prior NECTEC OCR evaluation work into deterministic metrics + embedding similarity + LLM-as-a-Judge reliability scoring
- Add evidence-grounded LLM-as-a-Verifier for critical OCR fields: supported / unsupported / uncertain with evidence spans

## POC Results Update (2026-05-06)

Three follow-up items have concrete results:

1. **VLM zero-shot classifier**: `poc/vlm-zero-shot-classifier/` classified both sample images correctly with confidence 0.95. The VLM agreed with the legacy 700-character rule for both product and advertisement samples, and fallback was not used.
2. **3-layer OCR evaluation stack**: `poc/ocr-eval-3layer/` confirmed severe Thai tokenizer drift in WER. The largest observed drift was 360 percentage points (`pair_02`: newmm 400% vs attacut 40%), while CER remained tokenizer-independent.
3. **Typhoon OCR LoRA research**: `research/ideas/idea6-lora-finetune-typhoon-ocr-2026-05.md` identifies the correct model slug as `scb10x/typhoon-ocr1.5-2b`, recommends bf16 LoRA on RTX 50xx/Blackwell instead of unstable 4-bit QLoRA, and notes that no public Thai medical OCR dataset exists.

Updated diagram report: [/output/diagrams/poc-results-vlm-eval-lora-2026-05-06.html](/output/diagrams/poc-results-vlm-eval-lora-2026-05-06.html)

## Why VLM Helps with Complex Thai Medical Layouts

- VLM reads both visual structure and text, so it can use spatial cues (table cells, headers, stamps, handwritten notes) that OCR-only pipelines often miss.
- Thai script has no explicit word boundaries in many contexts, and medical forms mix Thai-English terms, abbreviations, and numbers; VLM can leverage document context to reduce segmentation and label-association errors.
- For medical documents, correctness is often field-level (patient name, test name, value, unit, reference range), not just line-level text quality. VLMs are better suited for query-driven extraction into structured fields.

## Practical Pipeline (Draft)

1. Document preprocessing (denoise, perspective correction, region proposal).
2. VLM-based parsing for text + layout + key-value candidates.
3. Post-correction with constrained language model (medical lexicon + unit patterns).
4. Schema mapping to JSON fields for downstream FastAPI services.
5. Validation rules (range checks, unit consistency, mandatory field checks).

## Evaluation Notes

- Text quality: CER, WER.
- Extraction quality: field-level exact match, key-value F1.
- Safety quality: PHI leakage rate after processing.
- Clinical robustness: medical-term preservation rate (avoid over-correction).
- Semantic reliability: SentenceTransformer cosine similarity plus optional LLM judge scores for meaning preservation, numeric preservation, unit preservation, and over-correction risk.

## NECTEC NLP-to-LLM Extension (2026-05-05)

Prior NECTEC NLP work on SME product-name cleaning and OCR evaluation can be extended into an LLM/VLM research line:

- SME text cleaning baseline: PyThaiNLP `newmm`, regex language filtering, symbol/emoji cleanup, word-frequency thresholding, and text-length heuristics.
- OCR evaluation baseline: Thai-tokenized WER and SentenceTransformer cosine similarity.
- LLM extension: constrained product-name normalization, LLM-as-a-Judge OCR evaluation, VLM-based text-heavy image classification, and constrained LLM post-OCR correction.

Related idea note: [/research/ideas/ideas-2026-05.md](/research/ideas/ideas-2026-05.md)
Related references: [/research/references/refs-nectec-nlp-llm-extension-2026-05.md](/research/references/refs-nectec-nlp-llm-extension-2026-05.md)

## LLM-as-a-Verifier Extension (2026-05-06)

LLM-as-a-Judge gives quality scores, but LLM-as-a-Verifier should answer whether each extracted field is supported by evidence. This is better aligned with OCR safety because medical and product documents contain critical exact fields such as numeric values, units, dates, dosage, brand, and product/medical terms.

Proposed verifier labels:

- `supported`: field is backed by OCR text, image crop, or reference evidence.
- `unsupported`: field contradicts or is absent from evidence.
- `uncertain`: evidence is too noisy or ambiguous for a safe decision.

Related idea note: [/research/ideas/ideas-llm-as-verifier-2026-05.md](/research/ideas/ideas-llm-as-verifier-2026-05.md)
Related references: [/research/references/refs-llm-as-verifier-2026-05.md](/research/references/refs-llm-as-verifier-2026-05.md)

## VLM Thai OCR Deep Research (2026-05-06)

Additional research from the VLM Thai OCR HTML and reference set identified a stronger direction: build an internal Thai product/medical OCR benchmark, then evaluate modular OCR, Thai-specific VLMs, and general VLMs under the same metric stack.

Key additions:

- ThaiOCRBench provides a practical schema and task taxonomy for internal benchmark design.
- Typhoon OCR is a strong Thai-English document parsing baseline but should be paired with verifier/validation due to hallucination risk.
- Qwen2.5-VL is the main general VLM baseline to compare against Thai-specific models.
- DocOwl-style work supports layout/structure-aware OCR-free document understanding, especially for tables and multi-page documents.
- Existing Thai/multilingual CLIP-like models mean the research gap should be framed as under-validated Thai product-label image-text alignment, not total absence of Thai CLIP.

Related source synthesis: [/research/sources/vlm-thai-ocr-reference-deep-dive-2026-05-06.md](/research/sources/vlm-thai-ocr-reference-deep-dive-2026-05-06.md)
Related idea note: [/research/ideas/ideas-vlm-thai-ocr-deep-research-2026-05-06.md](/research/ideas/ideas-vlm-thai-ocr-deep-research-2026-05-06.md)
Related architecture map: [/research/diagrams/vlm-thai-ocr-architecture-map-2026-05-06.md](/research/diagrams/vlm-thai-ocr-architecture-map-2026-05-06.md)

---

## Concepts Glossary

### Noise (ในบริบท OCR เอกสารการแพทย์)
สิ่งรบกวนที่ทำให้ OCR อ่านภาพผิดพลาด แบ่งเป็น 3 กลุ่ม:
- **จากการถ่าย/สแกน**: ภาพเอียง บิดเบี้ยว แสงไม่สม่ำเสมอ เงา ความละเอียดต่ำ ภาพเบลอ
- **จากตัวเอกสาร**: กระดาษเก่า รอยพับ หมึกจาง ตราประทับทับข้อความ ลายมือแพทย์
- **จาก layout**: ตารางซ้อน เส้นชิด ตัวอักษรเล็ก ค่าตัวเลขและหน่วยอยู่ใกล้กัน

### Post-Correction
ขั้นตอนแก้ไขข้อความที่ OCR อ่านแล้วก่อนส่งต่อ:
- **Rule-based**: regex แก้ pattern ที่รู้อยู่แล้ว
- **LM-based (Unconstrained)**: โมเดลภาษาอ่านบริบทแล้วเดาคำที่ถูก — เสี่ยงแก้ศัพท์แพทย์ผิด
- **Constrained**: ล็อก medical lexicon + กฎหน่วยวัด ป้องกันการแก้ที่อันตรายเชิงคลินิก

### ความแตกต่างระหว่าง 4 ระบบ

| ระบบ | เข้าใจ Layout | ทนต่อ Noise | ปลอดภัย Medical Term | ความเร็ว |
|---|---|---|---|---|
| A: OCR-only | ❌ | ต่ำ | ✅ (ไม่แตะ) | เร็วสุด |
| B: OCR+LM | ❌ | ปานกลาง | ❌ เสี่ยง | ปานกลาง |
| C: OCR+Constrained | ❌ | ปานกลาง | ✅ | ปานกลาง |
| D: VLM+Constrained | ✅ | สูง | ✅ | ช้ากว่า แต่แม่นกว่า |

VLM ทนต่อ Noise ได้ดีกว่าเพราะไม่ได้แค่ "อ่านพิกเซล" แต่ "เข้าใจว่าฟิลด์นี้ควรมีอะไร" จากบริบทรอบข้าง

---

## Modular Lightweight Pipeline (ทางเลือกเบากว่า VLM เดี่ยว)

แทนที่จะให้ VLM ตัวเดียวรับทุกอย่าง ให้แยกเป็นชิ้นเล็กๆ เฉพาะทาง:

```
ภาพ
 │
 ▼
[1] Preprocessing       ← OpenCV
    denoise, deskew, binarize
 │
 ▼
[2] Layout Detection    ← DocLayout-YOLO (~30 MB)
    detect: ตาราง, หัวข้อ, ช่องฟอร์ม
 │
 ▼
[3] OCR per region      ← EasyOCR Thai (~200 MB)
    อ่านข้อความใน region ที่ detect มา
 │
 ▼
[4] Post-correction     ← ByT5-small หรือ WangchanBERTa
    + Medical Lexicon Lock (~300–400 MB)
 │
 ▼
[5] Field Structuring   ← Regex + Rules
    → JSON schema → FastAPI
```

### Tool Stack Reference

| ขั้นตอน | Tool | ขนาด | หมายเหตุ |
|---|---|---|---|
| Preprocessing | OpenCV | ~0 MB | ใช้อยู่แล้ว |
| Layout Detection | **DocLayout-YOLO** | ~30 MB | คล้าย YOLO11 ที่รู้จัก |
| OCR | **EasyOCR Thai** | ~200 MB | ใช้อยู่แล้ว |
| Post-correction | **ByT5-small** | ~300 MB | character-level, ไม่ต้อง tokenize Thai |
| Post-correction (Thai) | **WangchanBERTa** | ~400 MB | Thai BERT จาก NECTEC/VISTEC |
| Field Structuring | Regex + Rules | ~0 MB | ไม่ต้องโมเดล |

**รวม ~930 MB** vs Typhoon OCR VLM (~5–10x หนักกว่า)

### จุดสำคัญ
- Layout Detection (ขั้นที่ 2) คือหัวใจ — detect region ถูก ที่เหลือง่ายขึ้นมาก
- WangchanBERTa มาจาก NECTEC/VISTEC ตรง context งานที่ NECTEC โดยตรง
- ByT5-small ทำงานระดับ character ไม่ต้อง word tokenizer ภาษาไทย

---

## OCR Broad Context (2026-04-05)

### ภาพใหญ่ของสนาม OCR
- OCR ไม่ได้จบที่ text transcription อีกต่อไป แต่เป็น end-to-end document understanding pipeline.
- งานที่เด่นขึ้นคือ layout-aware recognition, field-level extraction, และ post-correction ที่ควบคุมข้อผิดพลาดเชิงโดเมน.
- ในโดเมนการแพทย์ ความถูกต้องระดับ field (ค่า, หน่วย, ชื่อการทดสอบ) สำคัญกว่าคะแนนข้อความรวมเพียงอย่างเดียว.

### 4 แกนวิจัยหลักที่กำลังเร่ง
- Image quality and restoration: ลด noise ที่ทำให้ downstream error สะสม.
- Layout and multimodal parsing: เข้าใจโครงสร้างเอกสาร ไม่ใช่แค่อ่านทีละบรรทัด.
- Constrained post-correction: ใช้ lexicon/rules เพื่อลด over-correction ของคำเฉพาะทาง.
- Reliability and compliance: วัดความเสี่ยง PHI leakage, consistency, และ fail-safe behavior.

### แนวโน้มประเมินผล
- จาก CER/WER อย่างเดียว ไปสู่ metric ผสม: field-level exact match, key-value F1, term-preservation, latency/memory.
- เน้นรายงาน failure mode และ recovery strategy มากขึ้น โดยเฉพาะเอกสาร noisy และ layout ซับซ้อน.

### Related Diagram
- [/research/diagrams/ocr-research-landscape-2026-04-05.md](/research/diagrams/ocr-research-landscape-2026-04-05.md)

---

## POC Log

| วันที่ | Tool | Stage | ไฟล์ | สถานะ |
|--------|------|-------|------|--------|
| 2026-04-05 | DocLayout-YOLO | Stage 2: Layout Detection | [/poc/doclayout-yolo/](/poc/doclayout-yolo/) | ✅ Run success (RTX 5070, cu128, 13 detections) |
| 2026-04-05 | EasyOCR Thai | Stage 3: Text Recognition | [/poc/easyocr-thai/](/poc/easyocr-thai/) | ✅ PASS — 42 regions (sample), 107 regions (real paper) |
| 2026-04-06 | PaddleOCR v5 | Stage 3: Text Recognition | [/poc/paddleocr-v5/](/poc/paddleocr-v5/) | ✅ PASS — 8 regions (sample), 53 regions (real paper); HF transformers backend |
| 2026-04-05 | GOT-OCR2.0 | Stage 3: Text Recognition (VLM) | [/poc/got-ocr2/](/poc/got-ocr2/) | ✅ PASS — 53 lines/2978 chars (real paper, 6.9s) |
| 2026-04-05 | ByT5-small | Stage 4: Post-correction | [/poc/byt5-ocr-correction/](/poc/byt5-ocr-correction/) | ✅ PASS — 8 samples, 0/8 exact (pretrained base, not fine-tuned) |
| 2026-04-05 | WangchanBERTa | Stage 4: Post-correction (MLM) | [/poc/wangchanberta-correction/](/poc/wangchanberta-correction/) | ✅ PASS — 8 samples, 1/8 exact (pretrained MLM) |
| 2026-05-06 | 3-Layer OCR Eval (CER/ANLS*/BERTScore) | Stage 6: Validation / Evaluation | [/poc/ocr-eval-3layer/](/poc/ocr-eval-3layer/) | ✅ PASS — 5 Thai medical pairs; demonstrates tokenizer drift (up to 100pp WER gap); L3 WangchanBERTa layer-9 |

### 2026-04-05 — DocLayout-YOLO POC
- **Source**: <https://github.com/opendatalab/DocLayout-YOLO>
- **Stage**: 2 — Layout Understanding
- **Model**: `juliozhao/DocLayout-YOLO-DocStructBench` (~120 MB, HuggingFace)
- **Detects**: title, plain_text, abandon, figure, figure_caption, table, table_caption, table_footnote, isolate_formula, formula_caption
- **CLI**: `python poc/doclayout-yolo/poc_runner.py --image doc.png --save-json`
- **Integration point**: JSON output (label + bbox_xyxy + confidence) feeds directly into Stage 3 — crop each region and pass to PaddleOCR/EasyOCR
- **Thai caveats**: Model trained on English-heavy data; test on Thai forms with `--conf 0.15` first; consider fine-tuning if recall on Thai table layouts is <0.6

### 2026-05-06 — 3-Layer OCR Evaluation Stack POC
- **Source**: custom implementation (CER via jiwer, ANLS* via anls, BERTScore direct transformers)
- **Stage**: 6 — Validation / Evaluation (replaces Module 2: WER + cosine sim)
- **Model**: `airesearch/wangchanberta-base-att-spm-uncased` for L3 BERTScore
- **Metrics**: L1 CER (tokenizer-agnostic), L2 ANLS* (threshold 0.5), L3 BERTScore-F1 (WangchanBERTa layer 9)
- **CLI**: `uv run python poc/ocr-eval-3layer/poc_runner.py --test-suite sample_outputs/test_pairs.json --save-json out.json`
- **Key finding**: WER tokenizer drift demonstrated — pair_02 shows 400% (newmm) vs 500% (longest) on the same OCR output. CER stays at 11.1%.
- **Integration point**: JSON output feeds quality signal back into Stage 4 post-correction training loop
- **Thai caveats**: BERTScore uses raw cosine similarity (no baseline rescaling) — values not directly comparable to English BERTScore benchmarks. WangchanBERTa was pretrained on Thai Wikipedia/news; fine-tuning on medical Thai would improve medical term discrimination.
