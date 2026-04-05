"""Generate a synthetic Thai+English medical document for GOT-OCR2 testing."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 800
IMG_PATH = Path(__file__).parent / "sample_outputs" / "sample_doc.png"


def get_font(size: int):
    for p in [
        "/usr/share/fonts/truetype/tlwg/TlwgMono.ttf",
        "/usr/share/fonts/truetype/tlwg/Loma.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansThai-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> None:
    IMG_PATH.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    lines = [
        ("ผลการตรวจทางห้องปฏิบัติการ — Laboratory Report", 22),
        ("โรงพยาบาลศิริราช  Siriraj Hospital", 16),
        ("", 10),
        ("HN: 99887766    ชื่อ: นายธนพล ศรีสุข    อายุ: 45 ปี", 14),
        ("วันที่รับตรวจ: 2025-04-05    แพทย์ผู้สั่ง: พญ.กมลา วงศ์สว่าง", 14),
        ("", 10),
        ("═══════════════════════════════════════════════════════", 12),
        ("  Test                    Result     Unit      Ref Range", 12),
        ("═══════════════════════════════════════════════════════", 12),
        ("  Hemoglobin (Hb)         13.5       g/dL      13.0-17.0", 12),
        ("  Hematocrit (Hct)        40.2       %         40.0-54.0", 12),
        ("  WBC                     7,800      cells/uL  4,500-11,000", 12),
        ("  Platelet                250,000    cells/uL  150,000-400,000", 12),
        ("  FBS (น้ำตาลอดอาหาร)      126 H     mg/dL     70-100", 12),
        ("  HbA1c                   7.2 H      %         4.0-5.6", 12),
        ("  Creatinine              1.1        mg/dL     0.7-1.3", 12),
        ("  eGFR                    78         mL/min    >90", 12),
        ("═══════════════════════════════════════════════════════", 12),
        ("", 10),
        ("สรุป: ระดับน้ำตาลในเลือดสูง สงสัยเบาหวาน แนะนำพบอายุรแพทย์", 14),
        ("Impression: Elevated FBS and HbA1c — suspect DM, refer to internist", 12),
    ]

    y = 30
    for text, size in lines:
        if text:
            draw.text((40, y), text, fill="black", font=get_font(size))
        y += size + 10

    draw.rectangle([15, 10, W - 15, H - 10], outline="gray", width=1)
    img.save(IMG_PATH, "PNG")
    print(f"[✓] Sample lab report image saved → {IMG_PATH}")


if __name__ == "__main__":
    main()
