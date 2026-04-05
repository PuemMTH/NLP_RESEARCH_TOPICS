"""Generate synthetic noisy OCR text pairs for ByT5 post-correction testing."""

import json
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent / "sample_outputs" / "sample_ocr_pairs.json"

# Pairs of (noisy OCR output, correct text)
# Simulates common Thai medical OCR errors:
#   - character substitution (ก→ท, า→ๅ, น→ม)
#   - missing/extra spaces, merged words
#   - English medical term garbling
PAIRS = [
    {
        "noisy": "ผลตรวจเลือค CBC พบว่ๅ Hemoglobin 13.5 g/dL ปทติ",
        "clean": "ผลตรวจเลือด CBC พบว่า Hemoglobin 13.5 g/dL ปกติ",
    },
    {
        "noisy": "ผู้ป่วยมๅด้วยอๅกๅรปวดท้องรุนแรง มีไข้ 38.5°C",
        "clean": "ผู้ป่วยมาด้วยอาการปวดท้องรุนแรง มีไข้ 38.5°C",
    },
    {
        "noisy": "Dx: Diatretes Mellitus Type 2 uncontrollecl",
        "clean": "Dx: Diabetes Mellitus Type 2 uncontrolled",
    },
    {
        "noisy": "สั่ง Meiformin 500 mg 1x2 ac แลe Glipizide 5 mg 1x1 ac",
        "clean": "สั่ง Metformin 500 mg 1x2 ac และ Glipizide 5 mg 1x1 ac",
    },
    {
        "noisy": "WBC 7,800 cells/uL  Platelet 250, 000 cells/uL",
        "clean": "WBC 7,800 cells/uL  Platelet 250,000 cells/uL",
    },
    {
        "noisy": "นัดตรวจซ้ำ 2 สัปคาห์ ที่ OPD อายุรทรรม",
        "clean": "นัดตรวจซ้ำ 2 สัปดาห์ ที่ OPD อายุรกรรม",
    },
    {
        "noisy": "ค่ๅ eGFR 78 mL/min ค่ๅ Creatimime 1.1 mg/dL",
        "clean": "ค่า eGFR 78 mL/min ค่า Creatinine 1.1 mg/dL",
    },
    {
        "noisy": "แพ้ยๅ Penicillin หัามสั่งยๅกลุ่ม Beta—lactam",
        "clean": "แพ้ยา Penicillin ห้ามสั่งยากลุ่ม Beta-lactam",
    },
]


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(PAIRS, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[✓] Sample OCR pairs saved → {OUTPUT_PATH}  ({len(PAIRS)} pairs)")


if __name__ == "__main__":
    main()
