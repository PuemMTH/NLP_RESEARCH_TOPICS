# Last Updated: 2026-03-31

# Diagram: Research File Link Map

```mermaid
graph TD
    subgraph topics["📂 topics/"]
        T1([thai-medical-ocr-post-correction.md])
        T2([technical-profile-and-career.md])
    end

    subgraph sources["📂 sources/"]
        S1([thai-medical-ocr-post-correction-2026-03-31.md])
        S2([tanapat-eiam-arj-profile-cv.md])
    end

    subgraph references["📂 references/"]
        R1([refs-thai-medical-ocr-post-correction.md])
        R2([refs-nlp-broad-topics.md])
        R3([refs-tanapat-profile.md])
    end

    subgraph ideas["📂 ideas/"]
        I1([draft-proposal-thai-medical-ocr-masters.md])
        I2([experiment-plan-thai-medical-ocr.md])
        I3([ideas-2026-03.md])
    end

    subgraph diagrams["📂 diagrams/"]
        D1([pipeline-thai-medical-ocr-modular.md])
        D2([system-comparison-ocr-abcd.md])
    end

    T1 --> S1
    T1 --> I1
    T1 --> I2
    T1 --> D1
    T1 --> D2

    T2 --> S2

    S1 --> R1
    S2 --> R3

    I1 --> S1
    I2 --> S1
    I3 --> S1

    D1 --> T1
    D1 --> I2
    D2 --> T1
    D2 --> I2
```

## Notes
- อัปเดต diagram นี้ทุกครั้งที่เพิ่มไฟล์ใหม่เข้า research/
- refs-nlp-broad-topics.md ยังไม่มี topic เชื่อมโยง (orphan) — เป็น reference กลางที่ยังไม่ผูกกับ topic เฉพาะ
