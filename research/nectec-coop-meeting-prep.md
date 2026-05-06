# สรุปเนื้อหาการนำเสนอสหกิจศึกษา (Cooperative Education Presentation)
**หัวข้อ:** การวิเคราะห์ตำแหน่งและจำแนกอวัยวะจากภาพทางการแพทย์ (Location Analysis and Organ Classification from Medical Images)

---

## 1. ภาพรวมและวัตถุประสงค์
โครงการนี้มุ่งเน้นการใช้เทคโนโลยี AI และ Computer Vision เพื่อช่วยสนับสนุนการวินิจฉัยทางการแพทย์ ลดภาระงานของแพทย์ และลดความผิดพลาดในการตีความภาพถ่ายทางการแพทย์ โดยมี 2 งานหลักคือ:
*   **การประมวลผลต่อมลูกหมากจากภาพ CT (Prostate Processing):** เพื่อตรวจจับตำแหน่งและแบ่งส่วน (Segmentation) ต่อมลูกหมาก
*   **การคัดแยกอวัยวะจากภาพทางการแพทย์ (Organ Classification):** เพื่อจำแนกประเภทภาพถ่ายอวัยวะ (เช่น สมอง, ดวงตา) จากแหล่งต่างๆ เช่น MRI, CT, OCT

---

## 2. ประเด็นสำคัญและข้อมูลที่นำเสนอ

### ก. การประมวลผลต่อมลูกหมาก (Prostate)
*   **เทคนิคที่ใช้:** ใช้ **YOLO11** (โมเดล l และ m) สำหรับการทำ Object Detection เพื่อหา Bounding Box และนำไปใช้ร่วมกับ **SAM (Segment Anything Model)** สำหรับการทำ Segmentation
*   **ข้อมูล (Dataset):** 
    *   ชุดที่ 1: ประมาณ 1,400 ภาพ (ทำ Label เอง 300 ภาพ)
    *   ชุดที่ 2: ประมาณ 4,000 ไฟล์ จากโรงพยาบาล (มีการจัดการโครงสร้างข้อมูลและสร้าง Bbox จาก Mask)
*   **ผลการทดลอง:** ทดสอบโมเดลที่ 40 epoch ให้ผลลัพธ์ดีที่สุด (อ้างอิงจากค่า Loss และ mAP50) และทดลองใช้ SAMMed_vit2b.pt เพื่อเพิ่มความแม่นยำในโดเมนการแพทย์
*   **ระบบที่พัฒนา:** เว็บแอปพลิเคชัน (Frontend: Vite+React+TS, Backend: FastAPI)

### ข. การคัดแยกอวัยวะ (Organ Classification)
*   **หมวดหมู่การจำแนก:** Axial Brain, Frontal Brain, Eye OCT, Eye, และ Unknown
*   **การพัฒนาโมเดล:** 
    *   เริ่มต้นใช้ YOLO8 ต่อมาอัปเกรดเป็น **YOLO11n** (สมอง) และ **YOLO11m** (ดวงตา)
    *   มีการแก้ปัญหาโมเดลทายผิดเมื่อภาพถูกหมุน โดยการทำ **Data Augmentation** (หมุน 30 องศา, ขยายภาพ, พลิกภาพ)
*   **ระบบที่พัฒนา:** เว็บแอปพลิเคชัน (Frontend: Vite+React+TS, Backend: FastAPI)

### ค. งานอื่นๆ และกิจกรรม
*   **งานวิจัย/พัฒนาเสริม:**
    *   OCR เอกสารและภาพทางการแพทย์ (Pytesseract)
    *   ระบบแยกสินค้า SME และตัดชื่อสินค้า (PyThaiNLP)
    *   ระบบประมาณการสูญเสียเลือด (Estimate Blood Loss API)
    *   การจำแนก DR Level (Diabetic Retinopathy) ด้วย CLIP และ Roboflow
    *   การทำความสะอาด Dataset ผ้าก๊อซ (Gauze Dataset)
    *   LSTM สำหรับ Human Action Recognition
