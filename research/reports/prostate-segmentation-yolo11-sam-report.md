# Research Report: Prostate Segmentation via YOLO11 & SAM
**Project:** NECTEC Cooperative Education / Master's Thesis Prep
**Lead Researcher:** Tanapat Eiam-arj
**Mentor:** Sarintr Watcharabutsarakham (P'Rin)
**Date:** May 2026 (Consolidated from Jan-Mar 2025 results)

---

## 1. Objective
To develop a high-precision medical imaging pipeline for detecting and segmenting the prostate gland from CT and MRI scans, reducing manual labeling time for radiologists and providing consistent anatomical masks for further clinical analysis.

---

## 2. Technical Methodology

### 2.1 The Two-Stage Pipeline
The system utilizes a **Detection-to-Segmentation** workflow:
1.  **Stage 1 (Detection):** Use **YOLO11 (Large/Medium)** to identify the Bounding Box of the prostate.
2.  **Stage 2 (Segmentation):** Pass the Bounding Box as a prompt to **SAM (Segment Anything Model)** or **MedSAM** to generate the final high-resolution mask.

### 2.2 Model Evolution
- **Initial Phase:** YOLOv8/YOLO11n (Nano) for quick testing.
- **Optimization Phase:** Upgraded to **YOLO11l (Large)** for higher mAP.
- **Segmentation Models:**
    - **SAM (Standard):** Good general performance.
    - **SAM2 (SAM2b.pt):** Tested for improved efficiency.
    - **MedSAM (SAMMed_vit2b.pt):** Specialized medical foundation model for better domain-specific boundary detection.

---

## 3. Dataset & Training

### 3.1 Data Sources
- **Initial Dataset:** ~1,400 images (300 manually labeled by the team).
- **Expansion:** Added ~4,000 files from hospital data.
- **Preprocessing:** 
    - Conversion from PNG masks to YOLO-compatible `.txt` labels (x, y, w, h normalized).
    - Data split: 70% Train, 20% Test, 10% Val.
    - Roboflow used for management and data augmentation.

### 3.2 Training Configuration
- **Model:** YOLO11l.pt
- **Epochs:** 20 to 50 epochs (optimized based on mAP50 and Loss curves).
- **Inference:** Integrated with SAM to produce final `.png` masks and `.json` coordinates.

---

## 4. System Implementation: Prostate API
A specialized web interface was developed to operationalize the model:
- **Frontend:** Vite + React + TypeScript + Konva (for canvas visualization).
- **Backend:** FastAPI (Python).
- **Storage Strategy:** Organized by `/yyyy/mm/dd/<uuid>/` containing:
    - `_original.png`
    - `_sam_mask.png`
    - `_bbox.txt`
    - `_bbox.png`
- **Infrastructure:** Containerized using Docker-Compose with external model mounting to optimize image size.

---

## 5. Key Results & Performance
- **Validation:** Best performance achieved at **40-50 epochs** with YOLO11l.
- **Visual Accuracy:** MedSAM showed superior boundary definition compared to standard SAM in clinical CT slices.
- **Deployment:** Successfully transitioned from a synchronous pipeline to a modular API structure.

---

## 6. Future Directions (Master's Thesis Potential)
1.  **3D Volumetric Segmentation:** Extending the 2D slice-based approach to full 3D CT volume reconstruction.
2.  **Active Learning:** Implementing a feedback loop where radiologists can correct SAM masks to further fine-tune the YOLO detector.
3.  **Cross-Organ Generalization:** Applying the YOLO+SAM pipeline to other organs (e.g., Kidney, Liver) using the same framework.

---
**Related Files:**
- [NECTEC Presentation Text](/files/NECTEC_Presentation_text.txt)
- [Meeting Preparation Guide](/research/topics/chanlekha-advisor-meeting-prep-2026-05-06-th.md)
