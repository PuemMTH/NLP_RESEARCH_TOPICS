# Last Updated: 2026-04-04

### RT-2: Vision-Language-Action Model
**Source**: https://deepmind.google/discover/blog/rt-2-new-model-translates-vision-and-language-into-action/
**Topic(s)**: vision-language-action, embodied-reasoning, generalization-in-robotics
**Summary**: RT-2 reframes robot actions as tokens and co-fine-tunes vision-language backbones on web and robot data to produce executable control policies. The approach targets broader generalization and transfer of semantic knowledge from web-scale pretraining to real robotic tasks.
**Key Points**:
- Converts low-level robot actions into token sequences compatible with VLM/LLM pipelines.
- Reports strong gains on unseen scenarios and emergent skills over earlier baselines.
- Highlights ability to preserve in-distribution task performance while improving OOD behavior.
- Explores plan-and-act behavior with language reasoning traces before action tokens.
**Referenced / Related**:
- RT-2 paper PDF (robotics-transformer2.github.io/assets/rt2.pdf) - primary technical source.
- RT-1 baseline and Language Table benchmark links - reproducibility and comparison context.
- PaLM-E and PaLI-X backbones - transfer learning design choices.
**Ideas / Gaps**:
- Open question on safety filters for action-token decoding in human-shared spaces.
- Need cost-performance studies for smaller open models under similar generalization tests.
