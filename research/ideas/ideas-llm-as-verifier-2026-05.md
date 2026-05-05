# Last Updated: 2026-05-06

# Ideas: LLM as a Verifier for Thai OCR and SME Data Pipelines (2026-05)

## Context

The existing NECTEC pipeline already has deterministic evaluation metrics:

- Thai-tokenized WER with PyThaiNLP `newmm`
- CER as a tokenizer-independent OCR metric candidate
- SentenceTransformer cosine similarity
- Candidate semantic evaluation with BERTScore or LLM-as-a-Judge

The next research step is to move from **LLM-as-a-Judge** to **LLM-as-a-Verifier**.

## Judge vs. Verifier

| Role | Output | Main question | Risk |
|---|---|---|---|
| LLM-as-a-Judge | score, ranking, explanation | "How good is this output?" | subjective scoring, prompt sensitivity |
| LLM-as-a-Verifier | pass/fail/uncertain with evidence | "Is this claim or field supported by the source?" | evidence dependency, false verification |

For Thai OCR, a verifier is more useful than a generic judge because downstream use often depends on exact preservation of critical facts:

- numeric value
- unit
- product name
- brand
- medicine/test name
- date
- dosage or quantity
- key-value alignment

## Proposed Research Direction

**"Evidence-Grounded LLM Verification for Thai OCR Outputs and Product Data Cleaning"**

Core idea:
- Treat OCR output or cleaned product data as a set of claims/fields.
- Verify each field against the original OCR text, image crop, or reference text.
- Return structured verification labels: `supported`, `unsupported`, `uncertain`, plus reason and evidence span.

## Verification Pipeline

```text
Image / OCR JSON / Reference Text
        |
        v
Field extraction or cleaned product text
        |
        v
Claim decomposition
        |
        v
Evidence retrieval
  - OCR line / bbox
  - image crop
  - product dictionary
  - medical lexicon
        |
        v
LLM verifier
        |
        v
Structured result:
  supported / unsupported / uncertain
  evidence span
  failure reason
  severity
```

## Candidate POC

Create `poc/llm-ocr-verifier/`:

- Input:
  - OCR output JSON
  - extracted fields JSON
  - optional reference text
  - optional image crop path
- Output:
  - verification report JSON
  - field-level summary Markdown

Example output schema:

```json
{
  "field": "unit",
  "predicted_value": "mg/dL",
  "evidence": "Glucose 98 mg/dL",
  "label": "supported",
  "severity": "low",
  "reason": "The predicted unit exactly appears next to the glucose value."
}
```

## Metrics

- Field verification accuracy against human labels
- Unsupported-field detection F1
- False-pass rate for critical fields
- False-fail rate for correct numeric fields
- Abstention rate (`uncertain`)
- Cost and latency per document

## Best Fit With Existing Work

### SME Product Cleaning

Verifier checks whether an LLM-normalized product name is faithful:

- Did it preserve brand?
- Did it preserve size/quantity/unit?
- Did it remove only promotional/noisy text?
- Did it invent product attributes not visible in the OCR text?

### OCR Evaluation

Verifier checks whether OCR output preserves exact facts:

- Is the numeric value copied correctly?
- Is the unit correct?
- Is the Thai product/medical term preserved?
- Is the semantic meaning preserved without unsafe correction?

### Thai Medical OCR

Verifier acts as a safety layer before downstream structuring:

- Flag unsupported extracted fields.
- Abstain when OCR evidence is too noisy.
- Require human review for high-severity fields such as dosage, lab value, and patient identifiers.

## Research Hypothesis

Hypothesis:
- A verifier that uses explicit evidence spans and an `uncertain` label will be more reliable than a pure LLM judge score for Thai OCR outputs, especially on numeric fields and unit preservation.

Open question:
- Can a Thai-capable LLM verify numeric and unit fields robustly, given that prior fact-verification research reports weaker performance on numeral-related claims?

## Recommended Experiment

1. Build a small verification dataset from existing OCR outputs:
   - 100 product label fields
   - 100 text-heavy ad/product classification examples
   - 100 medical/document fields if safe data is available
2. Annotate each predicted field as supported, unsupported, or uncertain.
3. Compare:
   - deterministic rule verifier
   - LLM-as-a-Judge score threshold
   - evidence-grounded LLM verifier
4. Report:
   - field verification F1
   - critical false-pass rate
   - abstention quality
   - cost/latency

## Practical Priority

This should be implemented after the 3-layer evaluation stack:

1. CER + ANLS + LLM-judge
2. LLM-as-a-Verifier
3. VLM fallback for low-confidence or unsupported fields

