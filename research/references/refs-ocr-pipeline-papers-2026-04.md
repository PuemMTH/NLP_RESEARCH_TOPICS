# Last Updated: 2026-04-05

# Reference Mining: OCR Pipeline Papers by Stage

Source basis:
- arXiv query sweeps performed on 2026-04-05 for OCR pipeline subtopics
- Existing OCR references already indexed in this workspace

---

## 1) Preprocessing (denoise, rectification, orientation, restoration)

- PreP-OCR: A Complete Pipeline for Document Image Restoration and Enhanced OCR Accuracy (2025)
  - https://arxiv.org/abs/2505.20429
- NAF-DPM: A Nonlinear Activation-Free Diffusion Probabilistic Model for Document Enhancement (2024)
  - https://arxiv.org/abs/2404.05669
- ForCenNet: Foreground-Centric Network for Document Image Rectification (2025)
  - https://arxiv.org/abs/2507.19804
- Seeing Straight: Document Orientation Detection for Efficient OCR (2025)
  - https://arxiv.org/abs/2511.04161
- MatteViT: High-Frequency-Aware Document Shadow Removal with Shadow Matte Guidance (2025)
  - https://arxiv.org/abs/2512.08789

## 2) Layout Understanding (region, reading order, structural parsing)

- DocLayout-YOLO: Enhancing Document Layout Analysis through Diverse Synthetic Data and Global-to-Local Adaptive Perception (2024)
  - https://arxiv.org/abs/2410.12628
- DLAFormer: An End-to-End Transformer For Document Layout Analysis (2024)
  - https://arxiv.org/abs/2405.11757
- PARL: Position-Aware Relation Learning Network for Document Layout Analysis (2026)
  - https://arxiv.org/abs/2601.07620
- Dolphin-v2: Universal Document Parsing via Scalable Anchor Prompting (2026)
  - https://arxiv.org/abs/2602.05384
- DocSAM: Unified Document Image Segmentation via Query Decomposition and Heterogeneous Mixed Learning (2025)
  - https://arxiv.org/abs/2504.04085

## 3) Text Recognition (OCR/HTR core recognition)

- VISTA-OCR: Towards generative and interactive end-to-end OCR models (2025)
  - https://arxiv.org/abs/2504.03621
- FastTextSpotter: A High-Efficiency Transformer for Multilingual Scene Text Spotting (2024)
  - https://arxiv.org/abs/2408.14998
- Towards Universal Khmer Text Recognition (2026)
  - https://arxiv.org/abs/2603.00702
- Handwritten Text Recognition of Historical Manuscripts Using Transformer-Based Models (2025)
  - https://arxiv.org/abs/2508.11499
- SARD: A Large-Scale Synthetic Arabic OCR Dataset for Book-Style Text Recognition (2025)
  - https://arxiv.org/abs/2505.24600

## 4) Post-correction (error correction after OCR)

- OCR Error Post-Correction with LLMs in Historical Documents: No Free Lunches (2025)
  - https://arxiv.org/abs/2502.01205
- Multimodal LLMs for OCR, OCR Post-Correction, and Named Entity Recognition in Historical Documents (2025)
  - https://arxiv.org/abs/2504.00414
- Post-OCR Text Correction for Bulgarian Historical Documents (2024)
  - https://arxiv.org/abs/2409.00527
- RoundTripOCR: Data Generation for Post-OCR Correction in Low-Resource Devanagari Languages (2024)
  - https://arxiv.org/abs/2412.15248
- NeKo: Cross-Modality Post-Recognition Error Correction with Tasks-Guided MoE Language Model (2024)
  - https://arxiv.org/abs/2411.05945

## 5) Structured Extraction (KIE/VIE/schema mapping)

- MeDocVL: A Visual Language Model for Medical Document Understanding and Parsing (2026)
  - https://arxiv.org/abs/2602.06402
- ExStrucTiny: A Benchmark for Schema-Variable Structured Information Extraction from Document Images (2026)
  - https://arxiv.org/abs/2602.12203
- UNIKIE-BENCH: Benchmarking Large Multimodal Models for Key Information Extraction in Visual Documents (2026)
  - https://arxiv.org/abs/2602.07038
- Qianfan-OCR: A Unified End-to-End Model for Document Intelligence (2026)
  - https://arxiv.org/abs/2603.13398
- ROAP: A Reading-Order and Attention-Prior Pipeline for Optimizing Layout Transformers in Key Information Extraction (2026)
  - https://arxiv.org/abs/2601.05470

## 6) Validation / Compliance (reliability, policy, PHI/privacy)

- FinCriticalED: A Visual Benchmark for Financial Fact-Level OCR Evaluation (2025)
  - https://arxiv.org/abs/2511.14998
- SCORE: A Semantic Evaluation Framework for Generative Document Parsing (2025)
  - https://arxiv.org/abs/2509.19345
- Doc-PP: Document Policy Preservation Benchmark for Large Vision-Language Models (2026)
  - https://arxiv.org/abs/2601.03926
- DICOM De-Identification via Hybrid AI and Rule-Based Framework for Scalable, Uncertainty-Aware Redaction (2025)
  - https://arxiv.org/abs/2507.23736
- Not What the Doctor Ordered: Surveying LLM-based De-identification and Quantifying Clinical Information Loss (2025)
  - https://arxiv.org/abs/2509.14464

---

## Practical Notes for Use

- Some papers span multiple stages in the pipeline; they are placed in the stage where they contribute most directly.
- For thesis/prototype planning, use this file as a seed list, then shortlist 2-3 papers per stage for deep reading and reproducible baselines.
