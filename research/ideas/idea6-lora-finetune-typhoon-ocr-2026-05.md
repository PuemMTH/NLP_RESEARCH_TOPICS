# Last Updated: 2026-05-06

# Idea 6: LoRA Fine-Tune Typhoon OCR V1.5 for Thai Medical Domain
## Implementation Plan — Ready to Run in 1–2 Days

**Context**: Stage 3 (Text Recognition) and Stage 5 (Struct Extraction) of the NECTEC Thai Medical OCR pipeline.
**Goal**: Domain-adapt `scb10x/typhoon-ocr1.5-2b` to Thai medical documents (lab results, prescriptions, referral letters, discharge summaries) using LoRA on a small in-house annotated dataset.

References: [/research/references/refs-lora-vlm-finetune-2026-05.md](/research/references/refs-lora-vlm-finetune-2026-05.md)

---

## 1. Correct Model Slug

| Field | Value |
|-------|-------|
| HuggingFace slug | `scb10x/typhoon-ocr1.5-2b` |
| Mirror slug | `typhoon-ai/typhoon-ocr1.5-2b` (same weights) |
| Base model | `Qwen/Qwen3-VL-2B-Instruct` |
| Parameters | 2B (dense, not MoE) |
| Precision | BF16 |
| License | Apache 2.0 |
| Architecture | Qwen3-VL vision encoder + language model |

---

## 2. Critical Constraint: Prompt-Lock

Typhoon OCR V1.5 is trained and evaluated with one fixed prompt. Deviating from it at inference degrades performance significantly (documented in model card).

**Canonical inference prompt (must be preserved in all fine-tuning data):**

```
Extract all text from the image.

Instructions:
- Only return the clean Markdown.
- Do not include any explanation or extra text.
- You must include all information on the page.

Formatting Rules:
- Tables: Render tables using <table>...</table> in clean HTML format.
- Equations: Render equations using LaTeX syntax with inline ($...$) and block ($$...$$).
- Images/Charts/Diagrams: Wrap in <figure>...</figure> with descriptions
- Page Numbers: Wrap in <page_number>...</page_number>
- Checkboxes: Use ☐ for unchecked and ☑ for checked boxes.
```

**Implication for data annotation**: Every training sample's `assistant` turn MUST be a valid Markdown document following these formatting rules. If you want structured field extraction (JSON), it must be a post-processing layer applied to the Markdown output — NOT a different fine-tune target format. Changing the output format will break the prompt-lock and likely degrade on non-medical documents.

---

## 3. Data Requirements

### 3.1 How Many Samples?

| Scenario | Pages | Training Samples (@ 3 epochs) | Expected Outcome |
|----------|-------|-------------------------------|-----------------|
| Minimal POC | 100 | ~300 | Domain vocabulary shift; reduced medical term errors |
| Recommended first run | 200–300 | ~600–900 | Measurable F1 improvement on lab result fields |
| Full domain adaptation | 500–1,000 | ~1,500–3,000 | Robust generalization across form types |

Empirical basis: Nanonets demonstrated meaningful improvement on Qwen2-VL-2B with 800 training samples (10 epochs). Phil Schmid achieved good VLM task adaptation with ~1,000 samples on a 7B model. For a 2B model on a more focused domain shift, 200 pages is a viable minimum.

### 3.2 Data Mix Proposal (No Public Thai Medical Dataset Exists)

No public Thai medical document OCR dataset with annotated images exists. The following in-house construction strategy is required:

| Source | Approximate Share | Notes |
|--------|------------------|-------|
| De-identified lab result forms (real) | 40% | Highest value; requires PHI scrubbing per PDPA |
| De-identified prescription slips (real) | 20% | Pharmacy-grade forms are lower PHI risk |
| Synthetic Thai medical forms | 30% | Generate using PyThaiNLP vocabulary + HTML/LaTeX templates rendered to PDF then image |
| Typhoon OCR general domain samples (replay) | 10% | Prevents catastrophic forgetting; pull from the Typhoon paper's CoSyn-style pipeline |

