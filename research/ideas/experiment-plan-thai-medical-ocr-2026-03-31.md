# Last Updated: 2026-03-31

# One-Page Experiment Plan: Thai Medical OCR (OCR-only vs VLM + Post-correction)

## 1) Objective
Evaluate whether a VLM-centered pipeline improves Thai medical document extraction quality over a strong OCR-only baseline under practical deployment constraints (latency, privacy, and robustness).

## 2) Research Question
For Thai medical documents with complex layouts, does VLM parsing plus constrained post-correction achieve better field-level correctness than OCR-only pipelines?

## 3) Hypothesis
H1: VLM + constrained post-correction yields higher field-level exact match and key-value F1 than OCR-only.
H2: OCR-only may remain faster, but VLM pipeline provides better robustness on noisy scans and mixed Thai-English text.
H3: Unconstrained LLM correction risks harming medical terms; lexicon-constrained correction reduces this failure mode.

## 4) Data Slice (Pilot)
- Size: 300-600 de-identified pages/images.
- Sources: lab reports, prescriptions, discharge summaries, medical forms.
- Split: 70% train/dev adaptation, 15% validation, 15% test.
- Annotation targets:
  - Plain text transcription (line-level)
  - Structured fields: patient metadata, test name, value, unit, reference range, date, hospital/site
- Requirements: PHI-masked storage and audit trail.

## 5) Systems Compared
A. OCR-only baseline
- OCR engine + rule-based normalization + regex field extraction

B. OCR + unconstrained LM post-correction
- Same OCR output, corrected by generic language model

C. OCR + constrained post-correction
- Domain lexicon constraints (Thai medical terms, abbreviations, units), format guards

D. VLM + constrained post-correction (target system)
- VLM document parsing (text + layout + key-values), then constrained correction and schema mapping

## 6) Metrics
Primary:
- Field-level exact match
- Key-value F1 (micro and macro)

Secondary:
- CER, WER
- Medical-term preservation rate
- Unit-value consistency score
- Latency per page and throughput
- PHI leakage rate after processing

## 7) Experimental Protocol
1. Build a unified JSON schema for all systems.
2. Freeze test split and evaluation scripts before tuning.
3. Tune each system on validation only.
4. Run 3 random-seed repeats where applicable.
5. Perform error analysis by document type and field type.
6. Report confidence intervals or bootstrap uncertainty on primary metrics.

## 8) Success Criteria (Go/No-Go)
- Go if system D improves field-level exact match by >= 8% over system A on test set.
- Go if medical-term preservation >= 98% and no PHI regression.
- No-Go if latency exceeds service SLA by > 2x without quality gain.

## 9) Risks and Mitigation
- Risk: Over-correction of clinical terms.
  - Mitigation: lexicon lock, unit patterns, constrained decoding.
- Risk: Layout variance across hospital templates.
  - Mitigation: template-stratified evaluation and augmentation.
- Risk: Privacy compliance gaps.
  - Mitigation: PHI redaction checks and isolated evaluation environment.

## 10) 4-Week Pilot Timeline
- Week 1: Data curation, schema, baseline OCR pipeline.
- Week 2: VLM integration and constrained post-correction.
- Week 3: Full evaluation + error analysis.
- Week 4: Ablation study and thesis/proposal-ready report.

## Source Anchors
- Typhoon OCR (Thai OCR): https://arxiv.org/abs/2601.14722
- MeDocVL (Medical document parsing): https://arxiv.org/abs/2602.06402
- No Free Lunches (LLM post-correction limits): https://arxiv.org/abs/2502.01205
