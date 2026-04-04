# Last Updated: 2026-04-04

### Do As I Can, Not As I Say (SayCan)
**Source**: https://say-can.github.io/
**Topic(s)**: nlp-for-robot-planning, language-grounding, long-horizon-robot-tasks
**Summary**: SayCan combines language-model skill usefulness with robot affordance/value scores to select executable next actions. The system is designed to bridge high-level natural language goals and low-level robot skills in real environments. Reported updates with PaLM-SayCan improve planning and execution reliability over earlier LM variants.
**Key Points**:
- Core scoring combines semantic relevance from LLM with feasibility from value functions.
- Demonstrates long-horizon task execution in kitchen-like service settings.
- Reported PaLM-SayCan numbers: 84% correct skill sequence selection and 74% successful execution.
- Shows multilingual query handling and chain-of-thought style prompting integration.
**Referenced / Related**:
- arXiv 2204.01691 (SayCan paper) - foundational affordance-grounded language planning.
- Inner Monologue follow-up - closed-loop feedback extension beyond one-step affordance scoring.
- Tabletop SayCan code release - practical reproduction and benchmarking entry point.
**Ideas / Gaps**:
- Need standardized benchmark for failure recovery after mid-plan execution errors.
- Compare open-loop skill selection vs closed-loop replanning under sensor noise.