### 3.3 Data Format

Use LLaVA-style JSON (required by 2U1/Qwen-VL-Series-Finetune and TRL SFTTrainer):

```json
{
  "id": "medocr-lab-001",
  "image": "images/lab_result_001.png",
  "conversations": [
    {
      "from": "human",
      "value": "<image>\nExtract all text from the image.\n\nInstructions:\n- Only return the clean Markdown.\n- Do not include any explanation or extra text.\n- You must include all information on the page.\n\nFormatting Rules:\n- Tables: Render tables using <table>...</table> in clean HTML format.\n- Equations: Render equations using LaTeX syntax with inline ($...$) and block ($$...$$).\n- Images/Charts/Diagrams: Wrap in <figure>...</figure> with descriptions\n- Page Numbers: Wrap in <page_number>...</page_number>\n- Checkboxes: Use ☐ for unchecked and ☑ for checked boxes."
    },
    {
      "from": "gpt",
      "value": "# Lab Result\n\nPatient: [NAME REDACTED] ...\n\n<table><tr><th>Test</th><th>Result</th><th>Unit</th><th>Reference Range</th></tr>...</table>"
    }
  ]
}
```

### 3.4 Annotation Protocol

1. Render each page at 150–300 DPI (match Typhoon OCR's training resolution).
2. Annotate the assistant turn as a faithful Markdown transcription of all visible text.
3. Use `<table>` HTML for tabular lab values (critical: numeric values and units must be exact).
4. Redact PHI in both the image and the annotation if using real documents.
5. Quality-check: two annotators per sample; resolve disagreements on numeric fields by returning to source.
6. Split: 80% train, 10% validation, 10% held-out test.

---

## 4. Training Recipe

### 4.1 Environment Setup

```bash
# Create project directory
mkdir -p poc/typhoon-ocr-lora && cd poc/typhoon-ocr-lora

# Initialize with uv
uv init .
uv python pin 3.11

# Add dependencies (no version pins per project convention)
uv add torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
uv add transformers peft trl accelerate
uv add bitsandbytes  # verify sm_120 Blackwell support before enabling 4-bit
uv add qwen-vl-utils  # required for process_vision_info()
uv add datasets pillow

# Flash Attention 2 (install after other packages to avoid conflicts)
uv add flash-attn --no-build-isolation
```

**Blackwell (sm_120) caveat on bitsandbytes**: As of early 2026, bitsandbytes 4-bit (QLoRA) support on RTX 50xx Blackwell is not universally stable. Test with:

```python
import bitsandbytes as bnb
print(bnb.__version__)
# Run: python -c "import torch; print(torch.cuda.get_device_capability())"
# sm_120 needs bnb >= 0.44.0 with cu128 wheels
```

If QLoRA 4-bit fails or produces NaN losses, fall back to plain bf16 LoRA. The 2B model loads comfortably in ~8–10GB VRAM at bf16, leaving room for optimizer states with gradient checkpointing.

### 4.2 LoRA Configuration (Recommended for 2B Dense Qwen3-VL)

```python
from peft import LoraConfig, TaskType

lora_config = LoraConfig(
    r=16,                          # rank; start here for domain shift with small data
    lora_alpha=32,                 # alpha = 2× rank is standard
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
    target_modules=[               # 7-module set for Qwen3-VL language model
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ],
    # Freeze the vision tower on the first run.
    # Vision encoder already understands document layouts.
    # Only unlock if medical-specific visual features are needed.
    modules_to_save=None,
)
```

**Why r=16/alpha=32**: Phil Schmid's r=8 recipe was designed for a simple product-description task on 7B. The 30B-MoE recipe (r=64) is overparameterized for a 2B dense model. For a domain-shift task with 200–300 samples on a 2B model, r=16–32 is the appropriate starting point — enough capacity to shift medical vocabulary without overfitting on limited data.

**Ablation order if results are poor**:
1. Increase r to 32 (alpha=64)
2. Unfreeze vision encoder (add vision projection layers to target_modules)
3. Add more synthetic data

### 4.3 QLoRA Variant (Optional — Verify bitsandbytes First)

```python
from transformers import BitsAndBytesConfig
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
# Pass to AutoModelForCausalLM.from_pretrained(quantization_config=bnb_config)
# Note: vision encoder must remain in bf16 (set llm_int8_skip_modules or equivalent)
```

### 4.4 Training Script (TRL SFTTrainer)

```python
from transformers import AutoProcessor, AutoModelForCausalLM
from trl import SFTConfig, SFTTrainer
from peft import LoraConfig, get_peft_model
import torch

MODEL_ID = "scb10x/typhoon-ocr1.5-2b"

# Load model in bf16 (default path; switch to BnB config for QLoRA)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",  # remove if flash-attn install fails
    device_map="auto",
)
processor = AutoProcessor.from_pretrained(MODEL_ID)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Expected output: ~10–15M trainable params (0.5–0.75% of 2B)

# SFT configuration
sft_config = SFTConfig(
    output_dir="./output/typhoon-ocr-lora-medical",
    num_train_epochs=3,
    per_device_train_batch_size=2,       # safe default for 24GB; increase to 4 if memory allows
    gradient_accumulation_steps=8,       # effective batch size = 16
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,
    max_grad_norm=1.0,
    bf16=True,
    gradient_checkpointing=True,
    gradient_checkpointing_kwargs={"use_reentrant": False},
    logging_steps=10,
    save_strategy="epoch",
    eval_strategy="epoch",
    report_to="none",                    # switch to "wandb" if tracking
    dataloader_num_workers=4,
    remove_unused_columns=False,         # required for multimodal collator
)

# Custom data collator (required for Qwen3-VL image handling)
from qwen_vl_utils import process_vision_info

def collate_fn(examples):
    texts = [processor.apply_chat_template(ex["messages"], tokenize=False, add_generation_prompt=False)
             for ex in examples]
    image_inputs = [process_vision_info(ex["messages"])[0] for ex in examples]
    batch = processor(
        text=texts,
        images=image_inputs,
        return_tensors="pt",
        padding=True,
    )
    labels = batch["input_ids"].clone()
    labels[labels == processor.tokenizer.pad_token_id] = -100
    batch["labels"] = labels
    return batch

trainer = SFTTrainer(
    model=model,
    args=sft_config,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=collate_fn,
)
trainer.train()
trainer.save_model("./output/typhoon-ocr-lora-medical/final")
```

**Alternative training framework**: `2U1/Qwen-VL-Series-Finetune` (GitHub) provides a ready-made training script for Qwen3-VL with LoRA. Clone and run with the JSON dataset format described in Section 3.3. This avoids writing a custom collator.

### 4.5 Optimizer Note

Use `adamw_torch_fused` for speed, or `adamw_bnb_8bit` if GPU memory is tight:

```python
optim="adamw_torch_fused"  # add to SFTConfig
```

---

## 5. GPU Memory and Time Estimates

| Configuration | VRAM Usage | Training Time (200 pages × 3 epochs) |
|--------------|-----------|--------------------------------------|
| bf16 LoRA, batch=2, grad_accum=8 | ~14–16 GB | ~25–40 min |
| bf16 LoRA, batch=4, grad_accum=4 | ~20–22 GB | ~20–30 min |
| QLoRA (nf4), batch=4, grad_accum=4 | ~10–12 GB | ~35–50 min (slower due to dequant overhead) |
| Unsloth-optimized (bf16 LoRA) | ~8–10 GB | ~15–25 min (1.7× speedup claimed) |

**Total end-to-end budget (first iteration)**:
- Data prep + annotation: 8–16h (depends on annotation tooling)
- Synthetic data generation: 2–4h (script rendering Thai forms to images)
- Environment setup + debugging: 2–4h
- Training runs (3 experiments): 1–3h
- Evaluation: 1–2h
- **Total: ~14–29h of elapsed work** (hardware runs only ~3–8h)

This fits within a 2-day sprint if annotations are pre-existing or partially available.

---

## 6. Evaluation Plan

### 6.1 Primary Metrics (Medical Domain)

| Metric | What It Measures | Tool |
|--------|-----------------|------|
| CER (Character Error Rate) | Character-level transcription accuracy; tokenizer-independent | `jiwer` or `fastwer` |
| ANLS (Avg. Normalized Levenshtein Similarity) | Tolerates minor OCR confusions; standard for document VQA | `anls` (PyPI) |
| Field-level F1 | Precision/recall on extracted key fields (test name, value, unit, date) | Custom extractor on Markdown output |
| Medical Term Preservation Rate | Fraction of medical terms (ICD, drug names, lab names) correctly transcribed | Build term lexicon from Thai SNOMED/ICD-10 |
| Numeric + Unit Accuracy | Exact match on numeric values and their units (critical for lab results) | Regex-based field extractor |

### 6.2 Baseline Comparison

| System | CER | ANLS | Notes |
|--------|-----|------|-------|
| Typhoon OCR V1.5 2B (no fine-tune) | measure | measure | Baseline |
| + LoRA r=16 (proposed) | measure | measure | Target: >5% ANLS gain |
| PaddleOCR (current Stage 3) | measure | measure | Existing system comparison |
| EasyOCR (current Stage 3) | measure | measure | Existing system comparison |

### 6.3 Field-Level F1 Extraction Protocol

After the model outputs Markdown, apply a rule-based or regex extractor to pull structured fields:

```python
import re

def extract_lab_fields(markdown_text):
    # Extract table rows from HTML tables in output
    rows = re.findall(r"<tr>(.*?)</tr>", markdown_text, re.DOTALL)
    fields = []
    for row in rows:
        cells = re.findall(r"<t[dh]>(.*?)</t[dh]>", row)
        fields.append(cells)
    return fields
```

Compare extracted fields against ground-truth annotations at the field level. Report precision, recall, F1 per field type.

### 6.4 Anti-Regression Check

Run fine-tuned model on a sample of the Typhoon OCR benchmark domains (financial reports, government forms) to confirm catastrophic forgetting has not occurred. The 10% general-domain replay samples in the training mix are the primary mitigation.

---

## 7. Step-by-Step Implementation Roadmap

### Day 1: Data and Environment

**Morning (3–4h): Environment**
1. Create `poc/typhoon-ocr-lora/` with uv
2. Install dependencies per Section 4.1
3. Verify: `python -c "import torch; print(torch.cuda.get_device_capability())"` → expect `(12, 0)` for Blackwell
4. Verify bitsandbytes: run a 4-bit load test. If it fails, proceed with bf16 LoRA only
5. Download model: `huggingface-cli download scb10x/typhoon-ocr1.5-2b`
6. Run baseline inference on 5 sample medical images to establish CER/ANLS floor

**Afternoon (4–6h): Data Preparation**
1. Collect 100–200 page images (lab results, prescriptions, referral letters)
2. PHI scrub: redact patient names, HN, dates of birth (use PIL rectangle overlay or text masking)
3. Annotate ground-truth Markdown using the canonical Typhoon prompt format
4. Write to LLaVA-style JSON (see Section 3.3 format)
5. Generate 50–80 synthetic pages:
   - Use PyThaiNLP to generate realistic Thai lab value tables
   - Render to HTML, convert to PDF via `weasyprint`, convert to PNG via `pdf2image`
   - Annotate synthetics programmatically (source is the HTML template itself)
6. Split: 80/10/10 train/val/test

### Day 2: Training and Evaluation

**Morning (2–3h): Training**
1. Run training with the recipe from Section 4.4
2. Monitor: loss should decrease within first 50 steps; if NaN, check learning rate (reduce to 5e-5) or switch to QLoRA
3. Save checkpoint at each epoch; evaluate val loss
4. Run 3 epochs; select best checkpoint by val ANLS

**Afternoon (2–3h): Evaluation and Iteration**
1. Run held-out test set through baseline and fine-tuned model
2. Compute CER, ANLS, field-level F1, medical term preservation rate
3. Run anti-regression test on 20 non-medical Thai documents
4. If performance is poor: increase r to 32, add more synthetic data, or unfreeze vision encoder
5. Save adapter weights: `model.save_pretrained("./output/typhoon-ocr-lora-medical/adapter")`
6. Document results in evaluation report

---

## 8. Inference After Fine-Tuning

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoProcessor
import torch

base = AutoModelForCausalLM.from_pretrained(
    "scb10x/typhoon-ocr1.5-2b",
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
model = PeftModel.from_pretrained(base, "./output/typhoon-ocr-lora-medical/adapter")
model.eval()

# Use the canonical prompt (do not modify)
PROMPT = """Extract all text from the image.

Instructions:
- Only return the clean Markdown.
- Do not include any explanation or extra text.
- You must include all information on the page.

Formatting Rules:
- Tables: Render tables using <table>...</table> in clean HTML format.
- Equations: Render equations using LaTeX syntax with inline ($...$) and block ($$...$$).
- Images/Charts/Diagrams: Wrap in <figure>...</figure> with descriptions
- Page Numbers: Wrap in <page_number>...</page_number>
- Checkboxes: Use ☐ for unchecked and ☑ for checked boxes."""
```

---

## 9. Risks and Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| bitsandbytes 4-bit broken on sm_120 Blackwell | Medium | Default to bf16 LoRA; 2B fits in 24GB without 4-bit |
| Catastrophic forgetting on general Thai docs | Low-Medium | Include 10% replay samples from CoSyn/Typhoon training distribution |
| Prompt-lock degradation if output format changes | High if ignored | Strictly follow canonical Typhoon output format in all annotations |
| PHI exposure in training data | High (legal risk) | PHI scrub before any data leaves the NECTEC environment |
| Overfitting on <100 samples | Medium | LoRA inherently regularizes; use dropout=0.05; validate after each epoch |
| ZeRO-3 + LoRA gradient flow issue | Low (single GPU) | Use accelerate default (no ZeRO or ZeRO-2) for single GPU |

---

## 10. Structured Extraction Pipeline (Post Fine-Tune)

The LoRA fine-tuned model outputs Markdown. To get structured JSON for Stage 5 (Struct Extraction), add a downstream extraction layer:

```
[Image] → [Typhoon OCR + LoRA adapter] → [Markdown text]
                                              ↓
                                   [Rule-based HTML table parser]
                                              ↓
                                   [Named field extractor (regex / small LLM)]
                                              ↓
                                   [Validated JSON for Stage 6]
```

This keeps the model's output format unchanged (preserving prompt-lock) while adding structure downstream. Thai medical field names can be matched using a Thai ICD-10 / lab code lexicon as the anchor vocabulary.

---

## 11. Connection to Pipeline Stages

| Pipeline Stage | Role of This Work |
|---------------|------------------|
| Stage 3: Text Recognition | Replaces or augments PaddleOCR/EasyOCR for full-page medical document understanding |
| Stage 4: Post-correction | Partially replaces ByT5/WangchanBERTa — the fine-tuned VLM corrects during recognition |
| Stage 5: Struct Extraction | Downstream extractor on Markdown output (Section 10 above) |
| Stage 6: Validation | Numeric and unit exact-match checks apply directly to extracted fields |

---

## 12. Next Steps After POC

1. If field-level F1 improves significantly (>10% over PaddleOCR baseline): expand dataset to 500 pages and retrain
2. Consider GRPO/DPO alignment if the model produces hallucinated values on edge-case lab forms
3. Publish internal benchmark: 200-page Thai medical OCR evaluation set with CER/ANLS/field-F1 scoring
4. Upstream contribution: release the synthetic Thai medical form generator as open-source to reduce the data scarcity problem for the community
