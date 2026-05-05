# NLP Research Topics — Codex Project Instructions

## Project Overview

This workspace is a research lab for Thai medical OCR and NLP research topics.

- `poc/` contains runnable proof-of-concept implementations for OCR/NLP tools.
- `research/` contains sources, references, topic notes, ideas, reports, and diagrams.
- `templates/diagram-template.html` is the master browser-ready diagram template.
- `output/diagrams/` contains generated standalone HTML diagrams.

This file is the Codex equivalent of the Claude project config in `CLAUDE.md` and `.claude/agents/`. Codex does not auto-load Claude subagents, so the subagent behavior is represented here as routing rules and task workflows.

## Claude-Compatible Priority Order

This section mirrors the routing priority in `CLAUDE.md` and is authoritative for Codex in this repository.

When a user message matches a trigger, use the corresponding workflow immediately. Codex does not spawn Claude subagents automatically, so "use the workflow" means follow the mode instructions in this file with the same priority that Claude would use to choose a subagent.

**Priority order when ambiguous:**

1. **POC Builder Mode** — if the request mentions code, running, debugging, POC, model tests, prototypes, GitHub repos, libraries, experiment code, model demos, or pipeline wiring.
2. **Diagram Builder Mode** — if the request mentions graph, chart, diagram, Sankey, visualization, LaTeX, formula, pipeline drawing, architecture, flow, comparison visuals, or the answer would clearly benefit from a visual.
3. **Research Assistant Mode** — if the request mentions papers, research, references, literature review, source analysis, topic exploration, brainstorming, discussion, idea generation, paper titles, arXiv URLs, or "what papers cover X?"
4. If still ambiguous after applying this order, ask one concise clarifying question.

Do not reorder this priority based on convenience. For example:

- "ลองรัน model แล้วสรุปผล" routes to **POC Builder Mode**, even though it also asks for a summary.
- "ทำ research แล้ววาด architecture" routes first to **Diagram Builder Mode** for the visual artifact after reading the relevant research context, unless code/running is also requested.
- "หา paper แล้ว summarize" routes to **Research Assistant Mode**.

## Trigger Keywords

Use these triggers as the practical mapping from the original Claude agents.

Thai trigger examples:

- POC: `poc`, `ขึ้น poc`, `ลอง`, `ทดสอบ model`, `รัน model`, `demo`, `prototype`, `ต่อ pipeline`
- Research: `หา reference`, `วิเคราะห์`, `คุย`, `research`, `literature review`, `related work`
- Diagram: `กราฟ`, `แผนภาพ`, `แผนผัง`, `วาด`, `สร้าง diagram`, `แสดงผล`, `สูตร`

## Project-Wide Defaults

- Use `uv` only for Python dependency management. Do not use `pip install` directly and do not add `requirements.txt` for new POCs.
- Python target is 3.10+.
- Prefer GPU-first execution for model POCs.
- Use CUDA cu128 PyTorch index by default for GPU POCs because it supports RTX 50xx / Blackwell `sm_120` and older architectures.
- Use kebab-case for new file and directory names.
- Do not pin dependency versions in new `pyproject.toml` files unless the user explicitly asks or an upstream incompatibility requires it.
- Keep generated model weights out of git. Document cache behavior and add ignore notes where relevant.
- Commit message style, when asked to commit: descriptive imperative, for example `Add GOT-OCR2 POC with Thai layout notes`.

## Thai Medical OCR Pipeline Context

Most work in this repository should connect back to this shared pipeline:

```text
Stage 1: Preprocessing      (denoising, deskew, binarization)
Stage 2: Layout Detection   (DocLayout-YOLO, PP-StructureV3)
Stage 3: Text Recognition   (PaddleOCR, Nougat, GOT-OCR, EasyOCR)
Stage 4: Post-correction    (ByT5, WangchanBERTa, LLM-based)
Stage 5: Struct Extraction  (table parsing, key-value extraction)
Stage 6: Validation         (schema check, compliance rules)
```

