# Last Updated: 2026-05-06

# Ideas: Deep Research Follow-up From VLM Thai OCR References

## Priority 1 — Internal Thai Product/Medical OCRBench

**Research question**: Can an internal benchmark inspired by ThaiOCRBench reveal which pipeline variant works best for SME product labels and Thai medical-like documents?

**Why this matters**:
- ThaiOCRBench already gives a schema and task taxonomy for Thai document/VLM evaluation.
- NECTEC work needs domain-specific categories not covered directly by generic Thai document benchmarks.

**Dataset slice**:
- 100 product label OCR samples
- 100 ad vs. product-package classification samples
- 100 key-value extraction samples from product labels
- 50-100 medical-like document samples, if privacy-safe

**Schema**:
- `image`
- `task`
- `question`
- `answer`
- `category`
- `field_type`
- `criticality`
- `evidence_bbox`

**Metrics**:
- CER for raw text
- ANLS/ANLS* for field text
- F1 for classification/KIE
- verifier false-pass rate for critical fields

## Priority 2 — Cost-Aware OCR Evaluation Cascade

**Research question**: Can a layered metric stack reduce LLM judging cost while improving OCR reliability?

**Design**:

```text
OCR output
  |
  v
Layer 1: exact/rule/CER
  | pass easy cases
  v
Layer 2: ANLS/BERTScore
  | route disagreements
  v
Layer 3: LLM judge/verifier
  | high-risk only
  v
human review / VLM fallback
```

**Contribution**:
- Adapts multi-layered evaluation ideas to Thai OCR.
- Adds field criticality and Thai tokenizer-risk awareness.

## Priority 3 — VLM Product-Label vs Advertisement Classifier

**Research question**: Can contrastive VLM prompts replace the 700-character text-length heuristic?

**Prompt design**:
- Class A: product packaging or label with ingredients, specifications, price, quantity, brand, barcode, or usage details.
- Class B: advertising image focused on lifestyle, promotion, claims, discount, slogan, or campaign content.

**Baseline**:
- Existing 700-character threshold.
- OCR text length + OCR bbox coverage.
- VLM zero-shot classifier.

**Metric**:
- F1 by class.
- False rejection of valid product images.
- Failure mode by packaging/ad subtype.

## Priority 4 — Evidence-Grounded VLM Fallback

**Research question**: When should the pipeline call a heavy VLM instead of trusting modular OCR?

**Trigger candidates**:
- low OCR confidence
- low ANLS against expected field pattern
- verifier label = `unsupported` or `uncertain`
- layout detector finds table/form but OCR field extraction is incomplete

**System design**:
- Modular pipeline is default.
- VLM is fallback for only difficult regions or fields.
- Verifier decides whether VLM output is acceptable.

**Why this is better than VLM-only**:
- Reduces cost and latency.
- Keeps interpretable OCR/layout evidence.
- Allows safety checks on high-risk fields.

## Priority 5 — Thai Product Image-Text Alignment

**Research question**: Are existing Thai/multilingual CLIP-style models good enough to detect mismatches between product images and extracted OCR/product descriptions?

**Candidate models**:
- `patomp/thai-light-multimodal-clip-and-distill`
- `jina-clip-v2`
- Typhoon2-Vision as a judgment model

**Experiment**:
- Positive pairs: image and OCR text from same product.
- Negative pairs: swap OCR text across product categories.
- Hard negatives: same category but different brand/quantity.

**Metric**:
- Recall@1 / Recall@10 for retrieval
- AUROC for match vs. mismatch
- failure rate on Thai-English mixed labels

## Priority 6 — Typhoon OCR vs Qwen2.5-VL vs Modular Pipeline

**Research question**: Is a Thai-specific OCR VLM actually better than a strong general VLM and the existing modular pipeline on NECTEC-like data?

**Systems to compare**:
- Modular: DocLayout-YOLO + EasyOCR/PaddleOCR + ByT5/WangchanBERTa
- Thai-specific VLM: Typhoon OCR or Typhoon2-Vision
- General VLM: Qwen2.5-VL

**Metrics**:
- text CER
- key-value F1
- ANLS
- verifier critical false-pass rate
- latency
- VRAM
- output format stability

## Updated Gap Statements

1. **Thai product-label benchmark gap**: ThaiOCRBench is broad, but product-label OCR and SME ad/package classification need a domain-specific benchmark.
2. **Thai OCR metric gap**: WER is tokenizer-relative; CER/ANLS/verifier should be studied specifically for Thai OCR.
3. **Verifier gap**: LLM-as-a-Judge gives score, but Thai OCR needs evidence-grounded verification for numbers, units, brands, and medical/product terms.
4. **Thai image-text alignment gap**: public Thai/multilingual CLIP-like models exist, but product-label OCR alignment is under-validated.
5. **VLM fallback policy gap**: most work compares full VLM systems, but practical deployment needs a policy for when to call the heavy VLM.

## Recommended Next POC Order

1. `poc/ocr-evaluation-cascade/`
2. `poc/vlm-product-image-classifier/`
3. `poc/llm-ocr-verifier/`
4. `poc/vlm-fallback-router/`
5. `poc/product-image-text-alignment/`

