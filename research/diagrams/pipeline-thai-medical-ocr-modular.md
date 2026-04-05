# Last Updated: 2026-03-31

# Diagram: Thai Medical OCR — Modular Lightweight Pipeline

```mermaid
flowchart TD
    IMG([📄 ภาพเอกสารการแพทย์]) --> PRE

    PRE["[1] Preprocessing\nOpenCV\ndenoise · deskew · binarize"]
    PRE --> LAY

    LAY["[2] Layout Detection\nDocLayout-YOLO ~30MB\ndetect: ตาราง · หัวข้อ · ช่องฟอร์ม"]
    LAY --> OCR

    OCR["[3] OCR per Region\nEasyOCR Thai ~200MB\nอ่านข้อความแต่ละ region"]
    OCR --> POST

    POST["[4] Post-correction\nByT5-small / WangchanBERTa ~300-400MB\n+ Medical Lexicon Lock"]
    POST --> FIELD

    FIELD["[5] Field Structuring\nRegex + Rules\nmap → JSON schema"]
    FIELD --> API([🔌 FastAPI Service])
```

## Notes
- รวม ~930 MB (เบากว่า VLM เดี่ยว 5-10x)
- ขั้นตอนที่ 2 Layout Detection คือ bottleneck หลัก — detect region ถูกแล้วที่เหลือง่าย
- WangchanBERTa มาจาก NECTEC/VISTEC เหมาะกับ context ภาษาไทยทางการแพทย์
- ByT5-small ทำงานระดับ character ไม่ต้อง word tokenizer

## Related
- Topic: [/research/topics/thai-medical-ocr-post-correction.md](/research/topics/thai-medical-ocr-post-correction.md)
- Experiment Plan: [/research/ideas/experiment-plan-thai-medical-ocr-2026-03-31.md](/research/ideas/experiment-plan-thai-medical-ocr-2026-03-31.md)
- See also: [system-comparison-ocr-abcd.md](system-comparison-ocr-abcd.md)
