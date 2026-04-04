# Last Updated: 2026-04-04 (top-3 thesis picks added)

# Topic: NLP and Robotics

## Included Sources
- ../sources/saycan-grounding-language-robotic-affordances-2026-04-04.md
- ../sources/rt-2-vla-robot-control-2026-04-04.md
- ../sources/openvla-open-source-vla-2026-04-04.md
- ../references/refs-nlp-robotics.md

## Topic Summary
This topic focuses on connecting natural language understanding to executable robotic behavior. Current directions converge on language-grounded planning (SayCan) and unified vision-language-action policies (RT-2, OpenVLA), with a key trade-off between broad semantic generalization, controllability, compute cost, and safety.

## Subtopics
- Language grounding with affordances and skill libraries
- Vision-language-action policy learning
- Open-source embodied foundation models
- Efficient adaptation to new robots and tasks
- Safety, verification, and failure recovery in language-driven control

## Candidate Research Questions
- How to combine open VLA policies with explicit symbolic constraints for safer execution?
- Which adaptation strategy gives best sample efficiency across robot embodiments?
- How robust are language-conditioned policies to multilingual commands and ambiguity?
- Can closed-loop feedback (scene descriptors, success detectors) reduce cascading errors in long-horizon tasks?

## Open Threads
- Build a small reproducible benchmark: instruction complexity x environment shift x safety violations.
- Compare open models (OpenVLA-like) vs closed/co-trained models (RT-2-style) on semantic OOD tasks.
- Design human-in-the-loop override and intervention metrics for real deployment.

## Top 3 Thesis Picks (Selected)

### 1) Safe Action Token Decoding for Open VLA Policies
- Why this is top: Strong novelty and direct safety impact in real deployment; connects NLP intent parsing to robotics execution constraints.
- Core question: How to insert symbolic safety constraints and affordance checks between language-conditioned action tokens and actuator commands?
- Difficulty: High
- Resource needs: 1 robot platform, simulator fallback, safety-rule engine, medium-to-high GPU budget for policy adaptation.
- Minimum experiment set:
	- Baseline OpenVLA-style policy without safety layer.
	- Constrained decoding with forbidden-action masks and state-aware guards.
	- Compare task success, safety-violation rate, and recovery time.

### 2) Thai-English Multilingual Grounding for Long-Horizon Manipulation
- Why this is top: Good novelty for local context and highly practical for service robots; tractable timeline for a master's thesis.
- Core question: How robust are language-grounded robot policies to Thai-English code-switch, ambiguity, and paraphrase drift?
- Difficulty: Medium-High
- Resource needs: robot or sim benchmark, bilingual instruction set, modest GPU budget for adaptation/evaluation.
- Minimum experiment set:
	- Build multilingual instruction splits (Thai, English, code-switch).
	- Evaluate grounding error types (object mismatch, relation mismatch, step omission).
	- Test clarification prompts and confidence-triggered replanning.

### 3) Data-Efficient OpenVLA Adaptation with LoRA Under Real-World Shift
- Why this is top: Highest feasibility and strong engineering value; excellent if you want publishable, reproducible systems work quickly.
- Core question: Which parameter-efficient method (LoRA/partial tuning) gives best sample efficiency across camera/background/robot shifts?
- Difficulty: Medium
- Resource needs: open checkpoints, one target robot setup (or high-fidelity sim), moderate GPU budget.
- Minimum experiment set:
	- Compare full finetune vs LoRA vs last-layer tuning.
	- Measure success vs number of demos and domain shift severity.
	- Report compute-time-memory trade-offs.

## Selection Criteria Used
- Feasibility in 6-12 months
- Novelty and publishability
- Resource fit (compute + data + hardware)
- Practical deployment impact

## Related Diagram
- ../diagrams/nlp-robotics-top3-thesis-picks-2026-04-04.md
