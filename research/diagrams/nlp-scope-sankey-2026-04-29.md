# NLP Scope Overview — Sankey Graph
# Last Updated: 2026-04-29

```mermaid
sankey-beta

"NLP Research","Natural Language Understanding",30
"NLP Research","Natural Language Generation",25
"NLP Research","Information Extraction",15
"NLP Research","Multimodal & Document AI",20
"NLP Research","Machine Translation",10

"Natural Language Understanding","Text Classification",10
"Natural Language Understanding","Question Answering",10
"Natural Language Understanding","NER & Sequence Labeling",10

"Natural Language Generation","LLM & Text Generation",12
"Natural Language Generation","Summarization",8
"Natural Language Generation","Dialogue Systems",5

"Information Extraction","Relation Extraction",6
"Information Extraction","Event Detection",5
"Information Extraction","Knowledge Graph",4

"Multimodal & Document AI","OCR & Document AI",9
"Multimodal & Document AI","Vision-Language Models",7
"Multimodal & Document AI","Speech & ASR",4

"Machine Translation","Neural MT",6
"Machine Translation","Low-resource & Thai NLP",4

"Text Classification","Healthcare",3
"Text Classification","Finance",3
"Text Classification","Legal",2
"Text Classification","General Apps",2

"Question Answering","Healthcare",3
"Question Answering","Education",4
"Question Answering","General Apps",3

"NER & Sequence Labeling","Healthcare",4
"NER & Sequence Labeling","Legal",3
"NER & Sequence Labeling","Finance",3

"LLM & Text Generation","General Apps",5
"LLM & Text Generation","Code & Dev Tools",4
"LLM & Text Generation","Education",3

"Summarization","Healthcare",3
"Summarization","Legal",3
"Summarization","General Apps",2

"Dialogue Systems","Healthcare",2
"Dialogue Systems","General Apps",3

"Relation Extraction","Healthcare",3
"Relation Extraction","Legal",3

"Event Detection","Finance",3
"Event Detection","General Apps",2

"Knowledge Graph","Healthcare",2
"Knowledge Graph","General Apps",2

"OCR & Document AI","Healthcare",5
"OCR & Document AI","Legal",2
"OCR & Document AI","Finance",2

"Vision-Language Models","Healthcare",3
"Vision-Language Models","General Apps",4

"Speech & ASR","Education",2
"Speech & ASR","General Apps",2

"Neural MT","General Apps",4
"Neural MT","Education",2

"Low-resource & Thai NLP","Healthcare",2
"Low-resource & Thai NLP","Education",2
```

## โครงสร้าง 3 ชั้น

| ชั้น | หมวด | คำอธิบาย |
|------|------|-----------|
| 1 | NLP Research | จุดเริ่มต้น — งานวิจัย NLP ทั้งหมด |
| 2 | Core Areas | 5 กลุ่มหลัก (NLU, NLG, IE, Multimodal, MT) |
| 3 | Tasks | งานย่อยใต้แต่ละกลุ่ม (QA, OCR, NER, ฯลฯ) |
| 4 | Domains | ด้านการประยุกต์ใช้ (Healthcare, Legal, Finance, Education, General) |

## หมายเหตุ
- **ความกว้างของเส้น** = สัดส่วนความสำคัญ/ปริมาณงานวิจัย (ตัวเลขเชิงสัมพัทธ์)
- **OCR & Document AI** → Healthcare เป็นเส้นหลักของโปรเจกต์นี้ (Thai Medical OCR Pipeline)
- **Low-resource & Thai NLP** แยกออกมาเพื่อเน้น context ภาษาไทย
