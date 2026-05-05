# Last Updated: 2026-05-05

# References: NECTEC NLP Work → LLM/VLM Extension

## Thai NLP Foundations

- PyThaiNLP `word_tokenize` supports Thai word tokenization with the `newmm` engine. Useful as the deterministic baseline for Thai WER and product-name token analysis. Source: <https://pythainlp.org/docs/2.0/api/tokenize.html>
- KhanomTanLLM is a bilingual Thai-English language model from PyThaiNLP. Useful as a local/open Thai LLM candidate for product-name normalization experiments. Source: <https://github.com/PyThaiNLP/KhanomTanLLM>
- WangChanGLM is a multilingual instruction-following model from PyThaiNLP. Useful background for Thai instruction-following LLM work. Source: <https://github.com/PyThaiNLP/WangChanGLM>

## Semantic Similarity / Embedding Metrics

- SentenceTransformers documentation describes semantic textual similarity by embedding texts and comparing vectors, commonly with cosine similarity. This supports the existing OCR semantic-similarity metric. Source: <https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html>
- Sentence-BERT introduced sentence embeddings that can be compared using cosine similarity for semantic textual similarity tasks. Source: <https://arxiv.org/abs/1908.10084>

## OCR / Document Understanding With LLMs and VLMs

- NeKo studies post-recognition generative correction with task-oriented experts, including post-OCR correction. Source: <https://huggingface.co/papers/2411.05945>
- mPLUG-DocOwl 1.5 focuses on OCR-free document understanding and structure learning for text-rich document images. Source: <https://huggingface.co/papers/2403.12895>
- Ocean-OCR presents a multimodal LLM for general OCR applications across document understanding, scene text recognition, and handwritten text recognition. Source: <https://huggingface.co/papers/2501.15558>
- Typhoon OCR is a Thai-English document parsing VLM designed for real-world Thai and English documents. Source: <https://docs.opentyphoon.ai/en/ocr/> and <https://huggingface.co/typhoon-ai/typhoon-ocr-7b>
- Typhoon OCR paper presents an open VLM for Thai and English document extraction. Source: <https://arxiv.org/abs/2601.14722>

## LLM-as-a-Judge / Evaluation

- Judging the Judges studies alignment and vulnerabilities in LLM-as-a-Judge evaluation, useful as a caution that LLM judging must be validated and not treated as ground truth. Source: <https://huggingface.co/papers/2406.12624>
- MLLM-as-a-Judge evaluates multimodal LLMs as judges for vision-language tasks. Relevant if OCR evaluation includes the image crop, not only reference/hypothesis text. Source: <https://www.sciencestack.ai/paper/2402.04788>

