"""
poc_runner.py — 3-Layer OCR Evaluation Stack (POC)

Replaces the current Module 2 evaluation (WER + cosine similarity) with a
more robust 3-layer stack:
  L1 : CER  (Character Error Rate)          — tokenizer-agnostic
  L2 : ANLS* (Avg. Normalized Lev. Similarity, threshold=0.5)
  L3 : BERTScore with WangchanBERTa         — semantic, Thai-aware

Also computes the OLD baseline metrics for side-by-side comparison:
  - WER with PyThaiNLP newmm tokenizer
  - WER with PyThaiNLP attacut tokenizer  (demonstrates ~40% tokenizer drift)
  - Cosine similarity with SentenceTransformer (paraphrase-multilingual-mpnet)

Usage (single pair):
    uv run python poc_runner.py --reference "ยาแก้ปวดหัว" --hypothesis "ยาแกปวดหว"

Usage (test suite from generate_sample.py):
    uv run python poc_runner.py --test-suite sample_outputs/test_pairs.json

    uv run python poc_runner.py \\
        --test-suite sample_outputs/test_pairs.json \\
        --save-json sample_outputs/eval_results.json
"""
import argparse
import json
import pathlib
import sys
import time
from typing import Any

# ---------------------------------------------------------------------------
# Device resolution
# ---------------------------------------------------------------------------

def resolve_device(requested: str | None) -> str:
    try:
        import torch
    except ImportError:
        print("[WARN] torch not installed — using cpu")
        return "cpu"

    if requested is not None:
        return requested

    if not torch.cuda.is_available():
        print("[device] CUDA not available — using cpu")
        return "cpu"

    idx = torch.cuda.current_device()
    name = torch.cuda.get_device_name(idx)
    props = torch.cuda.get_device_properties(idx)
    vram_gb = props.total_memory / 1024**3
    major, minor = props.major, props.minor
    sm_tag = f"sm_{major}{minor}"

    arch_list = torch.cuda.get_arch_list()
    if sm_tag not in arch_list:
        print(
            f"[WARN] GPU '{name}' is {sm_tag} but installed torch only supports: "
            f"{arch_list}.\n"
            f"       Fix: change pyproject.toml torch index to pytorch-cu128 and re-run uv sync.\n"
            f"       Falling back to cpu."
        )
        return "cpu"

    print(f"[device] GPU: {name}  |  arch: {sm_tag}  |  VRAM: {vram_gb:.1f} GB")
    return "cuda"


# ---------------------------------------------------------------------------
# L0 — OLD BASELINE METRICS (WER newmm, WER attacut, cosine similarity)
# ---------------------------------------------------------------------------

def compute_wer_newmm(reference: str, hypothesis: str) -> float:
    try:
        from jiwer import wer
        from pythainlp.tokenize import word_tokenize
    except ImportError as e:
        print(f"[WARN] Skipping WER newmm — {e}")
        return float("nan")

    ref_tokens = " ".join(word_tokenize(reference, engine="newmm"))
    hyp_tokens = " ".join(word_tokenize(hypothesis, engine="newmm"))
    return wer(ref_tokens, hyp_tokens) * 100


def compute_wer_attacut(reference: str, hypothesis: str) -> float:
    try:
        from jiwer import wer
        from pythainlp.tokenize import word_tokenize
    except ImportError as e:
        print(f"[WARN] Skipping WER attacut — {e}")
        return float("nan")

    try:
        ref_tokens = " ".join(word_tokenize(reference, engine="attacut"))
        hyp_tokens = " ".join(word_tokenize(hypothesis, engine="attacut"))
        return wer(ref_tokens, hyp_tokens) * 100
    except Exception as e:
        print(f"[WARN] attacut tokenizer unavailable ({e}) — trying 'longest'")
        try:
            ref_tokens = " ".join(word_tokenize(reference, engine="longest"))
            hyp_tokens = " ".join(word_tokenize(hypothesis, engine="longest"))
            return wer(ref_tokens, hyp_tokens) * 100
        except Exception as e2:
            print(f"[WARN] Fallback tokenizer also failed ({e2})")
            return float("nan")


def load_sentence_transformer(device: str):
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("[WARN] sentence-transformers not installed — skipping cosine sim")
        return None
    print("[L0] Loading SentenceTransformer (paraphrase-multilingual-mpnet-base-v2)…")
    model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2", device=device)
    return model


def compute_cosine_sim(model, reference: str, hypothesis: str) -> float:
    if model is None:
        return float("nan")
    import torch
    embs = model.encode([reference, hypothesis], convert_to_tensor=True)
    cos = torch.nn.functional.cosine_similarity(embs[0].unsqueeze(0), embs[1].unsqueeze(0))
    return float(cos.item())


