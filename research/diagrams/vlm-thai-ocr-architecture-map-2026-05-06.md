# Last Updated: 2026-05-06

# Diagram: VLM Thai OCR Architecture Map

## Modular OCR + VLM Fallback Architecture

```mermaid
flowchart LR
  A[Input Thai document image] --> B[Preprocess<br/>deskew denoise crop]
  B --> C[Layout detection<br/>DocLayout-YOLO]
  C --> D[OCR per region<br/>EasyOCR / PaddleOCR]
  D --> E[Post-correction<br/>ByT5 / WangchanBERTa]
  E --> F[Field extraction<br/>rules + schema]
  F --> G[Evaluation cascade<br/>CER + ANLS + BERTScore]
  G --> H{Verifier result}
  H -->|supported| I[Accept field JSON]
  H -->|unsupported / uncertain| J[VLM fallback<br/>Typhoon OCR / Qwen2.5-VL]
  J --> K[Evidence-grounded verifier]
  K --> I
  K -->|still uncertain| L[Human review]
```

## Typhoon OCR-Style Data Construction / Inference Architecture

```mermaid
flowchart TB
  A[Raw Thai/English documents] --> B[Traditional OCR output]
  B --> C[VLM restructuring]
  C --> D[Curated synthetic / structured data]
  D --> E[Fine-tune VLM backbone]
  E --> F[Typhoon OCR model]
  G[Document image] --> F
  F --> H[Markdown / structured extraction]
  H --> I[Verifier + validation]
```

## Qwen2.5-VL Conceptual Architecture

```mermaid
flowchart LR
  A[Image / document / video] --> B[Dynamic resolution processor]
  B --> C[Native ViT vision encoder<br/>window attention]
  D[Prompt / task instruction] --> E[Text tokenizer]
  C --> F[Multimodal token fusion<br/>mRoPE positions]
  E --> F
  F --> G[Qwen language model]
  G --> H[Text / bbox / structured answer]
```

## mPLUG-DocOwl OCR-Free Architecture

```mermaid
flowchart LR
  A[High-resolution document image] --> B[Vision tower<br/>CLIP-style encoder]
  B --> C[Vision-to-text projection]
  C --> D[Multimodal fusion]
  E[Question / instruction] --> D
  D --> F[LLM decoder]
  F --> G[OCR-free document answer<br/>table / chart / text / layout]
```

## Source Links

- Typhoon OCR paper: <https://arxiv.org/abs/2601.14722>
- Typhoon OCR model card: <https://huggingface.co/typhoon-ai/typhoon-ocr-7b>
- Qwen2.5-VL technical report: <https://arxiv.org/abs/2502.13923>
- Qwen2.5-VL architecture notes: <https://deepwiki.com/QwenLM/Qwen2.5-VL/2-model-architecture>
- mPLUG-DocOwl system architecture: <https://deepwiki.com/X-PLUG/mPLUG-DocOwl/1.2-system-architecture>
- mPLUG-DocOwl 1.5: <https://arxiv.org/abs/2403.12895>
- mPLUG-DocOwl2: <https://arxiv.org/abs/2409.03420>

