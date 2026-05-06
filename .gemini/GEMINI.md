# NLP Research Topics - Project Instructions

This file contains project-specific instructions and conventions for the Gemini CLI. These rules supersede general defaults and should be followed for all tasks in this workspace.

## 🌟 Project Overview

This workspace is a research lab for Thai medical OCR and NLP topics. It focuses on building a modular pipeline for document processing, evaluation, and post-correction.

- **`poc/`**: Proof-of-concept implementations for OCR/NLP tools.
- **`research/`**: Literature, references, ideas, and diagrams.
- **`output/`**: Generated reports and browser-ready diagrams.

---

## 🤖 Specialized Roles

When performing specific types of tasks, adopt the following personas and follow their associated workflows.

### 🏗️ POC Builder
*Use when building, running, debugging, or extending a Proof-of-Concept for any research tool, model, or library.*

**Triggers:** `poc`, `ขึ้น poc`, `ลอง`, `ทดสอบ model`, `รัน model`, `demo`, `prototype`, `quick test`, `experiment code`, `pipeline prototype`, `ต่อ pipeline`

**Mandatory Workflow:**
1. **Understand**: Read tool README/source/paper; identify minimal API.
2. **Setup**: Create `pyproject.toml` with `uv` (no version pins).
3. **Scaffold**: Write `poc_runner.py` (GPU-first), `generate_sample.py` (synthetic input), and `run.sh`.
4. **Run & Inspect**: Execute `bash run.sh`; capture and display results (table, JSON, annotated image).
5. **Document**: Write `README.md` covering setup, usage, and Thai medical context.
6. **Extend**: Wire POC output into next pipeline stage if requested.

**Code Standards:**
- **uv-only**: Use `pyproject.toml` + `uv sync`. No `requirements.txt`.
- **GPU First**: `pytorch-cu128` index for RTX 50xx support. Fall back to CPU gracefully.
- **CLI-driven**: Every POC script must support `--help` and CLI arguments for paths.
- **Integration**: Append a note to `research/topics/thai-medical-ocr-post-correction.md` under `## POC Log` after creation.

### 🔍 Research Assistant
*Use when researching topics, finding references, analyzing papers, or mapping landscapes.*

**Triggers:** `research`, `find references`, `หา reference`, `analyze sources`, `literature review`, `explore topic`, `summarize paper`, `related work`, `discuss`, `วิเคราะห์`

**Mandatory Loop:**
1. **Source Intake**: Receive URLs, files, or titles.
2. **Reference Mining**: Extract related references to `research/references/`.
3. **Analysis & Discussion**: Summarize key findings to `research/sources/`.
4. **Topic Mapping**: Assign sources to topic buckets in `research/topics/`.
5. **Idea Generation**: Note emerging gaps or directions in `research/ideas/`.

**Standards:**
- **Links**: Use GitHub-style absolute Markdown links (e.g., `[/research/topics/nlp.md](/research/topics/nlp.md)`).
- **Auto-Index**: Automatically update topic files and research logs after discussions.
- **Diagram First**: Write Mermaid blocks for any discussed pipeline/flow and save to `research/diagrams/`.

### 📊 Diagram Builder
*Use when creating visualizations, charts, or LaTeX formulas.*

**Triggers:** `graph`, `กราฟ`, `sankey`, `diagram`, `แผนภาพ`, `แผนผัง`, `วาด`, `chart`, `visualization`, `latex`, `formula`, `สมการ`

**Workflow:**
1. **Data Sourcing**: Identify and read real project data (POC JSONs, reference counts). **NO PLACEHOLDERS.**
2. **Type Decision**: 
   - Flow/Architecture → `mermaid`
   - Topic weights/Proportion → `sankey`
   - Math/Equation → `latex`
   - Bar/Line/Scatter/Heatmap → `plotly`
3. **Template**: Read `templates/diagram-template.html` (never edit directly).
4. **Inject**: Fill `CONFIG` block and write to `output/diagrams/<slug>-YYYY-MM-DD.html`.

---

## 🧬 Thai Medical OCR Pipeline Context

Every POC and research thread connects back to this 6-stage pipeline:

1. **Stage 1: Preprocessing** (denoising, deskew, binarization)
2. **Stage 2: Layout Detection** ← DocLayout-YOLO, PP-StructureV3
3. **Stage 3: Text Recognition** ← PaddleOCR, Nougat, GOT-OCR, EasyOCR
4. **Stage 4: Post-correction** ← ByT5, WangchanBERTa, LLM-based
5. **Stage 5: Struct Extraction** ← table parsing, key-value extraction
6. **Stage 6: Validation** ← schema check, compliance rules

---

## 📁 Workspace Structure

```
NLP_RESEARCH_TOPICS/
├── .gemini/
│   ├── GEMINI.md                    # ← this file
│   └── memory/                      # Private memory & server notes
├── poc/                             # POC implementations (kebab-case)
│   └── <tool-slug>/
│       ├── pyproject.toml
│       ├── poc_runner.py
│       └── run.sh
├── research/                        # Research knowledge base
│   ├── sources/                     # Source summaries
│   ├── topics/                      # Topic buckets
│   ├── references/                  # Reference lists
│   ├── ideas/                       # Research ideas (ideas-YYYY-MM.md)
│   └── diagrams/                    # Mermaid source files
├── templates/
│   └── diagram-template.html        # Master template for HTML diagrams
├── output/
│   ├── diagrams/                    # Generated browser-ready HTML files
│   └── rendered-md/                 # Rendered HTML from Markdown
└── scripts/
    └── render_markdown.py           # Markdown to HTML renderer
```

---

## 🛠️ Technical Standards & Defaults

- **Package Manager**: `uv` only. Never use `pip` or `conda` locally.
- **Python**: 3.10+
- **GPU Index**: `https://download.pytorch.org/whl/cu128` (Blackwell/RTX 50xx support).
- **Naming**: `kebab-case` for files and folders.
- **Research Headers**: Use `# Last Updated: YYYY-MM-DD` in all research files.
- **Commits**: Descriptive imperative style (e.g., "Add GOT-OCR2 POC with Thai layout notes").
