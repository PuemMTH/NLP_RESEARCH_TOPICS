"""
generate_sample.py — Creates two synthetic test images + sidecar metadata

Image 1: sample_product.png
    A simple product image — plain bottle shape on white background, minimal text.
    Simulates a product photo with little to no promotional copy.
    Estimated OCR char count: ~30 chars  (well below 700-char threshold)

Image 2: sample_ad_label.png
    A text-heavy advertisement / product label image.
    Contains a large block of Thai promotional text (>700 chars).
    Simulates a label scan or ad flyer that would trigger the 700-char rule.

Both images also emit a sidecar JSON: sample_outputs/samples_metadata.json
    { "filename": "...", "image_type": "product|advertisement", "approx_char_count": N }
    The char count here is the ground-truth we generated — used by poc_runner.py
    to simulate the 700-char OCR threshold without needing a real OCR model.

Usage
-----
    uv run python generate_sample.py
    python generate_sample.py   (from the poc folder with uv activated)
"""

import json
import textwrap
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit(
        "[ERROR] Pillow is not installed. Run: uv sync"
    )

OUTPUT_DIR = Path(__file__).parent / "sample_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Font resolution — prefer NotoSansThai, fall back to NotoSerif, then default
# ---------------------------------------------------------------------------
THAI_FONT_CANDIDATES = [
    "/usr/share/fonts/noto/NotoSansThai-Regular.ttf",
    "/usr/share/fonts/noto/NotoSerifThai-Regular.ttf",
    "/usr/share/fonts/noto/NotoSansThaiLooped-SemiCondensed.ttf",
]

def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in THAI_FONT_CANDIDATES:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                continue
    print("[WARN] No Thai TTF font found — falling back to Pillow default font. "
          "Thai text will render as boxes. Install fonts-noto-core if needed.")
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Image 1 — product image (plain bottle, minimal text)
# ---------------------------------------------------------------------------

