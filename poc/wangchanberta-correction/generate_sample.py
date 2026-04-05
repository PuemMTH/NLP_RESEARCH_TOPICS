"""Generate synthetic Thai medical texts with masked/corrupted tokens for WangchanBERTa testing."""

import json
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent / "sample_outputs" / "sample_masked_texts.json"

# Thai medical sentences with <mask> tokens where OCR errors typically occur.
# WangchanBERTa MLM predicts the most likely token at <mask> positions.
SAMPLES = [
    {
        "masked": "ผู้ป่วยมาด้วย<mask>ปวดท้องรุนแรง มีไข้สูง",
        "expected_fill": "อาการ",
        "context": "Chief complaint with masked symptom descriptor",
    },
    {
        "masked": "ผลตรวจเลือด CBC <mask> Hemoglobin 13.5 g/dL อยู่ในเกณฑ์ปกติ",
        "expected_fill": "พบว่า",
        "context": "Lab result connector",
    },
    {
        "masked": "สั่งยา Metformin 500 mg รับประทาน<mask>เช้า-เย็น ก่อนอาหาร",
        "expected_fill": "วันละ",
        "context": "Drug prescription dosage frequency",
    },
    {
        "masked": "นัดตรวจ<mask>อีก 2 สัปดาห์ ที่แผนกอายุรกรรม",
        "expected_fill": "ซ้ำ",
        "context": "Follow-up appointment",
    },
    {
        "masked": "ค่า<mask>ในเลือดสูงกว่าปกติ สงสัยเบาหวาน",
        "expected_fill": "น้ำตาล",
        "context": "Lab value — diabetes screening",
    },
    {
        "masked": "ผู้ป่วยแพ้ยา Penicillin ห้าม<mask>ยากลุ่ม Beta-lactam",
        "expected_fill": "สั่ง",
        "context": "Drug allergy warning",
    },
    {
        "masked": "ความดัน<mask> 140/90 mmHg สูงกว่าเกณฑ์",
        "expected_fill": "โลหิต",
        "context": "Blood pressure reading",
    },
    {
        "masked": "แนะนำ<mask>อายุรแพทย์เพื่อตรวจเพิ่มเติม",
        "expected_fill": "พบ",
        "context": "Referral recommendation",
    },
]


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(SAMPLES, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[✓] Sample masked texts saved → {OUTPUT_PATH}  ({len(SAMPLES)} samples)")


if __name__ == "__main__":
    main()
