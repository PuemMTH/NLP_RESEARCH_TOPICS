# Last Updated: 2026-05-06

# References: LoRA/QLoRA Fine-Tuning for VLMs — May 2026

Topic: Fine-tuning vision-language models with LoRA/QLoRA, specifically for Qwen3-VL-based models and document OCR tasks.

---

## Primary Sources (Fetched and Verified)

### 1. Typhoon OCR Paper (arXiv 2601.14722)
**URL**: https://arxiv.org/html/2601.14722
**Authors**: SCB10X
**Key data**:
- V1.5 trained on 155,403 samples (doubled from 77,029 in V1)
- Base model for V1.5: Qwen3-VL 2B
- Training: full-parameter SFT on 4×H100, 2 epochs
- Data mix: synthetic structured docs (37.6%), general infographics (45.6%), Thai financial reports (7.2%), Thai books (5.6%), handwritten (5.5%), scanned (6.2%)
- No medical documents in training set — confirms domain gap

### 2. HuggingFace Model Card: scb10x/typhoon-ocr1.5-2b
**URL**: https://huggingface.co/scb10x/typhoon-ocr1.5-2b
**Key data**:
- Confirmed slug: `scb10x/typhoon-ocr1.5-2b`
- Base: `Qwen/Qwen3-VL-2B-Instruct`
- Tensor type: BF16, Apache 2.0 license
- CRITICAL: Model only works with the canonical prompt provided in the model card. Non-standard prompts break performance.
- Output format: Markdown with `<table>` HTML, LaTeX `$...$`/`$$...$$`, `<figure>`, `<page_number>`, ☐/☑ checkboxes

### 3. Phil Schmid — Fine-Tune Multimodal LLMs with TRL
**URL**: https://www.philschmid.de/fine-tune-multimodal-llms-with-trl
**Key data**:
- LoRA r=8, alpha=16, dropout=0.05, target=["q_proj","v_proj"], task_type="CAUSAL_LM"
- SFT on ~1,000 samples, 3 epochs, g6.2xlarge (24GB GPU), wall-clock ~1.5h
- QLoRA: load_in_4bit=True, bnb_4bit_use_double_quant=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=bfloat16
- SFTConfig: lr=2e-4, per_device_train_batch_size=4, gradient_accumulation_steps=8, num_train_epochs=3, max_grad_norm=0.3, warmup_ratio=0.03

### 4. Shaaf Salman — Fine-Tuning Qwen3-VL-30B-MoE with LoRA
**URL**: https://medium.com/@ishaafsalman/fine-tuning-qwen-qwen3-vl-30b-a3b-moe-architecture-with-lora-2365359e870f
**Key data**:
- Full projection set: target=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"]
- r=64, alpha=128, dropout=0.05
- 8×A100 80GB, 24–36h per 3 epochs
- ZeRO-2 recommended (ZeRO-3 breaks LoRA gradient flow)
- 53M trainable params = 0.17% of 31B total

### 5. Nanonets — Fine-Tuning VLMs for Data Extraction
**URL**: https://nanonets.com/blog/fine-tuning-vision-language-models-vlms-for-data-extraction/
**Key data**:
- Qwen2-VL-2B, CORD dataset, 800 training samples × 10 epochs
- ~20GB GPU VRAM, ~30 min training time
- Recommended sample target: "10,000 to 100,000 total training samples based on variation in the image"
- For limited data (200–800 pages): LoRA outperforms full fine-tune

### 6. 2U1/Qwen-VL-Series-Finetune (GitHub)
**URL**: https://github.com/2U1/Qwen-VL-Series-Finetune
**Key data**:
- Supports Qwen2-VL, Qwen2.5-VL, Qwen3-VL including LoRA and QLoRA
- Data format: LLaVA-style JSON with image paths and multi-turn conversation
- Vision LR typically 5–10× smaller than language model LR
- QLoRA with vision modules requires 16-bit precision for vision encoder

### 7. Unsloth — Qwen3-VL Run & Fine-tune
**URL**: https://unsloth.ai/docs/models/tutorials/qwen3-how-to-run-and-fine-tune/qwen3-vl-how-to-run-and-fine-tune
**Key data**:
- Unsloth claims 1.7× faster training, 60% less VRAM for Qwen3-VL
- Supports 2B, 4B, 8B, 32B Qwen3-VL
- Notebooks available and runnable on Colab for 8B; 2B is lighter
- Estimated throughput: 140k examples ≈ 13h, 160k examples ≈ 16h on consumer hardware

### 8. HuggingFace Cookbook — Fine-Tuning VLM with TRL
**URL**: https://huggingface.co/learn/cookbook/en/fine_tuning_vlm_trl
**Key data**:
- Standard Qwen2-VL recipe using SFTTrainer
- process_vision_info() required for image preprocessing in data collator
- OpenAI-style conversation format (system, user, assistant roles)

---

## Dataset Sources Found (Thai / Medical)

| Dataset | URL | Notes |
|---------|-----|-------|
| openthaigpt/thai-ocr-evaluation | https://huggingface.co/datasets/openthaigpt/thai-ocr-evaluation | General Thai OCR eval; not medical |
| iapp/thai_handwriting_dataset | https://huggingface.co/datasets/iapp/thai_handwriting_dataset | Used in Typhoon OCR training (5.5%) |
| lst-nectec/lst20 | https://huggingface.co/datasets/lst-nectec/lst20 | Text-only NLP corpus (NER, POS); no images |
| MedOCR-Vision Dataset | https://huggingface.co/datasets/naazimsnh02/medocr-vision-dataset | English medical OCR dataset; useful as a structure template |

**Conclusion**: No public Thai medical document OCR dataset with annotated images exists. Training data must be constructed in-house.

---

## Useful Community Resources

- Qwen3-VL issues tracker: https://github.com/QwenLM/Qwen3-VL/issues
- DataCamp fine-tuning Qwen3-VL-8B: https://www.datacamp.com/tutorial/fine-tuning-qwen3-vl-8b
- ROCm LoRA Qwen2-VL guide: https://rocm.docs.amd.com/projects/ai-developer-hub/en/latest/notebooks/fine_tune/fine_tuning_lora_qwen2vl.html
