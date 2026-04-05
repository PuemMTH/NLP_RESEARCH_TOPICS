"""
สร้าง document image สังเคราะห์สำหรับทดสอบ DocLayout-YOLO
ไม่ต้องมีไฟล์จริง — รันได้ทันทีหลัง uv sync
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1600
IMG_PATH = Path(__file__).parent / "sample_outputs" / "sample_doc.png"


def draw_text_block(draw: ImageDraw.ImageDraw, xy: tuple, text: str, size: int = 18) -> None:
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except OSError:
        font = ImageFont.load_default()
    draw.text(xy, text, fill="black", font=font)


def main() -> None:
    IMG_PATH.parent.mkdir(parents=True, exist_ok=True)

    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    # ── Title ──────────────────────────────────────────────
    draw.rectangle([60, 50, 800, 100], outline="lightgray", width=1)
    draw_text_block(draw, (70, 60), "Patient Discharge Summary — Medical Report", size=26)

    # ── Plain text paragraph ────────────────────────────────
    draw.rectangle([60, 130, 1140, 300], outline="lightgray", width=1)
    body = (
        "Patient ID: TH-2026-00412     Ward: Internal Medicine     Date: 2026-04-05\n\n"
        "Chief Complaint: Fever with chills for 3 days. On admission, temperature 38.9°C,\n"
        "BP 110/70 mmHg, HR 98 bpm. Lab results indicate elevated WBC (14,500/μL) and\n"
        "CRP 68 mg/L. Diagnosis: Community-acquired pneumonia (CAP).\n\n"
        "Treatment: IV Amoxicillin-Clavulanate 1.2 g q8h × 5 days. Patient discharged\n"
        "on oral Augmentin 625 mg bid × 7 days. Follow-up in 2 weeks."
    )
    draw_text_block(draw, (70, 140), body, size=18)

    # ── Table ───────────────────────────────────────────────
    table_x, table_y = 60, 340
    headers = ["Test", "Result", "Unit", "Reference Range", "Flag"]
    col_w = [220, 140, 120, 260, 80]
    row_h = 40

    rows = [
        ["WBC",          "14,500",  "/μL",   "4,000–10,000",  "H"],
        ["RBC",          "4.21",    "M/μL",  "4.50–5.90",     "L"],
        ["Hemoglobin",   "13.1",    "g/dL",  "13.5–17.5",     "L"],
        ["Hematocrit",   "39.2",    "%",     "41.0–53.0",     "L"],
        ["Platelet",     "298,000", "/μL",   "150,000–400,000",""],
        ["CRP",          "68",      "mg/L",  "<10",           "H"],
        ["Creatinine",   "0.9",     "mg/dL", "0.7–1.3",       ""],
    ]

    all_rows = [headers] + rows
    for r_idx, row in enumerate(all_rows):
        x = table_x
        for c_idx, (cell, cw) in enumerate(zip(row, col_w)):
            fill = "#D0E8FF" if r_idx == 0 else ("white" if r_idx % 2 == 0 else "#F8F8F8")
            draw.rectangle([x, table_y + r_idx * row_h, x + cw, table_y + (r_idx + 1) * row_h],
                           fill=fill, outline="gray", width=1)
            draw_text_block(draw, (x + 6, table_y + r_idx * row_h + 10), cell, size=16)
            x += cw

    # ── Table caption ───────────────────────────────────────
    caption_y = table_y + len(all_rows) * row_h + 6
    draw_text_block(draw, (60, caption_y), "Table 1. Complete Blood Count and Biochemistry Panel", size=14)

    # ── Figure placeholder ──────────────────────────────────
    fig_y = caption_y + 40
    draw.rectangle([60, fig_y, 560, fig_y + 280], outline="#AAAAAA", width=2)
    draw.line([60, fig_y, 560, fig_y + 280], fill="#CCCCCC", width=1)
    draw.line([560, fig_y, 60, fig_y + 280], fill="#CCCCCC", width=1)
    draw_text_block(draw, (230, fig_y + 125), "[Chest X-Ray]", size=20)

    # ── Figure caption ──────────────────────────────────────
    draw_text_block(draw, (60, fig_y + 290),
                    "Figure 1. Chest X-ray PA view showing right lower lobe consolidation.", size=14)

    # ── Abandon region (header/footer) ─────────────────────
    draw.rectangle([0, 0, W, 40], fill="#F0F0F0")
    draw_text_block(draw, (10, 10), "CONFIDENTIAL — Bangkok General Hospital — Page 1 of 1", size=13)
    draw.rectangle([0, H - 40, W, H], fill="#F0F0F0")
    draw_text_block(draw, (10, H - 28), "Generated: 2026-04-05  |  System: HIS v4.2  |  DO NOT COPY", size=13)

    img.save(IMG_PATH, "PNG")
    print(f"[✓] Sample document image saved → {IMG_PATH}")
    print(f"    Size: {W}×{H} px")


if __name__ == "__main__":
    main()
