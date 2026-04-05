# Last Updated: 2026-04-05

# Reference Mining: References Cited By Each OCR Pipeline Paper

Method:
- Source extraction from ar5iv HTML (`https://ar5iv.labs.arxiv.org/html/<arxiv_id>`), References section.
- Fallback extraction via alternative citation index or mirrored arXiv HTML when ar5iv/PDF fails.
- Target: at least 5 cited references per paper.
- Status: 30 papers extracted, 0 failed. (Recovery sources: ar5iv, arXiv HTML, NASA ADS, Semantic Scholar API)

Note:
- Entries are machine-extracted citation strings (compact form) to support fast literature chaining.
- For formal writing, verify full bib details in the original paper PDF.

---

## 1) Preprocessing

### 2505.20429 PreP-OCR
- Amrhein and Clematide (2018). Supervised OCR error detection and correction using statistical and neural machine translation methods.
- Bassil and Alwani (2012). OCR post-processing error correction algorithm using Google online spelling suggestion.
- Brooks et al. (2023). InstructPix2Pix: Learning to follow image editing instructions.
- Kupyn et al. (2019). DeblurGAN-v2.
- Smith (2007). An overview of the Tesseract OCR engine.

### 2404.05669 NAF-DPM
- Hradis et al. (2015). Convolutional neural networks for direct text deblurring.
- Pratikakis et al. (2017). ICDAR 2017 competition on document image binarization.
- Ho et al. (2020). Denoising diffusion probabilistic models.
- Song and Ermon (2021). Denoising diffusion implicit models.
- Saharia et al. (2022). Palette: Image-to-image diffusion models.

### 2507.19804 ForCenNet
- Das et al. (2019). DewarpNet.
- Feng et al. (2021). DocTr: Document image transformer for geometric unwarping.
- Jiang et al. (2022). Revisiting document image dewarping by grid regularization.
- Ma et al. (2018). DocUNet.
- Ronneberger et al. (2015). U-Net.

### 2511.04161 Seeing Straight
- Smith (2007). Tesseract OCR engine overview.
- Li et al. (2021). TrOCR.
- Liao et al. (2023). docTR.
- Touvron et al. (2024). Llama model technical report.
- Khan et al. (2025). Chitrarth vision-language model.

### 2512.08789 MatteViT
- Shah et al. (2018). Iterative photo shadow removal.
- Wang et al. (2019). Transformer network for shadow removal.
- Lin et al. (2020). BEDSR-Net.
- Qu et al. (2017). DeShadowNet.
- Smith (2007). Tesseract OCR engine overview.

---

## 2) Layout Understanding

### 2410.12628 DocLayout-YOLO
- Antonacopoulos et al. (2009). Dataset for document layout analysis.
- Zhong et al. (2019). PubLayNet.
- Pfitzmann et al. (2022). DocLayNet.
- Cheng et al. (2023). M6Doc.
- Ren et al. (2015). Faster R-CNN.

### 2405.11757 DLAFormer
- Carion et al. (2020). DETR.
- Zhu et al. (2021). Deformable DETR.
- Li et al. (2022). DiT.
- Pfitzmann et al. (2022). DocLayNet.
- Zhang et al. (2022). DINO.

### 2601.07620 PARL
- Bi et al. (2022). PaddlePaddle.
- Carion et al. (2020). DETR.
- Cheng et al. (2023). M6Doc.
- Da et al. (2023). Vision grid transformer for DLA.
- Luo et al. (2022). Doc-GCN.

### 2602.05384 Dolphin-v2
- Blecher et al. (2024). Nougat.
- Cui et al. (2025). PaddleOCR 3.0 technical report.
- Wang et al. (2024). MinerU.
- Bai et al. (2025). Qwen2.5-VL technical report.
- Xu et al. (2020). LayoutLM.

### 2504.04085 DocSAM
- Liu et al. (2023). Review of document analysis and recognition.
- Zhu et al. (2021). Deformable DETR.
- Li et al. (2020). DocBank.
- Zhong et al. (2019). PubLayNet.
- Pfitzmann et al. (2022). DocLayNet.

