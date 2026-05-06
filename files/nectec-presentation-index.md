# Index: NECTEC Presentation Research & Development

## 1. Metadata Header
*   **Title:** NECTEC Internship/Cooperative Education Research Presentation
*   **Date Range:** December 9, 2024 – March 12, 2025 (B.E. 2567-2568)
*   **Authors:**
    *   **Ms. Sarintr Watcharabutsarakham** (Mentor/พี่ริน)
    *   **Mr. Tanapat Eiam-arj** (Pluem/ปลื้ม)
    *   **Mr. Phatcharaphon Laorujiralai** (Hall/ฮอลล์)
*   **Affiliation:** NECTEC (National Electronics and Computer Technology Center)

---

## 2. Table of Contents
1.  [OCR & SME Data Processing](#ocr--sme-data-processing)
2.  [Object Detection & YOLO Models](#object-detection--yolo-models)
3.  [Segmentation Models (SAM & MedSAM)](#segmentation-models)
4.  [Medical Image Classification](#medical-image-classification)
5.  [Estimate Blood Loss (EBL) Project](#estimate-blood-loss-ebl-project)
6.  [Advanced Research (CLIP, LSTM, SAM2)](#advanced-research)
7.  [API & Infrastructure (Worker Queue, Docker)](#api--infrastructure)

---

## 3. Per-Meeting Index

### Meeting 1 (December 9, 2024)
*   **Attendees:** Sarintr, Tanapat, Phatcharaphon
*   **Key Topics:**
    *   Image classification for text-heavy vs. product images.
    *   Medical document OCR.
    *   SME Product Name cleaning.
    *   Introduction to YOLOv8 and Roboflow.
*   **Models/Tools:** Tesseract OCR, PyThaiNLP, Roboflow, YOLOv8.
*   **Outcomes:** Established threshold (700 characters) for filtering text-heavy images; initial data cleaning pipeline for SME names.

### Meeting 2 (December 24, 2024)
*   **Attendees:** Sarintr, Tanapat, Phatcharaphon
*   **Key Topics:**
    *   SME Data sampling and column merging.
    *   Bounding Box generation using Tesseract.
    *   SAM (Segment Anything Model) exploration.
    *   YOLO Classification for organs (Brain/Eyes).
*   **Models/Tools:** Tesseract, SAM, YOLOv8 Classification.
*   **Outcomes:** Automated Bbox generation with confidence thresholds; initial organ classification (Axial/Frontal Brain, Eyes).

### Meeting 3 (January 8, 2025)
*   **Attendees:** Sarintr, Tanapat, Phatcharaphon
*   **Key Topics:**
    *   Prostate mask Bounding Box detection.
    *   Estimate Blood Loss (EBL) UI/API development.
    *   EBL Dataset sorting (Gauze vs. Swab, Folded vs. Unfolded).
*   **Models/Tools:** YOLOv11, SAM, FastAPI, Figma, Vue3, Tailwind CSS.
*   **Outcomes:** Figma prototype for EBL; EBL API (IPU template) developed with FastAPI.

### Meeting 4 (January 27, 2025)
*   **Attendees:** Sarintr, Tanapat, Phatcharaphon
*   **Key Topics:**
    *   Prostate Mask Bbox expansion (+4,000 files).
    *   Zero-shot classification for Diabetic Retinopathy (DR) using CLIP.
    *   Human Action Recognition research.
    *   Classification API for organs.
*   **Models/Tools:** YOLOv11l, SAM2, MedSAM, CLIP (ViT-L/14, ViT-B/32), LSTM.
*   **Outcomes:** Improved Prostate detection; CLIP similarities report for DR levels; LSTM model for action recognition (7 classes).

### Meeting 5 (February 11, 2025)
*   **Attendees:** Sarintr, Tanapat, Phatcharaphon
*   **Key Topics:**
    *   EBL Frontend implementation (React + TypeScript).
    *   Labeling Diabetic Retinopathy (DR) features.
    *   Action Recognition training using YOLO.
    *   Organ classification augmentation.
*   **Models/Tools:** React, Vite, YOLO, Augmentation techniques.
*   **Outcomes:** Functional 2-page EBL web app; labeled dataset for Big dots, Small dots, and Sparkling features in DR.

### Meeting 6 (February 26, 2025)
*   **Attendees:** Sarintr, Tanapat, Phatcharaphon, Ta, On
*   **Key Topics:**
    *   EBL Worker Queue architecture design.
    *   Gauze dataset refinement (Under/Over segmentation).
    *   Prostate API static file serving.
    *   Docker-Compose optimization (Model mounting).
*   **Models/Tools:** RabbitMQ, Docker-Compose, Worker Queue pattern.
*   **Outcomes:** Transition from RPC to Worker Queue for long-running AI tasks; reduced Docker image size via external model mounting.

### Meeting 7 (March 12, 2025)
*   **Attendees:** Sarintr, Tanapat, Phatcharaphon
*   **Key Topics:**
    *   Redesign of EBL UI for batch processing.
    *   Detailed Worker Queue API flow (Main Entry -> Mask -> Sponge Classify -> EBL Estimate).
    *   Knowledge Sharing: Docker & API development.
*   **Models/Tools:** Mask2Former, ResNet18, XGBoost, RabbitMQ.
*   **Outcomes:** Pipeline modularization (Mask2Former for segment, ResNet18 for classification, XGBoost for estimation).

---

## 4. Master Glossary

### Technical Models & Architectures
*   **Tesseract OCR:** Open-source OCR engine used for text extraction and initial Bbox generation.
*   **YOLO (v8, v11):** Real-time object detection models; used for organ classification and prostate detection.
*   **SAM / SAM2 (Segment Anything Model):** Meta's foundation model for image segmentation; used for mask generation.
*   **MedSAM:** A specialized SAM fine-tuned for medical imaging.
*   **CLIP (Contrastive Language-Image Pre-training):** Used for zero-shot Diabetic Retinopathy level classification.
*   **Mask2Former:** Universal segmentation architecture used in the refined EBL pipeline.
*   **XGBoost:** Gradient boosting library used for the final blood loss volume estimation.
*   **LSTM (Long Short-Term Memory):** Recurrent neural network used for Human Action Recognition in videos.
*   **ResNet18:** Convolutional neural network used for classifying sponges (Gauze vs. Swab).

### Tools & Frameworks
*   **FastAPI:** Modern Python web framework used for building all backend services.
*   **RabbitMQ:** Message broker used for the "Worker Queue" architecture to handle asynchronous tasks.
*   **Vite / React / Vue3:** Frontend frameworks used for building the research dashboards and EBL interface.
*   **Roboflow:** Platform for dataset management, labeling, and training YOLO models.
*   **Konva:** 2D canvas library used for interactive image manipulation in the UI.
*   **PyThaiNLP:** Library for Thai natural language processing (tokenization, cleaning).
*   **Docker / Docker-Compose:** Containerization tools for deploying APIs and managing model environments.

### Technical Terms & Datasets
*   **DR (Diabetic Retinopathy):** Medical condition classified into levels (2, 3, 4) with features like Big dots, Small dots, and Sparkling.
*   **EBL (Estimate Blood Loss):** Project aimed at estimating blood volume in surgical sponges (Gauze/Swab).
*   **Axial / Frontal Brain:** Specific anatomical planes for MRI/CT classification.
*   **OCT (Optical Coherence Tomography):** Eye imaging used in the classification dataset.
*   **Worker Queue:** Design pattern using RabbitMQ to manage long-running AI processing tasks independently from the main API.
*   **RPC (Remote Procedure Call):** Initial synchronous communication pattern replaced by the Worker Queue.
*   **Perspective Transform:** Image processing technique used to flatten cropped sponges for better volume estimation.
