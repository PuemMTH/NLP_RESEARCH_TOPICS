# Last Updated: 2026-04-04

# OpenVLA Variants, Extensions, and Minecraft Evidence (Web Scan)

## Official OpenVLA and Checkpoints
- OpenVLA main repository (latest updates mention OFT and FAST): https://github.com/openvla/openvla
- OpenVLA project page: https://openvla.github.io/
- OpenVLA HF org models list: https://huggingface.co/openvla/models
- OpenVLA 7B checkpoint: https://huggingface.co/openvla/openvla-7b
- OpenVLA README mentions early checkpoint openvla-v01-7b: https://github.com/openvla/openvla#pretrained-vlas
- Prismatic-compatible checkpoint referenced for full fine-tuning: https://huggingface.co/openvla/openvla-7b-prismatic
- Official LIBERO fine-tuned checkpoints referenced in README:
  - https://huggingface.co/openvla/openvla-7b-finetuned-libero-spatial
  - https://huggingface.co/openvla/openvla-7b-finetuned-libero-object
  - https://huggingface.co/openvla/openvla-7b-finetuned-libero-goal
  - https://huggingface.co/openvla/openvla-7b-finetuned-libero-10

## OpenVLA Extensions / Tools
- OpenVLA-OFT project page: https://openvla-oft.github.io/
- OpenVLA-OFT code repository: https://github.com/moojink/openvla-oft
- FAST tokenizer research page: https://www.pi.website/research/fast
- FAST tokenizer HF model: https://huggingface.co/physical-intelligence/fast
- TensorRT-OpenVLA deployment/acceleration pipeline: https://github.com/rail-berkeley/tensorrt-openvla

## OpenVLA + Minecraft Evidence Checks
- GitHub repo search for "OpenVLA Minecraft": 0 repositories
  - https://github.com/search?q=OpenVLA+Minecraft&type=repositories
- GitHub discussions search for "OpenVLA Minecraft": 0 discussions
  - https://github.com/search?q=OpenVLA+Minecraft&type=discussions
- OpenVLA official issues search for "Minecraft": no results
  - https://github.com/openvla/openvla/issues?q=Minecraft
- arXiv result for "OpenVLA Minecraft": D2E, where Minecraft appears in context of VPT comparison; not an OpenVLA-on-Minecraft implementation
  - https://arxiv.org/abs/2510.05684

## Adjacent Minecraft VLA / Agent Lines (Not OpenVLA)
- OmniJARVIS (VLA for Minecraft): https://arxiv.org/abs/2407.00114
- JARVIS-VLA (visual games with keyboard/mouse): https://arxiv.org/abs/2503.16365
- OpenHA (hierarchical agentic models in Minecraft): https://arxiv.org/abs/2509.13347
- MAIN-VLA (open-world Minecraft and PvP settings): https://arxiv.org/abs/2602.02212
- Voyager (LLM lifelong agent in Minecraft):
  - https://voyager.minedojo.org/
  - https://arxiv.org/abs/2305.16291
  - https://github.com/MineDojo/Voyager
- VPT (Minecraft agents from unlabeled videos):
  - https://arxiv.org/abs/2206.11795
  - https://github.com/openai/Video-Pre-Training
- MineDojo benchmark/platform:
  - https://arxiv.org/abs/2206.08853
  - https://github.com/MineDojo/MineDojo

## Notes on Evidence Strength
- Confirmed (strong): no direct public OpenVLA+Minecraft repo in GitHub search results and no "Minecraft" issue in official openvla/openvla issues at scan time.
- Weak/indirect: one commit and one issue mention in broad GitHub search are in index/digest style repositories, not implementation repos.
- Adjacent evidence is stronger for non-OpenVLA Minecraft work (OmniJARVIS, JARVIS-VLA, OpenHA, MAIN-VLA, Voyager, VPT, MineDojo).
