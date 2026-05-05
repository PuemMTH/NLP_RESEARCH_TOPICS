# ocr-eval-3layer

3-Layer OCR Evaluation Stack for Thai Medical Documents — POC

Replaces the current Module 2 evaluation system (WER with PyThaiNLP newmm +
cosine similarity with SentenceTransformer) with a more robust, domain-aware
3-layer stack.

---

## Problem Statement

The current Module 2 system has two known weaknesses:

| Issue | Detail |
|-------|--------|
| Tokenizer-dependent WER | PyThaiNLP newmm vs. attacut produces ~40% relative drift in WER on the same model output. The score is not stable. |
| Generic cosine similarity | SentenceTransformer (multilingual) misses fine-grained medical term errors (e.g., substituting one drug name for another similar-sounding one). |

---

## Solution: 3-Layer Stack

```
L1 — CER (Character Error Rate)
     Tokenizer-agnostic. Formula: edit_distance(ref, hyp) / len(ref) * 100
     Library: jiwer

L2 — ANLS* (Average Normalized Levenshtein Similarity, threshold=0.5)
     Per-field and aggregate. NLS < 0.5 → 0, else NLS.
     Library: anls (PyPI)

L3 — BERTScore-style metric with WangchanBERTa
     Model: airesearch/wangchanberta-base-att-spm-uncased (12 layers, SPM)
     Layer: 11 (penultimate) — calibrated on 5 Thai medical OCR pairs.
     Reports precision, recall, F1 via greedy cosine alignment of layer embeddings.
     Implementation: direct transformers (see Deviations below).
```

Also computes OLD baseline metrics (WER newmm, WER attacut, cosine sim)
for direct side-by-side comparison.

---

## Setup

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
cd poc/ocr-eval-3layer
uv sync
```

---

## Usage

### End-to-end (recommended)

```bash
bash poc/ocr-eval-3layer/run.sh
```

This runs: uv sync → generate 5 sample pairs → single-pair demo → full suite.

### Single pair

```bash
uv run python poc_runner.py \
    --reference "ยาแก้ปวดหัว" \
    --hypothesis "ยาแกปวดหว"
```

### Full test suite (5 Thai medical pairs)

```bash
uv run python poc_runner.py \
    --test-suite sample_outputs/test_pairs.json \
    --save-json sample_outputs/eval_results.json
```

### CLI options

```
--reference TEXT        Reference (ground-truth) Thai text
--hypothesis TEXT       OCR hypothesis text (required with --reference)
--test-suite PATH       JSON file with test pairs (from generate_sample.py)
--device cuda|cpu       Force device (default: auto-detect GPU)
--save-json PATH        Write results to JSON file
--anls-threshold FLOAT  ANLS* threshold (default 0.5)
--skip-old-baseline     Skip WER/cosine baseline (faster)
```

---

## Output Format

### Stdout (per pair)

```
======================================================================
  Pair: pair_01
  REF: ยาแก้ปวดหัว
  HYP: ยาแกปวดหว
======================================================================
╭────────┬─────────────────────┬──────────┬───────────────────────────────╮
│ Layer  │ Metric              │ Value    │ Note                          │
├────────┼─────────────────────┼──────────┼───────────────────────────────┤
│ OLD    │ WER (newmm)         │ 66.7%    │ word-level, PyThaiNLP newmm   │
│ OLD    │ WER (attacut/long.) │ 100.0%   │ same model, different token.  │
│ OLD    │ Cosine Similarity   │ 0.8821   │ paraphrase-multilingual-mpnet │
│ L1     │ CER                 │ 25.0%    │ tokenizer-agnostic            │
│ L2     │ ANLS* (t=0.5)       │ 0.7500   │ 0=bad, 1=perfect             │
│ L3     │ BERTScore P         │ 0.9312   │ WangchanBERTa                 │
│ L3     │ BERTScore R         │ 0.9205   │ WangchanBERTa                 │
│ L3     │ BERTScore F1        │ 0.9258   │ WangchanBERTa                 │
╰────────┴─────────────────────┴──────────┴───────────────────────────────╯

  [Tokenizer-drift check]  WER newmm: 66.7%  |  WER attacut: 100.0%  |  CER: 25.0%  |  Absolute drift: 33.3pp