def create_product_image(out_path: Path) -> int:
    """Draw a simple product bottle. Returns approximate rendered char count."""
    W, H = 400, 600
    img = Image.new("RGB", (W, H), color=(245, 245, 250))
    draw = ImageDraw.Draw(img)

    # Bottle body
    body_x0, body_y0, body_x1, body_y1 = 130, 160, 270, 500
    draw.rounded_rectangle(
        [body_x0, body_y0, body_x1, body_y1],
        radius=40, fill=(180, 210, 240), outline=(80, 120, 180), width=3
    )

    # Bottle neck
    draw.rectangle([165, 110, 235, 165], fill=(180, 210, 240), outline=(80, 120, 180), width=3)

    # Bottle cap
    draw.rectangle([155, 90, 245, 115], fill=(60, 90, 150), outline=(30, 50, 100), width=2)

    # Highlight
    draw.ellipse([150, 200, 185, 280], fill=(220, 235, 255, 180))

    # Minimal label on bottle — just a product name
    label_font = _load_font(20)
    small_font = _load_font(14)

    draw.rectangle([145, 280, 255, 380], fill=(255, 255, 255), outline=(100, 140, 200), width=2)
    product_text = "ผลิตภัณฑ์\nแชมพู"
    draw.text((150, 290), product_text, fill=(30, 30, 60), font=label_font)
    draw.text((150, 345), "200 ml", fill=(80, 80, 100), font=small_font)

    # Bottom product code
    draw.text((W // 2 - 50, H - 50), "SKU-001234", fill=(120, 120, 140), font=small_font)

    img.save(out_path)

    # Total text rendered ≈ len of all strings combined
    rendered_text = "ผลิตภัณฑ์\nแชมพู 200 ml SKU-001234"
    approx_chars = len(rendered_text)
    print(f"[INFO] Created product image: {out_path}  (approx {approx_chars} chars)")
    return approx_chars


# ---------------------------------------------------------------------------
# Image 2 — advertisement / label image (text-heavy, >700 chars)
# ---------------------------------------------------------------------------

# Long Thai promotional text (~900+ chars) to exceed the 700-char threshold
THAI_AD_TEXT = (
    "โปรโมชั่นพิเศษ! ลดราคา 50% ทุกผลิตภัณฑ์ในร้าน\n\n"
    "สินค้าคุณภาพเยี่ยม ผ่านการรับรองมาตรฐาน อย. "
    "เหมาะสำหรับทุกสภาพผิว ไม่มีส่วนผสมของสารเคมีอันตราย "
    "ผลิตจากธรรมชาติ 100% ไม่ทดลองในสัตว์\n\n"
    "ส่วนผสมหลัก: น้ำมันมะพร้าวบริสุทธิ์, สารสกัดจากชาเขียว, "
    "วิตามิน E, โปรตีนจากน้ำนมข้าว, กลีเซอรีนธรรมชาติ\n\n"
    "วิธีใช้: ทาผลิตภัณฑ์บนบริเวณที่ต้องการ นวดเบาๆ เป็นเวลา 2-3 นาที "
    "แล้วล้างออกด้วยน้ำสะอาด ใช้ได้ทุกวัน เช้าและเย็น\n\n"
    "คำเตือน: หากเกิดการระคายเคืองให้หยุดใช้ทันทีและปรึกษาแพทย์ "
    "เก็บในที่แห้งและเย็น ห่างจากแสงแดดโดยตรง\n\n"
    "ขนาด: 200 มิลลิลิตร  ราคา: 299 บาท\n"
    "ผู้ผลิต: บริษัท เนเชอรัล บิวตี้ จำกัด\n"
    "ที่อยู่: 123 ถนนสุขุมวิท แขวงคลองเตย เขตคลองเตย กรุงเทพฯ 10110\n"
    "โทร: 02-123-4567  อีเมล: info@naturalbeauty.th\n\n"
    "หมดอายุ: ดูที่ก้นกล่อง  เลขทะเบียน อย.: 10-1-12345-6789\n"
    "ลงทะเบียนรับประกันสินค้าได้ที่ www.naturalbeauty.th\n"
)


def create_ad_label_image(out_path: Path) -> int:
    """Draw a text-heavy advertisement/label. Returns approximate rendered char count."""
    W, H = 600, 900
    img = Image.new("RGB", (W, H), color=(255, 250, 235))
    draw = ImageDraw.Draw(img)

    # Background decorative border
    draw.rectangle([10, 10, W - 10, H - 10], outline=(200, 50, 50), width=4)
    draw.rectangle([18, 18, W - 18, H - 18], outline=(200, 50, 50), width=1)

    # Header banner
    draw.rectangle([10, 10, W - 10, 80], fill=(200, 50, 50))
    header_font = _load_font(28)
    draw.text((W // 2 - 130, 22), "โปรโมชั่นพิเศษ!", fill=(255, 255, 255), font=header_font)

    # Body text — wrap and render
    body_font = _load_font(16)
    small_font = _load_font(13)

    y_cursor = 100
    line_height = 22

    for paragraph in THAI_AD_TEXT.strip().split("\n"):
        if not paragraph.strip():
            y_cursor += line_height // 2
            continue
        # Wrap at ~55 chars per line for this canvas width
        wrapped = textwrap.fill(paragraph, width=55)
        for line in wrapped.split("\n"):
            if y_cursor + line_height > H - 30:
                break
            draw.text((30, y_cursor), line, fill=(40, 30, 20), font=body_font)
            y_cursor += line_height
        y_cursor += 4

    # Footer barcode placeholder
    draw.rectangle([30, H - 80, 200, H - 30], fill=(0, 0, 0))
    draw.rectangle([35, H - 75, 195, H - 35], fill=(255, 255, 255))
    for i in range(0, 155, 6):
        draw.rectangle([37 + i, H - 72, 39 + i, H - 38], fill=(0, 0, 0))
    draw.text((210, H - 65), "8850123456789", fill=(40, 40, 40), font=small_font)

    img.save(out_path)
    approx_chars = len(THAI_AD_TEXT)
    print(f"[INFO] Created ad/label image: {out_path}  (approx {approx_chars} chars)")
    return approx_chars


# ---------------------------------------------------------------------------
# Sidecar metadata JSON
# ---------------------------------------------------------------------------

def write_metadata(records: list[dict], out_path: Path) -> None:
    out_path.write_text(json.dumps(records, ensure_ascii=False, indent=2))
    print(f"[INFO] Wrote sample metadata: {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    product_path = OUTPUT_DIR / "sample_product.png"
    ad_path = OUTPUT_DIR / "sample_ad_label.png"

    product_chars = create_product_image(product_path)
    ad_chars = create_ad_label_image(ad_path)

    metadata = [
        {
            "filename": str(product_path),
            "image_type": "product",
            "approx_char_count": product_chars,
            "threshold_decision": "product" if product_chars <= 700 else "advertisement",
        },
        {
            "filename": str(ad_path),
            "image_type": "advertisement",
            "approx_char_count": ad_chars,
            "threshold_decision": "product" if ad_chars <= 700 else "advertisement",
        },
    ]

    write_metadata(metadata, OUTPUT_DIR / "samples_metadata.json")
    print("\n[OK] Sample generation complete.")
    print(f"     Product image  : {product_path}")
    print(f"     Ad/label image : {ad_path}")
    print(f"     Metadata       : {OUTPUT_DIR / 'samples_metadata.json'}")


if __name__ == "__main__":
    main()
