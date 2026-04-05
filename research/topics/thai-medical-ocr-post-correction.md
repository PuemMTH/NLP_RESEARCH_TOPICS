# Last Updated: 2026-04-05 (modular pipeline indexed; broad OCR context added)

# Topic: Thai Medical OCR + Post-correction

## Included Sources
- thai-medical-ocr-post-correction-2026-03-31.md
- [/research/ideas/experiment-plan-thai-medical-ocr-2026-03-31.md](/research/ideas/experiment-plan-thai-medical-ocr-2026-03-31.md)
- [/research/ideas/draft-proposal-thai-medical-ocr-masters-2026-03-31.md](/research/ideas/draft-proposal-thai-medical-ocr-masters-2026-03-31.md)
- [/research/diagrams/pipeline-thai-medical-ocr-modular.md](/research/diagrams/pipeline-thai-medical-ocr-modular.md)
- [/research/diagrams/system-comparison-ocr-abcd.md](/research/diagrams/system-comparison-ocr-abcd.md)

## Topic Summary
This topic connects Thai OCR model design, medical-document extraction requirements, and post-OCR correction reliability. It is highly aligned with practical pipeline work involving FastAPI services, OCR processing, and medical data constraints.

## Subtopics
- Thai script-aware OCR and layout reconstruction
- Medical visual information extraction (field-level exactness)
- LLM-based post-correction under low-resource constraints
- Evaluation and deployment trade-offs (quality vs compute)

## Open Threads
- Build a Thai medical OCR benchmark slice (reports/prescriptions/scans)
- Compare OCR-only vs OCR+LLM post-correction with strict medical term preservation
- Test PHI-safe processing and de-identification impact on OCR quality

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
