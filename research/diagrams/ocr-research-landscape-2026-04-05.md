# Last Updated: 2026-04-05

# Diagram: OCR Research Landscape (2026)

```mermaid
flowchart LR
    A[Document Image Input] --> B[Preprocessing]
    B --> C[Layout Understanding]
    C --> D[Text Recognition]
    D --> E[Post-Correction]
    E --> F[Structured Extraction]
    F --> G[Validation and Compliance]

    B --> B1[Restoration and denoise]
    C --> C1[Region and table detection]
    D --> D1[Script and multilingual robustness]
    E --> E1[Rule-based]
    E --> E2[LLM-based unconstrained]
    E --> E3[LLM-based constrained]
    F --> F1[Key-value and schema mapping]
    G --> G1[PHI de-identification and leakage checks]
    G --> G2[Field-level consistency checks]

    H[Evaluation Layer] --> H1[CER and WER]
    H --> H2[Field-level exact match and F1]
    H --> H3[Medical term preservation]
    H --> H4[Latency and memory footprint]
    H --> H5[Failure and recovery analysis]

    C -.drives.-> H
    D -.drives.-> H
    E -.drives.-> H
    F -.drives.-> H
    G -.drives.-> H
```

## Notes
- Synthesized from OCR-related source summaries and topic notes currently indexed in this workspace.
- Designed as a broad context map for selecting OCR research direction and evaluation strategy.