---

## 3) Text Recognition

### 2504.03621 VISTA-OCR
- Zhou et al. (2017). EAST text detector.
- Vaswani et al. (2017). Attention Is All You Need.
- Baek et al. (2019). Character region awareness for text detection.
- Kim et al. (2022). OCR-free document understanding transformer.
- Lee et al. (2023). Pix2Struct.

### 2408.14998 FastTextSpotter
- Atienza (2021). ViT for efficient scene text recognition.
- Carion et al. (2020). DETR.
- Ch'ng et al. (2020). Total-Text.
- Das et al. (2024). Multilingual pretraining for text spotting.
- Das et al. (2023). Multi-domain noisy scene text spotting.

### 2603.00702 Universal Khmer Text Recognition
- Buoy et al. (2023). Low-resource non-Latin OCR baseline.
- Buoy et al. (2022). Khmer printed character recognition (attention seq2seq).
- Nom et al. (2024). KhmerST benchmark.
- Buoy et al. (2025). Attention drift mitigation for Khmer textline recognition.
- Vaswani et al. (2017). Attention Is All You Need.

### 2508.11499 HTR with Transformer-Based Models
- Vaswani et al. (2017). Attention Is All You Need.
- Li et al. (2021). TrOCR.
- Strobel et al. (2022). Transformer-based HTR for historical docs.
- Sanchez et al. (2019). HTR benchmarks.
- Kuncheva and Whitaker (2003). Diversity measures in classifier ensembles.

### 2505.24600 SARD
- Al-Sheikh et al. (2020). Arabic text recognition dataset review.
- Smith (2007). Tesseract OCR engine overview.
- He et al. (2016). ResNet.
- Dosovitskiy et al. (2021). Vision Transformer.
- Rashad (2024). Arabic-Nougat.

---

## 4) Post-correction

### 2502.01205 No Free Lunches
- Akiba et al. (2019). Optuna.
- Beshirov et al. (2024). Bulgarian post-OCR correction.
- Boros et al. (2024). Post-correction with LLMs.
- Jiang et al. (2024). Mixtral of Experts.
- Mesnard et al. (2024). Gemma.

### 2504.00414 Multimodal LLMs for OCR + Post-Correction + NER
- Buringh and Van Zanden (2009). Manuscripts and printed books in Europe.
- Gupta et al. (2007). OCR binarization and preprocessing for historical docs.
- Reul et al. (2019). OCR4all.
- Shen et al. (2021). LayoutParser.
- Petitpierre et al. (2023). Pipeline for historical census processing.

### 2409.00527 Bulgarian Post-OCR Correction
- Source used: NASA ADS references index (`https://ui.adsabs.harvard.edu/abs/2024arXiv240900527B/references`).
- Joulin et al. (2016). Bag of Tricks for Efficient Text Classification (arXiv:1607.01759).
- Lample and Conneau (2019). Cross-lingual Language Model Pretraining (arXiv:1901.07291).
- Liu et al. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach (arXiv:1907.11692).
- Sanh et al. (2019). DistilBERT, a distilled version of BERT (arXiv:1910.01108).
- Wolf et al. (2019). HuggingFace's Transformers: State-of-the-art NLP (arXiv:1910.03771).

### 2412.15248 RoundTripOCR
- Amrhein and Clematide (2018). Supervised OCR error detection/correction.
- Bojar et al. (2016). WMT findings.
- Devlin et al. (2019). BERT.
- D'hondt et al. (2017). Training corpus generation for OCR post-correction.
- Dwivedi et al. (2020). OCR for classical Indic documents.

### 2411.05945 NeKo
- Ackley et al. (1985). Boltzmann Machines.
- Brown et al. (2020). Language Models are Few-Shot Learners.
- Vaswani et al. (2017). Attention Is All You Need.
- Raffel et al. (2020). T5.
- Wolf et al. (2020). Transformers library paper.

---

## 5) Structured Extraction

