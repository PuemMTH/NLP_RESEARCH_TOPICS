# Last Updated: 2026-05-05

# References: VLM Extension for Thai OCR Pipeline (2026-05)

Topic thread: extending the NECTEC SME product-data cleaning + OCR evaluation pipeline with Vision-Language Models.

---

## Thai-Specific VLM and OCR Papers

### Typhoon OCR — Open Vision-Language Model For Thai Document Extraction
- **arXiv**: https://arxiv.org/abs/2601.14722
- **Authors**: Surapon Nonesung, Natapong Nitarach, Teetouch Jaknamon, Pittawat Taveekitworachai, Kunat Pipatanakul (SCB 10X)
- **Year**: 2026 (January)
- **Summary**: End-to-end open-source VLM for Thai and English document parsing. Uses a multi-stage data construction pipeline: traditional OCR output → VLM restructuring → curated synthetic data. V1.5 achieves higher BLEU, ROUGE-L, and Levenshtein scores than V1 despite being smaller (2B vs 7B parameters).
- **Pipeline stage**: Replaces Stage 3 (Text Recognition) + Stage 4 (Post-correction) + Stage 5 (Struct Extraction) as a unified pass.
- **Key caveat**: 5–10x heavier than the modular pipeline (EasyOCR + ByT5). Use-case trade-off: accuracy vs. memory.
- **Relevance to user modules**: Directly replaces/augments Module 2 evaluation: model outputs can be scored with their BLEU/ROUGE-L metrics or compared using ANLS.

### ThaiOCRBench — Task-Diverse Benchmark for Vision-Language Understanding in Thai
- **arXiv**: https://arxiv.org/abs/2511.04479
- **Authors**: Surapon Nonesung, Teetouch Jaknamon, Sirinya Chaiophat et al. (SCB 10X)
- **Year**: 2025 (accepted AACL 2025)
- **Summary**: First comprehensive Thai VLM benchmark. 2,808 human-annotated images across 13 task categories: chart/table/document parsing, fine-grained text recognition, full-page OCR, handwriting, key information extraction, document classification, diagram VQA, and more.
- **Models evaluated**: Gemini 2.5 Pro (best: 0.777 avg), GPT-4o, Claude Sonnet 4, Qwen2.5-VL 72B (best open-source: 0.615), InternVL3, Gemma3, LLaMA3.2 Vision, Tesseract, EasyOCR.
- **Metrics used**: TED (table/chart/document parsing), BMFL (text recognition tasks), F1 (key info extraction), ANLS (VQA tasks). WER/cosine similarity NOT used — deliberate design choice.
- **Key failure modes**: Language bias (model outputs non-Thai), structural mismatch on layout tasks, character-level errors in fine-grained recognition.
- **Relevance to user modules**: Blueprint for upgrading Module 2 metrics from WER+cosine sim → ANLS + field-level F1 + TED.

### Typhoon 2 — Family of Open Text and Multimodal Thai LLMs
- **arXiv**: https://arxiv.org/abs/2412.13702
- **Authors**: Kunat Pipatanakul, Potsawee Manakul, Natapong Nitarach et al. (SCB 10X)
- **Year**: 2024 (December)
- **Summary**: Full family: Typhoon2-Text (1B–70B, Llama 3 + Qwen2 base), Typhoon2-Vision (Thai document understanding), Typhoon2-Audio (speech-to-speech), Typhoon2-Safety (Thai cultural classifier). Vision component: Qwen2VL-7B fine-tuned for Thai.
- **HuggingFace**: scb10x/typhoon2-qwen2vl-7b-vision-instruct
- **Pipeline stage**: Stage 3 (recognition) + Stage 4 (post-correction) candidate.
- **Relevance to user modules**: Typhoon2-Vision is a direct candidate for product-label vs. ad image classification (Module 1 upgrade).

---

## General VLM Document Understanding Models

### Qwen2.5-VL Technical Report
- **arXiv**: https://arxiv.org/abs/2502.13923
- **Authors**: Shuai Bai, Keqin Chen et al. (Alibaba Qwen Team)
- **Year**: 2025 (February)
- **Summary**: VLM series in 3 sizes (edge to 72B). Flagship 72B matches GPT-4o and Claude 3.5 Sonnet on document understanding. Key features: robust structured data extraction from invoices/forms/tables, chart/diagram/layout analysis, dynamic resolution processing.
- **Benchmark standing**: Highest open-source average on ThaiOCRBench (0.615 avg, per above).
- **Pipeline stage**: Stage 3 replacement; Stage 5 structured extraction.
- **Relevance to user modules**: Zero-shot key-value extraction from product labels directly (Module 1 data cleaning); semantic understanding beyond cosine similarity (Module 2 upgrade).

