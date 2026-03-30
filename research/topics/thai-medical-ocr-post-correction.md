# Last Updated: 2026-03-31 (concepts indexed)

# Topic: Thai Medical OCR + Post-correction

## Included Sources
- thai-medical-ocr-post-correction-2026-03-31.md
- ../ideas/experiment-plan-thai-medical-ocr-2026-03-31.md
- ../ideas/draft-proposal-thai-medical-ocr-masters-2026-03-31.md

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
