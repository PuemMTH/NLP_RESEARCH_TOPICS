# POC: DocLayout-YOLO — Document Layout Detection

> Source: <https://github.com/opendatalab/DocLayout-YOLO>

DocLayout-YOLO ใช้ YOLOv10 backbone ที่ fine-tune บน DocStructBench เพื่อตรวจจับ layout region ในเอกสาร PDF/รูปภาพ เหมาะมากสำหรับ Stage 2 (Layout Understanding) ของ pipeline OCR ทางการแพทย์ไทย

---

## Layout Classes ที่ตรวจจับได้

| ID | Label            | ใช้กับเอกสารการแพทย์ |
|----|------------------|----------------------|
| 0  | title            | หัวข้อโรค / ชื่อแบบฟอร์ม |
| 1  | plain_text       | เนื้อหาทั่วไป / บันทึกแพทย์ |
| 2  | abandon          | header / footer / เลขหน้า |
| 3  | figure           | ภาพ X-ray / กราฟ |
| 4  | figure_caption   | คำอธิบายภาพ |
| 5  | table            | ตารางยา / ผลแล็บ |
| 6  | table_caption    | หัวตาราง |
| 7  | table_footnote   | หมายเหตุตาราง |
| 8  | isolate_formula  | สูตรยา / dosage formula |
| 9  | formula_caption  | คำอธิบายสูตร |

---

## Setup

```bash
# สร้าง virtual environment (แนะนำ)
python -m venv .venv && source .venv/bin/activate

# ติดตั้ง dependencies
pip install -r requirements.txt
```

> Model weights (~120 MB) จะ download อัตโนมัติจาก HuggingFace ครั้งแรกที่รัน
> และ cache ไว้ที่ `~/.cache/huggingface/`

---

## Usage

```bash
# พื้นฐาน
python poc_runner.py --image path/to/document.png

# ปรับ confidence threshold + บันทึก JSON
python poc_runner.py --image path/to/document.png --conf 0.3 --save-json

# ใช้ GPU (ถ้ามี)
python poc_runner.py --image path/to/document.png --device 0

# เปลี่ยน output directory
python poc_runner.py --image path/to/document.png --output-dir results/
```

### Output

- `sample_outputs/<name>_annotated.png` — รูปที่วาด bounding box + label ครบ
- `sample_outputs/<name>_detections.json` — (ถ้าใส่ `--save-json`) JSON array ของทุก detection

ตัวอย่าง JSON ที่ได้:
```json
{
  "image": "/path/to/document.png",
  "total_detections": 12,
  "detections": [
    {
      "label": "title",
      "class_id": 0,
      "confidence": 0.9231,
      "bbox_xyxy": [42.0, 58.0, 780.0, 102.0]
    },
    {
      "label": "table",
      "class_id": 5,
      "confidence": 0.8754,
      "bbox_xyxy": [38.0, 310.0, 990.0, 620.0]
    }
  ]
}
```

---

## เชื่อมกับ Pipeline OCR ทางการแพทย์ไทย

```
Input image
     │
     ▼
[DocLayout-YOLO]  ◄── Stage 2: Layout Understanding
     │
     ├─ title regions ──────► OCR ► post-correction ► structured extraction
     ├─ table regions ──────► table OCR (PaddleOCR / PP-StructureV3)
     ├─ figure regions ─────► ข้ามหรือส่งต่อ vision model
     └─ abandon regions ────► ตัดออกก่อน OCR main content
```

---

## ข้อจำกัด (Thai Medical Context)

- โมเดลฝึกบนเอกสารภาษาอังกฤษเป็นหลัก — layout ไทยอาจจำแนกผิดบางส่วน
- ฟอร์มใบสั่งยา/ใบรับรองแพทย์ที่สแกนมีคุณภาพต่ำอาจให้ confidence ต่ำ
- แนะนำ `--conf 0.15–0.25` สำหรับเอกสารสแกน; `--conf 0.3+` สำหรับ PDF render

---

## Next Steps

- [ ] ทดสอบบนตัวอย่างเอกสารการแพทย์ไทย (ฟอร์ม OPD, lab report, discharge summary)
- [ ] วัด mAP เทียบ baseline บน Thai document dataset
- [ ] Fine-tune ด้วย domain-specific samples ถ้า recall ต่ำ
- [ ] เชื่อม output JSON เข้า Stage 3 (PaddleOCR per region)
