# Last Updated: 2026-03-31

# Diagram: Thai Medical OCR — System Comparison (A vs B vs C vs D)

```mermaid
flowchart LR
    subgraph A["A: OCR-only ⚡ เร็วสุด"]
        A1[OCR Engine] --> A2[Regex/Rule] --> A3[JSON]
    end

    subgraph B["B: OCR + LM ⚠️ เสี่ยง"]
        B1[OCR Engine] --> B2[Language Model\nUnconstrained] --> B3[JSON]
    end

    subgraph C["C: OCR + Constrained ✅ ปลอดภัยขึ้น"]
        C1[OCR Engine] --> C2[LM + Lexicon Lock\n+ Unit Rules] --> C3[JSON]
    end

    subgraph D["D: VLM + Constrained 🎯 เป้าหมาย"]
        D1[VLM\nภาพ+Layout+ข้อความ] --> D2[Constrained\nPost-correction] --> D3[JSON]
    end

    IMG([📄 ภาพ]) --> A1 & B1 & C1 & D1
```

## Summary Table

| ระบบ | เข้าใจ Layout | ทนต่อ Noise | ปลอดภัย Medical Term | ความเร็ว |
|---|---|---|---|---|
| A: OCR-only | ❌ | ต่ำ | ✅ (ไม่แตะ) | เร็วสุด |
| B: OCR+LM | ❌ | ปานกลาง | ❌ เสี่ยง | ปานกลาง |
| C: OCR+Constrained | ❌ | ปานกลาง | ✅ | ปานกลาง |
| D: VLM+Constrained | ✅ | สูง | ✅ | ช้ากว่า แต่แม่นกว่า |

## Related
- Topic: [../topics/thai-medical-ocr-post-correction.md](../topics/thai-medical-ocr-post-correction.md)
- Pipeline diagram: [pipeline-thai-medical-ocr-modular.md](pipeline-thai-medical-ocr-modular.md)
- Experiment Plan: [../ideas/experiment-plan-thai-medical-ocr-2026-03-31.md](../ideas/experiment-plan-thai-medical-ocr-2026-03-31.md)