# ---------------------------------------------------------------------------
# L1 — CER (Character Error Rate)
# ---------------------------------------------------------------------------

def compute_cer(reference: str, hypothesis: str) -> float:
    try:
        from jiwer import cer
    except ImportError:
        print("[ERROR] jiwer not installed. Run: uv add jiwer", file=sys.stderr)
        sys.exit(1)

    # jiwer.cer works at character level — pass raw strings (no tokenization)
    return cer(reference, hypothesis) * 100


# ---------------------------------------------------------------------------
# L2 — ANLS* (Average Normalized Levenshtein Similarity)
# ---------------------------------------------------------------------------

def compute_anls(reference: str, hypothesis: str, threshold: float = 0.5) -> float:
    try:
        from anls import anls_score
    except ImportError:
        print("[ERROR] anls not installed. Run: uv add anls", file=sys.stderr)
        sys.exit(1)

    # gold_labels must be a list; prediction = hypothesis
    score = anls_score(prediction=hypothesis, gold_labels=[reference], threshold=threshold)
    return float(score)


# ---------------------------------------------------------------------------
# L3 — BERTScore with WangchanBERTa (direct transformers implementation)
#
# We implement BERTScore manually using transformers because bert-score 0.3.x
# is incompatible with transformers v5 (model_max_length overflow bug).
# Algorithm mirrors the original BERTScore paper:
#   P = mean over hyp tokens of max cosine similarity to any ref token
#   R = mean over ref tokens of max cosine similarity to any hyp token
#   F1 = 2 * P * R / (P + R)
# ---------------------------------------------------------------------------

_WANGCHAN_MODEL_ID = "airesearch/wangchanberta-base-att-spm-uncased"
# Layer choice: calibrated on 5 Thai medical OCR pairs.
# Layer 11 (penultimate) outperforms layer 9 on tone-mark and vowel OCR errors
# (the dominant failure mode in Thai medical documents).
# Trade-off: layer 11 gives lower F1 for heavy consonant-cluster drops (pair_04),
# which may be appropriate — heavy corruption really is less semantically similar.
_WANGCHAN_LAYER = 11

_bertscore_tok = None
_bertscore_mdl = None


def load_bertscore_model(device: str):
    global _bertscore_tok, _bertscore_mdl
    if _bertscore_tok is not None:
        return

    try:
        import torch
        from transformers import CamembertModel, CamembertTokenizer
    except ImportError as e:
        print(f"[ERROR] transformers not installed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[L3] Loading WangchanBERTa for BERTScore on {device}…")
    t0 = time.time()
    # Use slow tokenizer (CamembertTokenizer) to avoid SPM/protobuf issues
    _bertscore_tok = CamembertTokenizer.from_pretrained(_WANGCHAN_MODEL_ID, use_fast=False)
    _bertscore_tok.model_max_length = 512  # prevent overflow when model_max_length is huge

    _bertscore_mdl = CamembertModel.from_pretrained(
        _WANGCHAN_MODEL_ID,
        output_hidden_states=True,
    ).to(device)
    _bertscore_mdl.eval()
    elapsed = time.time() - t0
    print(f"[L3] WangchanBERTa loaded in {elapsed:.1f}s")


def _get_token_embeddings(texts: list[str], device: str) -> list:
    """Return layer-9 token embeddings for each text (excluding special tokens)."""
    import torch
    global _bertscore_tok, _bertscore_mdl

    results = []
    for text in texts:
        enc = _bertscore_tok(
            text,
            return_tensors="pt",
            max_length=512,
            truncation=True,
            padding=False,
        )
        enc = {k: v.to(device) for k, v in enc.items()}
        with torch.no_grad():
            out = _bertscore_mdl(**enc, output_hidden_states=True)
        # hidden_states: tuple of (num_layers+1) tensors, shape [1, seq_len, hidden]
        hidden = out.hidden_states[_WANGCHAN_LAYER]  # [1, seq_len, 768]
        # Remove batch dim; exclude [CLS] (idx 0) and [SEP] (last idx)
        emb = hidden[0, 1:-1, :]   # [seq_len-2, 768]
        # L2-normalize each token vector
        emb = emb / (emb.norm(dim=-1, keepdim=True) + 1e-9)
        results.append(emb)
    return results


