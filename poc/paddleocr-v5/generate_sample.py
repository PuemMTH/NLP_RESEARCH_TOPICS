"""Generate a synthetic Thai+English medical document for PaddleOCR testing."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 600
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
        ("ใบสั่งยา — Prescription Order", 24),
        ("โรงพยาบาลกรุงเทพ — Bangkok Hospital", 16),
        ("", 10),
        ("ชื่อผู้ป่วย: นางสาวพิมพ์ใจ สุขสันต์    HN: 12345678", 14),
        ("วันที่: 5 เมษายน 2569    แพทย์: นพ.วิชัย รักษา", 14),
        ("", 10),
        ("1. Amoxicillin 500 mg  cap  #30  Sig: 1 cap tid pc", 14),
        ("2. Paracetamol 500 mg  tab  #20  Sig: 1-2 tab q4-6h prn", 14),
        ("3. Omeprazole 20 mg  cap  #14  Sig: 1 cap od ac breakfast", 14),
        ("", 10),
        ("หมายเหตุ: ผู้ป่วยแพ้ Penicillin — ให้ระวังการสั่งยากลุ่ม Beta-lactam", 14),
    ]

    y = 30
    for text, size in lines:
        if text:
            draw.text((40, y), text, fill="black", font=get_font(size))
        y += size + 12

    draw.rectangle([20, 10, W - 20, H - 10], outline="gray", width=1)
    img.save(IMG_PATH, "PNG")
    print(f"[✓] Sample prescription image saved → {IMG_PATH}")


if __name__ == "__main__":
    main()