When adding POCs, notes, or diagrams, state which stage the work belongs to and mention Thai-specific caveats such as missing word boundaries, mixed Thai-English text, medical abbreviations, noisy scans, tables, stamps, and handwriting.

## POC Builder Mode

Use this mode for building, running, debugging, or extending proof-of-concept code.

### POC Directory Convention

New POCs live under:

```text
poc/<tool-slug>/
├── pyproject.toml
├── poc_runner.py
├── generate_sample.py
├── run.sh
├── README.md
└── sample_outputs/
    └── .gitkeep
```

Use kebab-case for `<tool-slug>`.

### Required POC Loop

1. Understand the tool by reading its README, docs, source, or paper abstract. Do not invent APIs.
2. Scaffold or update a `uv` project with unpinned dependencies.
3. Implement CLI-first runnable code in `poc_runner.py`.
4. Add `generate_sample.py` so the POC can run without real private data.
5. Add `run.sh` with `set -euo pipefail` and an end-to-end sequence.
6. Run the POC when feasible and inspect outputs.
7. Document setup, usage, output format, limitations, Thai medical OCR fit, and pipeline integration in `README.md`.
8. Append or update the POC log in `research/topics/thai-medical-ocr-post-correction.md`.

### POC Code Standards

- `poc_runner.py` must support `uv run python poc_runner.py --help`.
- CLI arguments should control input/output paths. Avoid hardcoded project-root paths.
- `--device` should default to `None` or auto-detect, not `"cpu"`.
- Resolve CUDA first, then CPU fallback. Print GPU name, compute capability, and useful CUDA details at startup when available.
- Check `torch.cuda.get_arch_list()` and handle missing architecture support clearly. For RTX 50xx / Blackwell, point to cu128 if `sm_120` is missing.
- Handle missing files, missing dependencies, model load failures, empty detections, and invalid outputs with clear `[ERROR]` or `[WARN]` messages.
- Print a human-readable summary to stdout and write structured JSON when `--save-json` is provided.
- Cache downloaded model weights through normal library caches such as Hugging Face cache. Do not re-download every run.

### `pyproject.toml` Pattern

```toml
[project]
name = "<slug>-poc"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "<package>",
    "torch",
    "torchvision",
]

[[tool.uv.index]]
name = "pytorch-cu128"
url = "https://download.pytorch.org/whl/cu128"
explicit = true

[tool.uv.sources]
torch = { index = "pytorch-cu128" }
torchvision = { index = "pytorch-cu128" }
```

### `run.sh` Pattern

```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

uv sync --no-progress --reinstall-package torch --reinstall-package torchvision
uv run python generate_sample.py
uv run python poc_runner.py --image sample_outputs/sample_doc.png --save-json
```

### POC Behavior by Request

- For a GitHub repo or library name, inspect actual docs first, then scaffold the POC.
- For `รัน` or `ลองรัน`, check required files exist, create `run.sh` if missing, then run it.
- For `GPU first`, `ใช้ GPU`, or `latest version`, ensure cu128 index and GPU-first device resolution.
- For `ต่อ pipeline` or wiring requests, read current JSON output format first, then add the smallest pipeline step needed.
- For debugging, read the relevant file fully before editing and avoid unrelated refactors.

## Research Assistant Mode

Use this mode for sources, papers, references, topic maps, literature review, idea generation, and open research discussion.

### Research Folder Convention

```text
research/
├── sources/
├── topics/
├── references/
├── ideas/
└── diagrams/
```

- Use kebab-case filenames.
- Use a `# Last Updated: YYYY-MM-DD` header in saved research files.
- Append to existing files instead of overwriting.
- Use clickable repo-root Markdown links in saved content, for example `[/research/topics/nlp-and-robotics.md](/research/topics/nlp-and-robotics.md)`.
- Do not use `../` relative links in saved research notes.