### 2602.06402 MeDocVL
- Huang et al. (2022). LayoutLMv3.
- Lee et al. (2022). FormNet.
- Xu et al. (2021). LayoutLMv2.
- Xu et al. (2020). LayoutLM.
- Li et al. (2021). StrucTexT.

### 2602.12203 ExStrucTiny
- Abdin et al. (2025). Phi-4 reasoning technical report.
- Agrawal et al. (2025). GPT-OSS model card.
- Bai et al. (2023). Qwen-VL.
- Biten et al. (2019). Scene text VQA.
- Chia et al. (2022). RelationPrompt.

### 2602.07038 UNIKIE-BENCH
- Abdallah et al. (2024). Survey on form understanding.
- Aiello et al. (2002). Document understanding methods.
- Bai et al. (2025a). Qwen3-VL technical report.
- Bai et al. (2025b). Qwen2.5-VL technical report.
- Bai et al. (2025c). LongBench v2.

### 2603.13398 Qianfan-OCR
- Source used: arXiv HTML (`https://arxiv.org/html/2603.13398`).
- Ainslie et al. (2023). GQA: training generalized multi-query transformer models from multi-head checkpoints (arXiv:2305.13245).
- AllenAI (2024). OlmOCR-bench: a comprehensive OCR evaluation benchmark (Hugging Face dataset).
- Bai et al. (2023). Qwen-VL (arXiv:2308.12966).
- Bai et al. (2025). Qwen2.5-VL technical report (arXiv:2502.13923).
- Blecher et al. (2023). Nougat: neural optical understanding for academic documents (arXiv:2308.13418).

### 2601.05470 ROAP
- Abdallah et al. (2024). Survey of form understanding.
- Devlin et al. (2019). BERT.
- Gu et al. (2022). XYLayoutLM.
- Jaume (2019). FUNSD.
- Hong et al. (2022). BROS.

---

## 6) Validation / Compliance

