"""Generate a synthetic Thai+English medical document image for EasyOCR testing."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 700
IMG_PATH = Path(__file__).parent / "sample_outputs" / "sample_doc.png"


def get_font(size: int):
    for p in [
        "/usr/share/fonts/truetype/tlwg/TlwgMono.ttf",       # Thai font
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
    font_big = get_font(26)
    font_med = get_font(18)
    font_sm = get_font(14)

    y = 30
    draw.text((40, y), "ใบรายงานผลตรวจทางห้องปฏิบัติการ", fill="black", font=font_big)
    y += 45
    draw.text((40, y), "Laboratory Report — Bangkok General Hospital", fill="gray", font=font_med)
    y += 40
    draw.line([(40, y), (960, y)], fill="black", width=2)
    y += 15

    lines = [
        "ชื่อผู้ป่วย: นายสมชาย ใจดี       Patient ID: TH-2026-00412",
        "วันที่ตรวจ: 5 เมษายน 2569        Ward: Internal Medicine",
        "",
        "ผลการตรวจ Complete Blood Count (CBC):",
        "  WBC        14,500  /μL       (Ref: 4,000–10,000)   สูง",
        "  RBC         4.21   M/μL      (Ref: 4.50–5.90)      ต่ำ",
        "  Hemoglobin 13.1    g/dL      (Ref: 13.5–17.5)      ต่ำ",
        "  Platelet   298,000 /μL       (Ref: 150,000–400,000)",
        "  CRP         68     mg/L      (Ref: <10)            สูง",
        "",
        "ผลการตรวจ Biochemistry:",
        "  Creatinine  0.9    mg/dL     (Ref: 0.7–1.3)",
        "  BUN         18     mg/dL     (Ref: 7–20)",
        "  FBS        102     mg/dL     (Ref: 70–100)         สูง",
        "",
        "แพทย์ผู้รับผิดชอบ: พญ.สุภาพร จิตรดี   License No. 12345",
    ]

    for line in lines:
        draw.text((40, y), line, fill="black", font=font_sm)
        y += 28

    draw.rectangle([30, 20, 970, H - 20], outline="gray", width=1)
    draw.text((40, H - 40), "เอกสารนี้เป็นความลับ — ห้ามเผยแพร่", fill="red", font=font_sm)

    img.save(IMG_PATH, "PNG")
    print(f"[✓] Sample Thai medical document saved → {IMG_PATH}")
    print(f"    Size: {W}×{H} px")


if __name__ == "__main__":
    main()