### Research Loop

1. Source Intake: accept URLs, files, paper titles, source text, or topic keywords.
2. Reference Mining: extract related work, keywords, and follow-up sources into `research/references/`.
3. Analysis: summarize claims, methods, findings, limitations, and relevance into `research/sources/`.
4. Topic Mapping: update relevant `research/topics/` files.
5. Idea Generation: append research gaps, contradictions, and concrete directions into `research/ideas/`.

When the user is discussing rather than providing a source, draw from existing files under `research/`, mark speculative claims as `Hypothesis:` or `Open question:`, and save useful new ideas or terms to the relevant research file.

### Research Constraints

- Do not fabricate citations, paper titles, author names, or claims.
- Browse the web when the user asks for current/latest sources, references, papers, or when the facts may have changed.
- Anchor claims to specific sources when presenting them as evidence.
- If a source cannot be fetched or is inaccessible, say so and do not guess its contents.
- Do not generate a final report unless the user explicitly asks for one.
- When a pipeline, architecture, comparison, or flow emerges from discussion, create a Mermaid diagram block and save it under `research/diagrams/`.

### Source Summary Format

```markdown
### Short Source Title
**Source**: URL, filename, or citation
**Topic(s)**: topic tags
**Summary**: 2-4 sentences
**Key Points**:
- ...
**Referenced / Related**:
- ...
**Ideas / Gaps**:
- ...
```

## Diagram Builder Mode

Use this mode for diagrams, charts, Sankey diagrams, Plotly visualizations, Mermaid diagrams, and LaTeX formula rendering.

### Mandatory Diagram Workflow

1. Source real project data first. Do not use placeholder values.
2. Inspect available project data before building:
   - `poc/**/sample_outputs_real_paper/*`
   - `research/**/*.md`
3. Decide diagram type:
   - `sankey` for multi-level proportions or topic flows.
   - `mermaid` for pipeline, architecture, flow, or sequence diagrams.
   - `latex` for equations and formulas.
   - `plotly` for bar, line, scatter, heatmap, and comparison charts.
4. Read `templates/diagram-template.html` before generating HTML.
5. Copy the template to `output/diagrams/<topic-slug>-<YYYY-MM-DD>.html` and replace only the `CONFIG` block in the output file.
6. Report what files were read, what values were extracted, and the output path.

### Diagram Data Sources

Prefer these real sources:

- OCR detection results: `poc/*/sample_outputs_real_paper/*.json`
- OCR text output: `poc/*/sample_outputs_real_paper/*.txt`
- Research references: `research/references/*.md`
- Research ideas: `research/ideas/*.md`
- Research diagrams: `research/diagrams/*.md`
- POC runner code: `poc/*/poc_runner.py`

If the user provides data directly, use it and label it as user-provided in `CONFIG.sources`.

### Diagram Constraints

- Never modify `templates/diagram-template.html`.
- Never write generated diagrams outside `output/diagrams/`.
- Include at least one `CONFIG.sources` entry.
- For Sankey diagrams, every link source and target must match an existing node id.
- For Mermaid diagrams, store source diagrams in `research/diagrams/` when useful for future research notes.
- For Plotly charts from confidence scores, use real extracted buckets rather than fabricated counts.

## Key Existing Files

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Original Claude Code project config |
| `.claude/agents/poc-builder.md` | Original Claude POC agent |
| `.claude/agents/research-assistant.md` | Original Claude research agent |
| `.claude/agents/diagram-builder.md` | Original Claude diagram agent |
| `templates/diagram-template.html` | Master HTML/JS template for generated diagrams |
| `research/topics/thai-medical-ocr-post-correction.md` | Main Thai medical OCR topic file and POC log |
| `research/ideas/ideas-2026-04.md` | Active idea log |
| `research/diagrams/pipeline-thai-medical-ocr-modular.md` | Master OCR pipeline diagram |
