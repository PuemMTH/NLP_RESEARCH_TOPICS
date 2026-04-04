# Last Updated: 2026-04-04

# Proposal Pack: Baselines, Metrics, and Ablations

## Scope
- Primary stack: Voyager/JARVIS-style agent for Minecraft instruction following.
- Proposed contribution line: constrained action decoding + reflection-based replanning.

## Benchmark Setup
- Environment: MineDojo-compatible Minecraft tasks (or equivalent reproducible setup).
- Task buckets:
  - T1: Short-horizon instruction following (1-3 steps)
  - T2: Mid-horizon tool-use tasks (4-8 steps)
  - T3: Long-horizon compositional tasks (9+ steps)
  - T4: Robustness split (unseen phrasing, distractors, partial observability)
- Language splits:
  - L1: English
  - L2: Thai-English code-switch
  - L3: Paraphrase/ambiguous commands

## Baselines
- B0 Scripted Skill Graph (non-LLM planner)
  - Fixed symbolic planner over predefined skill graph.
  - Purpose: lower-bound and sanity-check baseline.
- B1 Voyager-style Agent
  - Standard planner + code/tool generation + memory loop.
  - Purpose: strong open baseline for long-horizon Minecraft tasks.
- B2 JARVIS-style Planner-Executor
  - Instruction decomposition + multimodal policy/execution modules.
  - Purpose: stronger decomposition-focused baseline.
- B3 Proposed P1 (Voyager/JARVIS hybrid)
  - Unified planner-executor with explicit skill library retrieval.
- B4 Proposed P2 (P1 + constrained action decoding)
  - Valid-action masking and state-aware action constraints before execution.
- B5 Proposed P3 (P2 + reflection/replanning)
  - Error diagnosis + replan trigger from uncertainty and failure signals.

## Metrics

### Primary Outcome Metrics
- Task Success Rate (TSR): fraction of tasks completed within budget.
- Weighted Success Score (WSS): success weighted by task difficulty.
- Horizon Completion Rate (HCR): completion rate per horizon bucket (T1/T2/T3).

### Grounding and Safety Metrics
- Instruction Grounding Accuracy (IGA): percent of steps aligned to instruction intent.
- Invalid Action Rate (IAR): invalid actions per episode.
- Safety Violation Rate (SVR): forbidden/unsafe actions per episode.
- Recovery Success Rate (RSR): fraction of failed episodes recovered after replanning.

### Efficiency Metrics
- Steps-to-Success (STS): mean environment steps for successful episodes.
- Token/Prompt Cost (TPC): average model token usage per episode.
- Wall-clock per Episode (WPE): runtime latency.
- GPU-hour per 1k episodes (GHE): compute budget efficiency.

### Robustness and Generalization Metrics
- OOD Success Drop (OSD): TSR drop from in-distribution to robustness split T4.
- Paraphrase Robustness (PR): TSR under paraphrased commands.
- Code-switch Robustness (CR): TSR under Thai-English instructions.
- Distractor Robustness (DR): TSR with irrelevant objects/events.

## Metric Definitions (for proposal appendix)
- TSR = completed_tasks / total_tasks
- IAR = invalid_actions / total_actions
- SVR = safety_violations / total_episodes
- RSR = recovered_failures / total_failures
- OSD = TSR_ID - TSR_OOD

## Ablation Plan
- A1 minus Memory Module
  - Remove episodic memory/tool history retrieval.
  - Tests value of memory for long-horizon completion.
- A2 minus Reflection Module
  - Disable self-critique and replan generation.
  - Tests contribution to failure recovery.
- A3 minus Constrained Decoding
  - Execute unconstrained action outputs.
  - Tests safety and invalid-action impact.
- A4 minus Uncertainty Trigger
  - Always execute without confidence gating.
  - Tests robustness under ambiguous instructions.
- A5 minus Skill Retrieval
  - Replace retrieval with direct free-form planning only.
  - Tests benefit of explicit skill library grounding.
- A6 Language-only English
  - Remove code-switch and multilingual training/eval.
  - Tests multilingual contribution.

## Experimental Matrix (minimal publishable set)
- Compare B0-B5 on T1-T4 with L1-L3.
- Run at least 3 random seeds per condition.
- Report mean and 95% CI for TSR, IAR, SVR, RSR, OSD.
- Include cost table: WPE, TPC, GHE.

## Statistical Testing
- Success-rate comparisons: bootstrap CI and McNemar test where paired episodes exist.
- Cost/performance trade-off: Pareto plot (TSR vs GHE, TSR vs WPE).
- Robustness analysis: two-way ANOVA style factor analysis (task bucket x language split) when assumptions hold; otherwise non-parametric alternative.

## Threats to Validity
- Environment bias from benchmark-specific mechanics.
- Prompt sensitivity across runs.
- Potential leakage from handcrafted skill libraries.

## Expected Claim Structure
- Claim 1: P2 reduces IAR and SVR over B1/B2 with minimal TSR drop.
- Claim 2: P3 improves RSR and OOD robustness over P2.
- Claim 3: Multilingual setup improves CR while maintaining competitive TSR.

## Related Diagram
- ../diagrams/evaluation-framework-minecraft-nlp-robotics-2026-04-04.md
