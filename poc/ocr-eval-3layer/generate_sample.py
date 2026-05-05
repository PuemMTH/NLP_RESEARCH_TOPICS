"""
generate_sample.py — Creates sample_outputs/test_pairs.json with 5 Thai medical
OCR test pairs (reference text + realistic hypothesis with OCR errors).

Run:
    uv run python generate_sample.py
"""
import json
import pathlib

OUTPUT_DIR = pathlib.Path(__file__).parent / "sample_outputs"
OUTPUT_FILE = OUTPUT_DIR / "test_pairs.json"


TEST_PAIRS = [
    {
        "id": "pair_01",
        "description": "Medication name — missing tone mark",
        "reference": "ยาแก้ปวดหัว",
        "hypothesis": "ยาแกปวดหว",
    },
    {
        "id": "pair_02",
        "description": "Diagnosis — vowel substitution",
        "reference": "โรคความดันโลหิตสูง",
        "hypothesis": "โรคความดันโลหตสง",
    },
    {
        "id": "pair_03",
        "description": "Drug dosage — digit confusion + missing unit",
        "reference": "รับประทานวันละ 2 เม็ด หลังอาหาร",
        "hypothesis": "รบประทานวนล 2 เมด หลงอาหาร",
    },
    {
        "id": "pair_04",
        "description": "Allergy note — consonant cluster drop",
        "reference": "แพ้ยาเพนิซิลลิน",
        "hypothesis": "แพยาเพนซลน",
    },
    {
        "id": "pair_05",
        "description": "Lab result — near-perfect with one character swap",
        "reference": "ผลเลือดปกติ น้ำตาลในเลือด 95 mg/dL",
        "hypothesis": "ผลเลือดปกติ น้ำตาลในเลอด 95 mg/dL",
    },
]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(TEST_PAIRS, f, ensure_ascii=False, indent=2)
    print(f"[generate_sample] Wrote {len(TEST_PAIRS)} test pairs → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