def compute_bertscore(
    references: list[str],
    hypotheses: list[str],
    device: str,
) -> tuple[list[float], list[float], list[float]]:
    import torch

    print(f"[L3] Computing BERTScore (WangchanBERTa layer {_WANGCHAN_LAYER}) on {device}…")
    t0 = time.time()

    ref_embs = _get_token_embeddings(references, device)
    hyp_embs = _get_token_embeddings(hypotheses, device)

    P_list, R_list, F1_list = [], [], []
    for ref_e, hyp_e in zip(ref_embs, hyp_embs):
        # Cosine similarity matrix [hyp_len, ref_len]
        sim = torch.mm(hyp_e, ref_e.T)  # already L2-normalized

        if sim.numel() == 0:
            P_list.append(0.0)
            R_list.append(0.0)
            F1_list.append(0.0)
            continue

        precision = sim.max(dim=1).values.mean().item()  # hyp → ref
        recall    = sim.max(dim=0).values.mean().item()  # ref → hyp
        denom = precision + recall
        f1 = (2 * precision * recall / denom) if denom > 0 else 0.0

        P_list.append(round(precision, 4))
        R_list.append(round(recall, 4))
        F1_list.append(round(f1, 4))

    elapsed = time.time() - t0
    print(f"[L3] BERTScore done in {elapsed:.1f}s")
    return P_list, R_list, F1_list


# ---------------------------------------------------------------------------
# Evaluation orchestration
# ---------------------------------------------------------------------------

def evaluate_pair(
    pair_id: str,
    reference: str,
    hypothesis: str,
    st_model,
    device: str,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "id": pair_id,
        "reference": reference,
        "hypothesis": hypothesis,
    }

    # OLD baseline
    result["wer_newmm_pct"] = round(compute_wer_newmm(reference, hypothesis), 2)
    result["wer_attacut_pct"] = round(compute_wer_attacut(reference, hypothesis), 2)
    result["cosine_sim"] = round(compute_cosine_sim(st_model, reference, hypothesis), 4)

    # NEW 3-layer stack
    result["cer_pct"] = round(compute_cer(reference, hypothesis), 2)
    result["anls_star"] = round(compute_anls(reference, hypothesis), 4)
    # BERTScore computed in batch — placeholder filled later
    return result


def fill_bertscore_batch(results: list[dict], device: str) -> None:
    refs = [r["reference"] for r in results]
    hyps = [r["hypothesis"] for r in results]
    P_list, R_list, F1_list = compute_bertscore(refs, hyps, device)
    for r, p, rec, f1 in zip(results, P_list, R_list, F1_list):
        r["bs_precision"] = p
        r["bs_recall"] = rec
        r["bs_f1"] = f1


# ---------------------------------------------------------------------------
# Output / display
# ---------------------------------------------------------------------------

def print_pair_table(result: dict) -> None:
    try:
        from tabulate import tabulate
    except ImportError:
        _require("tabulate")

    rows = [
        # Layer, Metric, Value, Note
        ["OLD", "WER (newmm)",          f"{result['wer_newmm_pct']:.1f}%",      "word-level, PyThaiNLP newmm"],
        ["OLD", "WER (attacut/longest)",f"{result['wer_attacut_pct']:.1f}%",    "same model, different tokenizer"],
        ["OLD", "Cosine Similarity",    f"{result['cosine_sim']:.4f}",           "paraphrase-multilingual-mpnet"],
        ["L1",  "CER",                  f"{result['cer_pct']:.1f}%",             "tokenizer-agnostic"],
        ["L2",  "ANLS* (t=0.5)",        f"{result['anls_star']:.4f}",           "0=bad, 1=perfect"],
        ["L3",  "BERTScore P",          f"{result['bs_precision']:.4f}",         "WangchanBERTa"],
        ["L3",  "BERTScore R",          f"{result['bs_recall']:.4f}",            "WangchanBERTa"],
        ["L3",  "BERTScore F1",         f"{result['bs_f1']:.4f}",               "WangchanBERTa"],
    ]
    wer_drift = abs(result["wer_newmm_pct"] - result["wer_attacut_pct"])

    print(f"\n{'='*70}")
    print(f"  Pair: {result['id']}")
    print(f"  REF: {result['reference']}")
    print(f"  HYP: {result['hypothesis']}")
    print(f"{'='*70}")
    print(tabulate(rows, headers=["Layer", "Metric", "Value", "Note"], tablefmt="rounded_outline"))
    print(
        f"\n  [Tokenizer-drift check]  "
        f"WER newmm: {result['wer_newmm_pct']:.1f}%  |  "
        f"WER attacut: {result['wer_attacut_pct']:.1f}%  |  "
        f"CER: {result['cer_pct']:.1f}%  |  "
        f"Absolute drift: {wer_drift:.1f}pp"
    )