### mPLUG-DocOwl 2 — High-Resolution Compressing for OCR-Free Multi-Page Document Understanding
- **Reference**: Alibaba + RUC, September 2024
- **Summary**: Extends DocOwl 1.5 (unified structure learning for OCR-free document understanding) to multi-page setting with high-resolution compression. Handles tables, charts, complex layouts without an explicit OCR step.
- **Pipeline stage**: Stage 2 (layout) + Stage 3 (recognition) combined.
- **Note**: Verify with primary arXiv fetch before citing in formal work.

### InternVL 2.5 / InternVL3
- **Blog**: https://internvl.github.io/blog/2024-12-05-InternVL-2.5/
- **Summary**: Advanced multimodal LLM with strong DocVQA and InfographicVQA benchmark scores. Evaluated in ThaiOCRBench (open-source alternative to Qwen2.5-VL).
- **Pipeline stage**: Stage 3 + Stage 5.

---

## OCR Evaluation Metrics — Beyond WER and Cosine Similarity

### ANLS* — Universal Document Processing Metric for Generative LLMs
- **arXiv**: https://arxiv.org/abs/2402.03848
- **Year**: 2024
- **Summary**: Extension of ANLS (Average Normalized Levenshtein Similarity) to handle dictionaries and complex nested data structures, not just strings and lists. Standard metric in DocVQA/ST-VQA/LayoutLM/Donut evaluation. Threshold-based: penalizes OCR-recognition errors gently; outputs 0 if NLS < 0.5.
- **Why it matters for Module 2**: ANLS tolerates minor OCR transcription errors (e.g., ก vs. n-look-alikes) without harshly penalizing correct answers — better fit for Thai script than WER.
- **Pipeline stage**: Stage 6 (Validation) + Module 2 upgrade.

### BERTScore for LLM Evaluation
- **Reference**: https://www.analyticsvidhya.com/blog/2025/04/bertscore-a-contextual-metric-for-llm-evaluation/
- **Summary**: Uses contextual BERT embeddings for semantic similarity scoring. Better than cosine similarity on generic SentenceTransformer because it is token-level and alignment-aware. Limitations: computationally heavier; multilingual BERT required for Thai.
- **Relevance to Module 2**: Drop-in upgrade to cosine similarity score using wangchanberta or multilingual-BERT as the scorer.

### Multi-Layer Evaluation: Fusion of Metrics + LLM-as-Judge (COLING 2025)
- **Reference**: https://aclanthology.org/2025.coling-main.408.pdf
- **Summary**: Combines BERTScore, retrieval metrics, and domain-adapted LLM-as-judge for semantic coherence assessment of generated text. Shows LLM-as-judge can catch errors missed by lexical/embedding metrics.
- **Relevance to Module 2**: Recipe for a 3-layer OCR evaluation: CER/WER (lexical) + ANLS (character-tolerant) + LLM-judge (semantic/domain-aware).

### Thai WER Tokenization Bias
- **Reference**: ThaiWav2Vec2 paper (arXiv:2208.04799) + Gladia WER blog
- **Key finding**: Thai WER scores differ significantly by tokenizer choice — NewMM gives WER ~13.6%, deepcut gives ~8.2% for the same ASR system. This means Module 2's WER figure is tokenizer-relative, not absolute. Any comparison across systems must fix the tokenizer.
- **Implication**: Reporting WER with "PyThaiNLP newmm" is valid only if all compared systems use the same engine and version.

---

## Multimodal Product Understanding

### Multimodal E-Commerce Framework (ScienceDirect 2025)
- **Reference**: https://www.sciencedirect.com/article/pii/S2667096825000370
- **Summary**: BiLens-style framework combining ViT + LLM for product caption generation and retrieval. Evaluates BLIP-2, ViT-GPT2, Florence-2-large, GIT.
- **Pipeline stage**: Module 1 upgrade — replace 700-char threshold heuristic with VLM-based content classifier.

### Zero-Shot VLM Classification with Contrastive Descriptions (CVPR 2024)
- **Reference**: https://openaccess.thecvf.com/content/CVPR2024/papers/Saha_Improved_Zero-Shot_Classification_by_Adapting_VLMs_with_Text_Descriptions_CVPR_2024_paper.pdf
- **Summary**: LLM generates contrastive text descriptions to resolve ambiguous VLM classifications. Directly applicable to ad-image vs. product-label classification without training data.
- **Pipeline stage**: Module 1 — replace or augment 700-char text-length threshold.

