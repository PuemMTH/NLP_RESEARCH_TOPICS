# NLP Research Topics — Claude Code Project

## Project Overview

This workspace is a research lab for Thai medical OCR and NLP topics. It contains:
- `poc/` — Proof-of-concept implementations for OCR/NLP tools
- `research/` — Literature, references, ideas, and diagrams
- `.claude/agents/` — Subagent definitions (auto-loaded by Claude Code)

---

## Subagents (Auto-Loaded)

Claude Code loads agents from `.claude/agents/` automatically. Three agents are active:

### POC Builder — `.claude/agents/poc-builder.md`
**Auto-trigger on any of these keywords:**
- `poc`, `proof of concept`, `ขึ้น poc`, `ลอง`, `ทดสอบ model`
- `รัน model`, `demo`, `prototype`, `quick test`
- `experiment code`, `pipeline prototype`, `ต่อ pipeline`
- A GitHub repo URL or library name with intent to run it

**What it does:** Scaffolds and runs POC code under `poc/<slug>/` using uv. Always GPU-first, always CLI-driven.

### Research Assistant — `.claude/agents/research-assistant.md`
**Auto-trigger on any of these keywords:**
- `research`, `find references`, `หา reference`, `analyze sources`
- `literature review`, `explore topic`, `generate research ideas`
- `summarize paper`, `related work`, `discuss`, `คุย`, `วิเคราะห์`
- A paper title, arXiv URL, or "what papers cover X?"

**What it does:** Runs the source → reference mining → analysis → topic mapping → idea generation loop. Saves everything to `research/`.

### Diagram Builder — `.claude/agents/diagram-builder.md`
**Auto-trigger on any of these keywords:**
- `graph`, `กราฟ`, `sankey`, `diagram`, `แผนภาพ`, `แผนผัง`, `วาด`
- `chart`, `plot`, `visualization`, `แสดงผล`, `สร้าง diagram`
- `latex`, `formula`, `สมการ`, `สูตร`
- Any explanation/comparison that would benefit from a visual (pipeline, flow, architecture, proportion)

**What it does:** Reads `templates/diagram-template.html`, injects a filled `CONFIG` object (sankey / mermaid / latex / plotly), writes the output to `output/diagrams/<slug>-<date>.html`. The file can be opened directly in any browser — no server needed.

**Diagram type decision:**
| Intent | Type |
|--------|------|
| Flow / pipeline / architecture | `mermaid` |
| Topic weights / multi-level proportion | `sankey` |
| Math formula / equation | `latex` |
| Bar / line / scatter / heatmap | `plotly` |

---

## Agent Routing Rules (for main Claude context)

When the user's message matches a trigger above, **spawn the appropriate subagent immediately** — do not handle it inline. Pass the full user message as the subagent prompt with enough context.

**Priority order when ambiguous:**
1. If request mentions code/running → POC Builder
2. If request mentions graph/chart/diagram/formula → Diagram Builder
3. If request mentions papers/research/references → Research Assistant
4. If still ambiguous, ask one clarifying question.

---

## Workspace Layout

```
NLP_RESEARCH_TOPICS/
├── CLAUDE.md                        # ← this file
├── .claude/
│   └── agents/
│       ├── poc-builder.md           # POC Builder subagent
│       ├── research-assistant.md   # Research Assistant subagent
│       └── diagram-builder.md      # Diagram Builder subagent
├── templates/
│   └── diagram-template.html       # Master HTML/JS template (never edit directly)
├── output/
│   └── diagrams/                   # Generated HTML diagrams (browser-ready)
├── poc/
│   ├── doclayout-yolo/
│   ├── easyocr-thai/
│   ├── got-ocr2/
│   ├── paddleocr-v5/
│   ├── byt5-ocr-correction/
│   └── wangchanberta-correction/
└── research/
    ├── diagrams/
    ├── ideas/
    └── references/
```

---

## Thai Medical OCR Pipeline (shared context for all agents)

```
Stage 1: Preprocessing      (denoising, deskew, binarization)
Stage 2: Layout Detection   ← DocLayout-YOLO, PP-StructureV3
Stage 3: Text Recognition   ← PaddleOCR, Nougat, GOT-OCR, EasyOCR
Stage 4: Post-correction    ← ByT5, WangchanBERTa, LLM-based
Stage 5: Struct Extraction  ← table parsing, key-value extraction
Stage 6: Validation         ← schema check, compliance rules
```

Every POC and research thread connects back to this pipeline.

---

## Project-Wide Defaults

- **Package manager**: uv only — never `pip install` or `requirements.txt`
- **Python**: 3.10+
- **GPU**: CUDA cu128 index (supports RTX 50xx sm_120 Blackwell + all older)
- **File naming**: kebab-case everywhere
- **No version pins** in `pyproject.toml` — always resolve to latest
- **Commit style**: descriptive imperative ("Add GOT-OCR2 POC with Thai layout notes")

---

## Key Files

| Path | Purpose |
|------|---------|
| `poc/<slug>/poc_runner.py` | Main runnable for each POC |
| `poc/<slug>/run.sh` | One-shot runner (uv sync → sample → infer) |
| `templates/diagram-template.html` | Master HTML/JS template for all diagrams |
| `output/diagrams/*.html` | Generated browser-ready diagram files |
| `research/diagrams/pipeline-thai-medical-ocr-modular.md` | Master pipeline diagram (Mermaid source) |
| `research/ideas/ideas-2026-04.md` | Current active idea log |