def print_aggregate_table(results: list[dict]) -> None:
    import math
    from tabulate import tabulate

    def safe_mean(values):
        vals = [v for v in values if not math.isnan(v)]
        return sum(vals) / len(vals) if vals else float("nan")

    agg = {
        "wer_newmm_pct":  safe_mean([r["wer_newmm_pct"]  for r in results]),
        "wer_attacut_pct":safe_mean([r["wer_attacut_pct"] for r in results]),
        "cosine_sim":     safe_mean([r["cosine_sim"]      for r in results]),
        "cer_pct":        safe_mean([r["cer_pct"]         for r in results]),
        "anls_star":      safe_mean([r["anls_star"]       for r in results]),
        "bs_f1":          safe_mean([r["bs_f1"]           for r in results]),
    }

    rows = [
        ["OLD", "WER (newmm)",             f"{agg['wer_newmm_pct']:.1f}%"],
        ["OLD", "WER (attacut/longest)",  f"{agg['wer_attacut_pct']:.1f}%"],
        ["OLD", "Cosine Similarity", f"{agg['cosine_sim']:.4f}"],
        ["L1",  "CER",               f"{agg['cer_pct']:.1f}%"],
        ["L2",  "ANLS*",             f"{agg['anls_star']:.4f}"],
        ["L3",  "BERTScore F1",      f"{agg['bs_f1']:.4f}"],
    ]

    print(f"\n{'='*70}")
    print(f"  AGGREGATE RESULTS ({len(results)} pairs)")
    print(f"{'='*70}")
    print(tabulate(rows, headers=["Layer", "Metric", "Mean"], tablefmt="rounded_outline"))

    drift = abs(agg["wer_newmm_pct"] - agg["wer_attacut_pct"])
    if not math.isnan(drift):
        print(
            f"\n  [Mean tokenizer drift]  "
            f"WER newmm: {agg['wer_newmm_pct']:.1f}%  |  "
            f"WER attacut/longest: {agg['wer_attacut_pct']:.1f}%  |  "
            f"CER: {agg['cer_pct']:.1f}%  |  "
            f"Absolute drift: {drift:.1f}pp"
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="3-Layer OCR Evaluation Stack (CER / ANLS* / BERTScore)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--reference", type=str, help="Reference (ground-truth) Thai text")
    mode.add_argument(
        "--test-suite",
        type=str,
        metavar="PATH",
        help="Path to JSON file with test pairs (from generate_sample.py)",
    )
    p.add_argument(
        "--hypothesis",
        type=str,
        help="OCR hypothesis text (required when --reference is used)",
    )
    p.add_argument(
        "--device",
        type=str,
        default=None,
        help="Force 'cuda' or 'cpu'. Default = auto-detect.",
    )
    p.add_argument(
        "--save-json",
        type=str,
        metavar="PATH",
        default=None,
        help="Write results to this JSON file.",
    )
    p.add_argument(
        "--anls-threshold",
        type=float,
        default=0.5,
        help="ANLS* threshold (default 0.5).",
    )
    p.add_argument(
        "--skip-old-baseline",
        action="store_true",
        help="Skip WER and cosine-sim baseline (faster; omits old-metric columns).",
    )
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.reference and not args.hypothesis:
        parser.error("--hypothesis is required when --reference is specified.")

    device = resolve_device(args.device)

    # Build list of pairs to evaluate
    if args.reference:
        pairs = [{"id": "single", "reference": args.reference, "hypothesis": args.hypothesis}]
    else:
        suite_path = pathlib.Path(args.test_suite)
        if not suite_path.exists():
            print(f"[ERROR] Test suite file not found: {suite_path}", file=sys.stderr)
            sys.exit(1)
        with open(suite_path, encoding="utf-8") as f:
            pairs = json.load(f)
        print(f"[main] Loaded {len(pairs)} test pairs from {suite_path}")

    # Load shared models
    if args.skip_old_baseline:
        st_model = None
    else:
        st_model = load_sentence_transformer(device)

    load_bertscore_model(device)

    # Per-pair metrics (except BERTScore which runs in batch)
    print("\n[main] Computing L1 (CER) and L2 (ANLS*) for all pairs…")
    results = []
    for pair in pairs:
        r = evaluate_pair(
            pair_id=pair.get("id", "?"),
            reference=pair["reference"],
            hypothesis=pair["hypothesis"],
            st_model=st_model,
            device=device,
        )
        results.append(r)

    # BERTScore in batch (one model load for all pairs)
    fill_bertscore_batch(results, device)

    # Display
    for result in results:
        print_pair_table(result)

    if len(results) > 1:
        print_aggregate_table(results)

    # Optionally save JSON
    if args.save_json:
        out_path = pathlib.Path(args.save_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n[main] Results saved → {out_path}")

    print("\n[main] Done.")


if __name__ == "__main__":
    main()