### Multimodal Product Deduplication (arXiv 2025)
- **Reference**: https://arxiv.org/html/2509.15858v2
- **Summary**: Multimodal embeddings (text + image) for product deduplication. Macro F1 = 0.90. Validates that joint image+text representations outperform text-only or image-only approaches.
- **Pipeline stage**: Module 1 extension — de-duplicate product entries before classification.

---

## Multilingual / Low-Resource VLM

### Large Multimodal Models for Low-Resource Languages: A Survey (ScienceDirect 2026)
- **Reference**: https://www.sciencedirect.com/science/article/pii/S1566253526000680
- **Summary**: Survey of strategies for low-resource language VLMs: cross-lingual transfer, instruction tuning on translated data, hallucination-aware preference optimization. Thai is included in the low-resource multimodal challenge cluster.
- **Relevance**: Framing for why Typhoon-OCR approach (Thai-specific fine-tuning) is necessary vs. using general-purpose Qwen2.5-VL zero-shot.

### Cross-Lingual Transfer for Low-Resource Language VLMs (ACM MM 2023)
- **Reference**: https://dl.acm.org/doi/10.1145/3581783.3611992
- **Summary**: Visually-derived supervision for cross-lingual transfer; proposes using image-text alignment as a bridge when parallel text corpora are sparse. Applicable to Thai medical domain where annotated data is scarce.
- **Pipeline stage**: Stage 4 (Post-correction fine-tuning under data scarcity).

---

## Deep-Dive Additions (2026-05-06)

### ThaiOCRBench Hugging Face Dataset Card
- **Reference**: https://huggingface.co/datasets/typhoon-ai/ThaiOCRBench/blob/main/README.md
- **Summary**: Confirms dataset fields (`image`, `Task`, `question`, `answer`, `category`), test split size of 2,808 samples, and 13 task categories.
- **Relevance**: Direct schema template for an internal NECTEC product/medical OCR benchmark.

### Typhoon OCR Hugging Face Model Card
- **Reference**: https://huggingface.co/typhoon-ai/typhoon-ocr-7b
- **Summary**: Bilingual Thai-English document parsing model based on Qwen2.5-VL-Instruct. Supports structured documents and outputs Markdown/HTML/figure tags, but is task-specific and may hallucinate.
- **Relevance**: Use as Stage 3+4+5 VLM baseline, but pair with verifier/validation before downstream use.

### mPLUG-DocOwl2
- **Reference**: https://arxiv.org/abs/2409.03420
- **Summary**: OCR-free high-resolution multi-page document understanding with visual token compression.
- **Relevance**: Useful if the project expands from single images to multi-page PDFs or long documents.

### Thai-Light Multimodal CLIP/Distill
- **Reference**: https://huggingface.co/patomp/thai-light-multimodal-clip-and-distill
- **Summary**: Thai image-text feature extraction candidate trained/evaluated on Thai MS COCO-style data.
- **Relevance**: Lightweight candidate for product image-text alignment, but not validated for OCR/product-label text.

### Jina CLIP v2
- **Reference**: https://huggingface.co/tomaarsen/jina-clip-v2
- **Summary**: General multilingual image-text embedding model supporting many languages and 512x512 images.
- **Relevance**: Strong multilingual baseline for product image-text alignment and mismatch detection.

### Qwen2.5-VL Architecture Notes
- **Reference**: https://deepwiki.com/QwenLM/Qwen2.5-VL/2-model-architecture
- **Summary**: Describes Qwen2.5-VL as a specialized vision encoder plus large language model, with dynamic resolution processing, streamlined ViT/window attention, multimodal RoPE, and memory/quantization notes.
- **Relevance**: Source for the Qwen2.5-VL conceptual architecture diagram in [/research/diagrams/vlm-thai-ocr-architecture-map-2026-05-06.md](/research/diagrams/vlm-thai-ocr-architecture-map-2026-05-06.md).

### mPLUG-DocOwl System Architecture Notes
- **Reference**: https://deepwiki.com/X-PLUG/mPLUG-DocOwl/1.2-system-architecture
- **Summary**: Describes the DocOwl family as OCR-free document understanding models with three core components: vision tower, multimodal fusion, and LLM decoder.
- **Relevance**: Source for the OCR-free document architecture diagram in [/research/diagrams/vlm-thai-ocr-architecture-map-2026-05-06.md](/research/diagrams/vlm-thai-ocr-architecture-map-2026-05-06.md).