### 2511.14998 FinCriticalED
**Source**: Semantic Scholar API (recovered 2026-04-05 after multiple fallback attempts)
- Gan et al. (2025). MME-Finance: A Multimodal Finance Benchmark for Expert-level Understanding and Reasoning. ACM MM 2025. DOI: 10.1145/3746027.3758230
- Jin et al. (2025). Multi-Stage Field Extraction of Financial Documents with OCR and Compact Vision-Language Models. arXiv:2510.23066
- Wei et al. (2025). DeepSeek-OCR: Contexts Optical Compression. arXiv:2510.18234
- Cui et al. (2025). PaddleOCR-VL: Boosting Multilingual Document Parsing via a 0.9B Ultra-Compact Vision-Language Model. arXiv:2510.14528
- Niu et al. (2025). MinerU2.5: A Decoupled Vision-Language Model for Efficient High-Resolution Document Parsing. arXiv:2509.22186
- Cui et al. (2025). PaddleOCR 3.0 Technical Report. arXiv:2507.05595
- Peng et al. (2025). MultiFinBen: Benchmarking Large Language Models for Multilingual and Multimodal Financial Application. arXiv:2506.14028
- Luo et al. (2025). FinMME: Benchmark Dataset for Financial Multi-Modal Reasoning Evaluation. arXiv:2505.24714
- Hegde et al. (2025). ChartQA-X: Generating Explanations for Visual Chart Reasoning. arXiv:2504.13275
- Nakhl'e et al. (2025). DOLFIN - Document-Level Financial test set for Machine Translation. arXiv:2502.03053
- Fu et al. (2024). OCRBench v2: An Improved Benchmark for Evaluating Large Multimodal Models on Visual Text Localization and Reasoning. arXiv:2501.00321
- Wei et al. (2024). Slow Perception: Let's Perceive Geometric Figures Step-by-step. arXiv:2412.20631
- Ouyang et al. (2024). OmniDocBench: Benchmarking Diverse PDF Document Parsing with Comprehensive Annotations. arXiv:2412.07626
- Yang et al. (2024). CC-OCR: A Comprehensive and Challenging OCR Benchmark for Evaluating Large Multimodal Models in Literacy. arXiv:2412.02210
- OpenAI (2024). GPT-4o System Card. arXiv:2410.21276
- Yue et al. (2024). MMMU-Pro: A More Robust Multi-discipline Multimodal Understanding Benchmark. arXiv:2409.02813
- Wei et al. (2024). General OCR Theory: Towards OCR-2.0 via a Unified End-to-end Model. arXiv:2409.01704
- Liu et al. (2024). Focus Anywhere for Fine-grained Multi-page Document Understanding. arXiv:2405.14295
- Li et al. (2024). SEED-Bench-2-Plus: Benchmarking Multimodal Large Language Models with Text-Rich Visual Comprehension. arXiv:2404.16790
- Chen et al. (2024). OneChart: Purify the Chart Structural Extraction via One Auxiliary Token. arXiv:2404.09987
- Masry & Hajian (2024). LongFin: A Multimodal Document Understanding Model for Long Financial Domain Documents. arXiv:2401.15050
- Wadhawan et al. (2024). ConTextual: Evaluating Context-Sensitive Text-Rich Visual Reasoning in Large Multimodal Models. arXiv:2401.13311
- Wei et al. (2023). Vary: Scaling up the Vision Vocabulary for Large Vision-Language Models. arXiv:2312.06109
- Yue et al. (2023). MMMU: A Massive Multi-Discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI. arXiv:2311.16502
- Shi et al. (2023). Exploring OCR Capabilities of GPT-4V(ision): A Quantitative and In-depth Evaluation. arXiv:2310.16809
- Liu et al. (2023). OCRBench: on the hidden mystery of OCR in large multimodal models. arXiv:2305.07895
- Patterson et al. (2022). The Carbon Footprint of Machine Learning Training Will Plateau, Then Shrink. arXiv:2204.05149
- Mathew et al. (2020). DocVQA: A Dataset for VQA on Document Images. arXiv:2007.00398
- Mishra et al. (2019). OCR-VQA: Visual Question Answering by Reading Text in Images. ICDAR 2019.
- Lin, C.-Y. (2004). ROUGE: A Package for Automatic Evaluation of Summaries. ACL Workshop.
- Papineni et al. (2002). Bleu: a Method for Automatic Evaluation of Machine Translation. ACL 2002.
- Cohen, J. (1960). A Coefficient of Agreement for Nominal Scales.
- Fleiss, J. (1971). Measuring nominal scale agreement among many raters.
- Levenshtein, V. (1965). Binary codes capable of correcting deletions, insertions, and reversals.

### 2509.19345 SCORE
- Clausner et al. (2013). Significance of reading order in document recognition.
- Everingham et al. (2010). PASCAL VOC challenge.
- Gilani et al. (2017). Table detection with deep learning.
- Ha et al. (1995). Recursive XY-cut.
- Harley et al. (2015). Deep conv nets for document image classification.

### 2601.03926 Doc-PP
- Ali et al. (2025). SustainableQA.
- Bai et al. (2025). Qwen3-VL technical report.
- Chang et al. (2025). Security policy preservation benchmark.
- Chia et al. (2025). M-LongDoc benchmark.
- Lee et al. (2025). CheckEval.

### 2507.23736 DICOM De-Identification
- Institute of Medicine (2009). Beyond the HIPAA Privacy Rule.
- Shojaei et al. (2024). Security and privacy in health information systems.
- Freymann et al. (2012). Image data sharing for biomedical research.
- Aryanto et al. (2016). Image de-identification methods.
- Clark et al. (2013). The Cancer Imaging Archive.

### 2509.14464 Not What the Doctor Ordered
- Abdalla et al. (2020). Word embeddings for clinical-note privacy.
- Abdalla (2022). Rethinking Clinical De-identification.
- Alsentzer et al. (2019). Clinical BERT embeddings.
- Altalla et al. (2025). Evaluating GPT models for clinical de-identification.
- Brown et al. (2020). Language Models are Few-Shot Learners.