*   **กิจกรรม:** การเป็นผู้ช่วยสอน (TA) โครงการ AI for Thai ที่ มก. กำแพงแสน และ มทร.ธัญบุรี รวมถึงกิจกรรมภายใน สวทช./NECTEC

---

## 3. จำแนกงานตามสาขา

### Computer Vision (CV)

| งาน | เทคนิค | หมายเหตุ |
|-----|--------|---------|
| Prostate Segmentation | YOLO11 + SAM | Detection → Segmentation pipeline |
| Organ Classification | YOLO11n/m + Data Augmentation | Brain / Eye / OCT |
| DR Level Classification | CLIP + Roboflow | Multimodal — overlap CV+NLP |
| Blood Loss Estimation | Rule-based API | ไม่ใช้ ML |
| Human Action Recognition | LSTM | Video sequence |
| Gauze Dataset Cleaning | Manual / Script | Data prep |

### NLP / ภาษาไทย

| งาน | เทคนิค | จุดเชื่อมกับโปรเจกต์เรา |
|-----|--------|------------------------|
| OCR เอกสาร/ภาพทางการแพทย์ | Pytesseract | Thai Medical OCR pipeline ตรงๆ |
| แยกสินค้า SME + ตัดชื่อสินค้า | PyThaiNLP | Thai text processing / tokenization |

> **สรุป:** งาน NLP ตรงๆ มี 2 งาน (OCR + PyThaiNLP) ส่วนที่เหลือเป็น CV — จุดเชื่อมสำหรับการคุยกับ NECTEC คือ **OCR pipeline** ที่ยังใช้ Pytesseract ซึ่งมีปัญหากับภาษาไทย เปิดโอกาสเสนอ approach ที่ดีกว่าได้

---

## 4. คำถามหรือจุดที่ควรถามในการประชุม

1.  **ด้านประสิทธิภาพ (Performance):**
    *   ค่า mAP50 หรือ Dice Coefficient ของการทำ Prostate Segmentation อยู่ที่เท่าไร และเพียงพอต่อการนำไปใช้งานจริงในทางการแพทย์หรือไม่?
    *   หลังจากการทำ Augmentation ในส่วนของ Organ Classification ความแม่นยำ (Accuracy) เพิ่มขึ้นมากน้อยเพียงใด?

2.  **ด้านการนำไปใช้งาน (Deployment):**
    *   ระบบที่พัฒนาขึ้น (FastAPI + React) มีแผนจะนำไปทดสอบใช้งานจริง (Pilot Test) กับโรงพยาบาลที่เป็นเจ้าของข้อมูลหรือไม่?
    *   การประมวลผลต่อภาพ (Inference Time) ใช้เวลานานเท่าไร หากต้องนำไปรันบนเครื่องคอมพิวเตอร์ทั่วไปในโรงพยาบาล?

3.  **ด้านข้อมูล (Dataset):**
    *   ปัญหาเรื่องความแตกต่างของข้อมูล (Data Variability) จากต่างแหล่งที่มา (เช่น จาก Kaggle เทียบกับข้อมูลโรงพยาบาล) ส่งผลต่อประสิทธิภาพของโมเดลอย่างไร?
    *   มีการทำ Data Privacy หรือ Anonymization อย่างไรสำหรับข้อมูลที่ได้มาจากโรงพยาบาล?

4.  **แผนงานในอนาคต:**
    *   มีแผนจะขยายขอบเขตไปยังอวัยวะอื่นๆ หรือไม่?
    *   งาน OCR ที่พัฒนาขึ้น มีความแม่นยำเพียงพอในการสกัดข้อมูลตัวเลขสำคัญจากเอกสารแพทย์หรือไม่? (เนื่องจาก Pytesseract มักมีปัญหากับภาษาไทยและฟอนต์เฉพาะทาง)
