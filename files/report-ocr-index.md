# สรุปรายงานการพัฒนาและทดสอบระบบ OCR (REPORT OCR)

---

## 1. ภาพรวมและขอบเขตงาน
รายงานฉบับนี้ครอบคลุมการวิจัยและพัฒนาระบบ OCR (Optical Character Recognition) โดยเน้นภาษาไทยและภาษาอังกฤษ ตั้งแต่การสร้างชุดข้อมูลจำลอง (Synthetic Dataset) การสร้างโมเดลตรวจจับข้อความ (Text Detection) ไปจนถึงการรู้จำข้อความ (Text Recognition) และการประยุกต์ใช้กับภาพทางการแพทย์ (DICOM)

---

## 2. เครื่องมือและ Pipeline ที่ใช้

### **ส่วนที่ 1: การจัดการข้อมูล (Data Generation & Preprocessing)**
*   **Dataset Generation:** ใช้เครื่องมือหลายตัวเพื่อสร้างภาพข้อความจำลอง:
    *   **TRDG (Text Recognition Data Generator):** ใช้สร้างภาพคำ/ประโยค (รองรับไทย-อังกฤษ)
    *   **SynthText:** ใช้สำหรับสร้างภาพข้อความที่มีความซับซ้อนตามสภาพแวดล้อม
    *   **Synthtiger:** เครื่องมือสร้าง Synthetic Data ที่ปรับแต่ง Font, Background และ Effects (Shadow, Blur, Noise) ได้ละเอียด
*   **Data Sources:** ดึงข้อมูลข้อความจาก Kaggle, AI4Thai (NE-Corpus) และวิดีโอ YouTube

### **ส่วนที่ 2: โมเดลและการเรียนรู้ (NLP & OCR Models)**
*   **Text Detection (การตรวจจับข้อความ):**
    *   **YOLO v11:** โมเดลหลักที่ใช้ (ทั้งรุ่นปกติและ OBB - Oriented Bounding Box) โดยมีการทำ Fine-tuning ด้วยชุดข้อมูลจำลอง
    *   โมเดลอื่นๆ ที่ทดสอบ: PaddleOCR, Pytesseract, EAST Model
*   **Text Recognition (การรู้จำข้อความ):**
    *   **EasyOCR:** โมเดลหลักที่นำมา Fine-tune (โครงสร้าง ResNet + LSTM + CTC)
    *   **Typhoon OCR (SCB 10X):** ทดสอบผ่าน API และ HuggingFace สำหรับภาษาไทย
    *   **Ollama (Vision Models):** สำหรับการประมวลผลภาพด้วยโมเดลภาษาขนาดใหญ่

---

## 3. ผลการทดลองและ Metrics หลัก

### **Metrics ที่ใช้ประเมิน:**
*   **CER (Character Error Rate):** อัตราความผิดพลาดระดับตัวอักษร (ยิ่งต่ำยิ่งดี)
*   **WER (Word Error Rate):** อัตราความผิดพลาดระดับคำ โดยใช้ PyThaiNLP ในการตัดคำไทย
*   **Semantic Similarity:** ความคล้ายคลึงทางความหมาย (0.0 - 1.0)
*   **Accuracy:** วัดความถูกต้อง 100% ของทั้งประโยค

### **ผลการทดสอบที่สำคัญ:**
*   **YOLO v11 Detection:** ให้ค่า Precision สูงถึง 0.99 และ mAP50 ที่ 0.99 บน Custom Dataset
*   **EasyOCR Fine-tuning:**
    *   การทำ Fine-tune 15,000 iterations ช่วยลด CER และ WER ได้อย่างมีนัยสำคัญเมื่อเทียบกับ Base Model
    *   พบว่าการใช้ข้อมูลที่ Merge ระหว่าง Out-source และ Kaggle ให้ผลลัพธ์ที่ครอบคลุมกว่า
*   **Medical DICOM Test:** ทดสอบบนภาพหลาย Modality (CT, DX, MG, MR, PT) พบว่า **PaddleOCR** ให้ประสิทธิภาพในการตรวจจับ Box ในภาพทางการแพทย์ได้ดีกว่าเครื่องมืออื่นในบางกรณี โดยเฉพาะภาพที่มีขนาดใหญ่

---

## 4. ปัญหาที่พบและ Next Steps

### **ปัญหาที่พบ (NLP/OCR):**
*   **Multilingual Prediction:** ปัญหาการเรียกใช้งาน Custom Model ร่วมกับภาษาอื่น (ทำนายได้เฉพาะภาษาไทยเพียงอย่างเดียวในบาง Config)
*   **Config Complexity:** ความยากในการตั้งค่า Configuration สำหรับภาษาไทยในโมเดล EasyOCR
*   **Image Quality:** ภาพทางการแพทย์ที่มีขนาดเล็ก (เช่น 256x256) หรือขนาดใหญ่มาก (2800x2300) ส่งผลต่อประสิทธิภาพโมเดลต่างกัน

### **Next Steps:**
*   **Fine-tuning Optimization:** หาวิธี Fine-tune ร่วมกับ Pre-trained model ภาษาไทยที่มีอยู่แล้วเพื่อผลลัพธ์ที่ดีขึ้น
*   **Thai Config:** พัฒนามาตรฐานการ Config สำหรับโมเดลภาษาไทยให้ใช้งานง่ายและเสถียร
*   **Integration:** แก้ไขปัญหาการ Predict ภาษาไทยควบคู่กับภาษาอื่น (Hybrid Recognition)

---

## 5. ส่วนงานอื่นๆ (Non-OCR/System)
*   **DICOM Processing:** การแปลงไฟล์ DICOM เป็นภาพเพื่อนำมาประมวลผล OCR
*   **Deployment:** การสร้าง API และระบบจัดการผลลัพธ์ในรูปแบบ CSV/JSON
*   **Augmentation:** การใช้เทคนิค Mosaic, Mixup, Hue, Saturation เพื่อเพิ่มความหลากหลายให้ชุดข้อมูลฝึกฝน