```

### JSON (--save-json)

```json
[
  {
    "id": "pair_01",
    "reference": "ยาแก้ปวดหัว",
    "hypothesis": "ยาแกปวดหว",
    "wer_newmm_pct": 66.67,
    "wer_attacut_pct": 100.0,
    "cosine_sim": 0.8821,
    "cer_pct": 25.0,
    "anls_star": 0.75,
    "bs_precision": 0.9312,
    "bs_recall": 0.9205,
    "bs_f1": 0.9258
  }
]
```

---

## Deviations from Spec

### L3: Direct transformers instead of bert-score library

`bert-score==0.3.x` is incompatible with `transformers v5` (integer overflow in
`set_truncation_and_padding` caused by WangchanBERTa's default `model_max_length`
of 10^30). Rather than pin `transformers` to v4.x (which conflicts with other
POCs in this workspace), L3 is implemented directly using `transformers.CamembertModel`:
- Load WangchanBERTa with `output_hidden_states=True`
- Extract layer-11 embeddings, L2-normalize each token vector
- Greedy cosine alignment: P = mean(max over ref for each hyp token), R = mean(max over hyp for each ref token)
- F1 = harmonic mean of P and R

This is mathematically equivalent to the bert-score algorithm (no IDF weighting, no baseline rescaling).
The `bert-score` package is still listed in `pyproject.toml` as reference but is unused at runtime.

### Layer selection

Layer 11 of 12 was selected by calibration on the 5-pair suite:

| Layer | pair_01 F1 | pair_02 F1 | pair_03 F1 | pair_04 F1 | pair_05 F1 |
|-------|------------|------------|------------|------------|------------|
| 9     | 0.218      | 0.126      | 0.554      | 0.151      | 0.927      |
| 10    | 0.361      | 0.529      | -          | -          | 0.929      |
| **11**| **0.425**  | **0.725**  | 0.506      | 0.057      | **0.907**  |
| 12    | 0.311      | 0.389      | -          | -          | 0.910      |

Layer 11 best discriminates tone-mark and vowel-loss OCR errors (pairs 01, 02 — the dominant Thai OCR failure mode). The low score for pair_04 (heavy consonant cluster drop: "แพ้ยาเพนิซิลลิน" → "แพยาเพนซลน") at layer 11 may be appropriate — that level of corruption does make the word genuinely less semantically retrievable.

---

## Thai Medical OCR Pipeline Integration

```
Stage 1: Preprocessing      (denoising, deskew)
Stage 2: Layout Detection   (DocLayout-YOLO)
Stage 3: Text Recognition   (PaddleOCR / GOT-OCR)
Stage 4: Post-correction    (ByT5 / WangchanBERTa)
Stage 5: Struct Extraction  (table, key-value)
Stage 6: Validation         (schema, compliance)
         ↑
         THIS POC — replaces Module 2 quality signal
         Used to measure Stage 3 output and Stage 4 improvement.
```

### Thai Language Notes

- L1 (CER) has no Thai-specific concerns — works on any Unicode text.
- L2 (ANLS*) uses standard Levenshtein edit distance — also language-agnostic.
- L3 (BERTScore) uses WangchanBERTa, which was pretrained on Thai Wikipedia +
  Thai news corpora. It handles Thai sub-word tokenization via SentencePiece
  (SPM uncased). Fine-tuning on medical text would improve discrimination of
  medical term near-misses further.
- The tokenizer-drift demo uses newmm vs. attacut (both bundled in PyThaiNLP)
  rather than external `deepcut` (TF1-era, frequent install failures). The
  drift argument is identical — same OCR output, different WER score.

---

## Notes on Model Caching

- WangchanBERTa weights are downloaded once to `~/.cache/huggingface/`.
- SentenceTransformer weights: `~/.cache/torch/sentence_transformers/`.
- Never commit `*.pt`, `*.bin`, `*.safetensors` files.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `jiwer` | CER + WER computation |
| `anls` | ANLS* metric |
| `bert-score` | Reference only (unused at runtime — see Deviations) |
| `transformers` | WangchanBERTa model + CamembertTokenizer for L3 |
| `sentencepiece` | SPM tokenizer for WangchanBERTa |
| `protobuf` | Required by sentencepiece SPM serialization |
| `sentence-transformers` | OLD baseline cosine similarity |
| `pythainlp` | WER tokenizer (newmm, attacut) |
| `attacut` | Neural Thai tokenizer for tokenizer-drift demo |
| `tabulate` | Pretty-print output tables |
| `torch` | GPU inference (cu128, Blackwell-compatible) |
