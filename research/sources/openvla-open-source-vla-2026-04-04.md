# Last Updated: 2026-04-04

### OpenVLA: Open-Source Vision-Language-Action Model
**Source**: https://openvla.github.io/
**Topic(s)**: open-source-vla, robot-policy-transfer, efficient-finetuning
**Summary**: OpenVLA presents an open 7B VLA model trained on Open X-Embodiment episodes, aiming for multi-robot manipulation generalization and accessible fine-tuning workflows. It emphasizes practical adaptation to new robots and tasks through parameter-efficient methods.
**Key Points**:
- Uses a fused visual encoder plus LLM backbone to predict tokenized robot actions.
- Trained on 970k robot episodes; checkpoints and training pipeline are open.
- Reports strong out-of-the-box cross-platform manipulation performance.
- LoRA-style adaptation shows favorable performance-memory trade-offs for downstream tuning.
**Referenced / Related**:
- arXiv 2406.09246 (OpenVLA) - canonical paper citation.
- Open X-Embodiment dataset - main pretraining corpus.
- Comparison against RT-2-X, Octo, and Diffusion Policy - evaluation framing.
**Ideas / Gaps**:
- Investigate failure cases on semantic tasks requiring internet-scale world knowledge.
- Benchmark robustness to domain shifts in camera setup, lighting, and distractors.
