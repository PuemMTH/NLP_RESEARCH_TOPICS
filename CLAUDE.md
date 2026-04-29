# NLP Research Topics — Claude Code Project

## Project Overview

This workspace is a research lab for Thai medical OCR and NLP topics. It contains:
- `poc/` — Proof-of-concept implementations for OCR/NLP tools
- `research/` — Literature, references, ideas, and diagrams
- `.claude/agents/` — Subagent definitions (auto-loaded by Claude Code)

---

## Subagents (Auto-Loaded)

Claude Code loads agents from `.claude/agents/` automatically. Two agents are active:

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

---

## Agent Routing Rules (for main Claude context)

When the user's message matches a trigger above, **spawn the appropriate subagent immediately** — do not handle it inline. Pass the full user message as the subagent prompt with enough context.

If the request is ambiguous (e.g. "help me with OCR"), ask one clarifying question: "Do you want to run/build code (POC Builder) or read/discuss papers (Research Assistant)?"

---

## Workspace Layout

```
NLP_RESEARCH_TOPICS/
├── CLAUDE.md                        # ← this file
├── .claude/
│   └── agents/
│       ├── poc-builder.md           # POC Builder subagent
│       └── research-assistant.md   # Research Assistant subagent
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
| `research/diagrams/pipeline-thai-medical-ocr-modular.md` | Master pipeline diagram |
| `research/ideas/ideas-2026-04.md` | Current active idea log |
