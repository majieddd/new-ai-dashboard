"""E18 preregistered identifiability audit of input-only novelty triggers.

Synthetic six-symbol classification. This does not train an EBM, grow a model,
or test a language model. See PROTOCOL_E18.md before interpreting scores.
"""
import argparse
import hashlib
import json
import platform
import subprocess
from pathlib import Path

import numpy as np
import torch
from torch import nn

HERE = Path(__file__).resolve().parent
SEEDS = (31, 37, 41, 43, 47)
LENGTH, ALPHABET, DIM = 6, 8, 48
STEPS, BATCH, LR, BLOCK = 160, 128, .05, 32
SCORES = ("input_nll", "logit_free_energy", "predictive_entropy")


def encode(seq):
    x = np.zeros((len(seq), DIM), dtype=np.float32)
    x[np.arange(len(seq))[:, None],
      np.arange(LENGTH)[None, :] * ALPHABET + seq] = 1
    return x


def make_data(seed, n_train=2048, n_val=512, n_test=512):
    """Old first symbol 0..3; nuisance first symbol 4..7; no overlaps."""
    n = n_train + n_val + n_test
    if not 0 < n <= 4 * (ALPHABET ** (LENGTH - 1)):
        raise ValueError("requested old sequence count is out of range")
    rng = np.random.default_rng(seed + 18000)
    space = 4 * ALPHABET ** (LENGTH - 1)
    old_id = rng.choice(space, size=n, replace=False)
    nuisance_id = rng.choice(space, size=n_test, replace=False) + space
    powers = ALPHABET ** np.arange(LENGTH - 1, -1, -1)
    def decode(ids):
        return ((ids[:, None] // powers) % ALPHABET).astype(np.int8)
    all_old, nuisance = decode(old_id), decode(nuisance_id)
    data = {"train": all_old[:n_train],
            "val": all_old[n_train:n_train + n_val],
            "test": all_old[n_train + n_val:],
            "nuisance": nuisance}
    return data


def input_nll(train_seq, seq):
    counts = np.ones((LENGTH, ALPHABET), dtype=np.float64)
    for pos in range(LENGTH):
        counts[pos] += np.bincount(train_seq[:, pos], minlength=ALPHABET)
    logp = np.log(counts / counts.sum(axis=1, keepdims=True))
    return -logp[np.arange(LENGTH)[None, :], seq].sum(axis=1)


def auc(old, shifted):
    """Exact pairwise empirical AUROC; tied scores receive half credit."""
    old, shifted = np.asarray(old), np.asarray(shifted)
    if len(old) == 0 or len(shifted) == 0:
        raise ValueError("both classes must have nonempty scores")
    delta = shifted[:, None] - old[None, :]
    return float((np.count_nonzero(delta > 0) +
                  .5 * np.count_nonzero(delta == 0)) / delta.size)


def blocks(errors, size=BLOCK):
    if len(errors) % size:
        raise ValueError("block test requires a complete last block")
    return np.asarray(errors).reshape(-1, size).sum(axis=1).astype(int)


def alert_report(counts, threshold):
    hits = np.flatnonzero(counts > threshold)
    return {"counts": counts.tolist(), "alert_blocks": int(len(hits)),
            "first_alert_after_labels": int((hits[0] + 1) * BLOCK) if len(hits) else None}


def one(seed, device):
    torch.manual_seed(seed)
    np.random.seed(seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(seed)
    data = make_data(seed)
    train_x = torch.from_numpy(encode(data["train"])).to(device)
    train_y = torch.from_numpy(data["train"][:, -1].astype(np.int64)).to(device)
    model = nn.Linear(DIM, ALPHABET).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    gen = np.random.default_rng(seed + 18100)
    for _ in range(STEPS):
        idx = gen.integers(len(data["train"]), size=BATCH)
        loss = nn.functional.cross_entropy(model(train_x[idx]), train_y[idx])
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    model.eval()
    predictions, logits = {}, {}
    with torch.no_grad():
        for split in ("val", "test", "nuisance"):
            out = model(torch.from_numpy(encode(data[split])).to(device))
            logits[split] = out.cpu().numpy().astype(np.float64)
            predictions[split] = out.argmax(dim=-1).cpu().numpy()
    # Exactly paired old/concept X, scored only once; concept differs in y.
    get_scores = {}
    for split in ("val", "test", "nuisance"):
        out = logits[split]
        z = out - out.max(axis=1, keepdims=True)
        p = np.exp(z) / np.exp(z).sum(axis=1, keepdims=True)
        get_scores[split] = {
            "input_nll": input_nll(data["train"], data[split]),
            "logit_free_energy": -np.logaddexp.reduce(out, axis=1),
            "predictive_entropy": -np.sum(p * np.log(p), axis=1),
        }
    metrics = {}
    raw = {"val": {}, "old": {}, "concept": {}, "nuisance": {}}
    for score in SCORES:
        val = get_scores["val"][score]
        old = get_scores["test"][score]
        concept = old.copy()
        nuisance = get_scores["nuisance"][score]
        threshold = float(np.quantile(val, .95))
        metrics[score] = {"old_vs_concept_auc": auc(old, concept),
                          "old_vs_nuisance_auc": auc(old, nuisance),
                          "threshold_from_old_val": threshold,
                          "old_val_fpr": float(np.mean(val > threshold)),
                          "old_test_fpr": float(np.mean(old > threshold)),
                          "concept_tpr": float(np.mean(concept > threshold)),
                          "nuisance_tpr": float(np.mean(nuisance > threshold))}
        for group, scores in (("val", val), ("old", old),
                              ("concept", concept), ("nuisance", nuisance)):
            raw[group][score] = scores.tolist()
        if metrics[score]["old_vs_concept_auc"] != .5:
            raise AssertionError("paired input-only score changed on label shift")
    errors = {"val": predictions["val"] != data["val"][:, -1],
              "old": predictions["test"] != data["test"][:, -1],
              "concept": predictions["test"] != data["test"][:, 0],
              "nuisance": predictions["nuisance"] != data["nuisance"][:, -1]}
    counts = {k: blocks(v) for k, v in errors.items()}
    error_threshold = int(counts["val"].max())
    feedback = {k: alert_report(v, error_threshold) for k, v in counts.items()}
    for group in errors:
        feedback[group]["accuracy_before_adaptation"] = float(1 - errors[group].mean())
    return {"seed": seed, "metrics": metrics, "feedback": feedback,
            "feedback_threshold_max_old_val_errors_per_block": error_threshold,
            "input_sha256": {k: hashlib.sha256(encode(v).tobytes()).hexdigest()
                             for k, v in data.items()},
            "paired_concept_and_old_input_sha256": hashlib.sha256(encode(data["test"]).tobytes()).hexdigest(),
            "raw_scores": raw}


def run(out=None, device="cpu"):
    torch.set_num_threads(1)
    dev = torch.device(device)
    rows = [one(seed, dev) for seed in SEEDS]
    source = [HERE / p for p in ("run_e18.py", "PROTOCOL_E18.md", "test_e18.py")]
    status = subprocess.run(["git", "status", "--porcelain"], cwd=HERE,
                            capture_output=True, text=True, check=True).stdout
    result = {"experiment": "E18",
              "scope": "input-only trigger identifiability; no EBM training, no growth, no LLM",
              "protocol": {"seeds": list(SEEDS), "train": 2048, "val": 512,
                           "test": 512, "nuisance": 512, "steps": STEPS,
                           "batch": BATCH, "lr": LR, "block": BLOCK,
                           "calibration_quantile": .95, "test_selection": "none"},
              "provenance": {"git_base": subprocess.run(["git", "rev-parse", "HEAD"],
                            cwd=HERE, capture_output=True, text=True, check=True).stdout.strip(),
                            "working_tree_dirty": bool(status),
                            "source_sha256": {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                                              for f in source},
                            "python": platform.python_version(), "numpy": np.__version__,
                            "torch": torch.__version__, "device": device,
                            "device_name": torch.cuda.get_device_name(dev) if dev.type == "cuda"
                            else platform.processor()},
              "runs": rows}
    dest = Path(out) if out else HERE / "results/E18/summary.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise FileExistsError(f"refusing to overwrite E18 result: {dest}")
    dest.write_text(json.dumps(result, indent=2), encoding="utf-8")
    for row in rows:
        print(row["seed"], "AUC paired", row["metrics"]["input_nll"]["old_vs_concept_auc"],
              "nuisance AUC", row["metrics"]["input_nll"]["old_vs_nuisance_auc"],
              "feedback delay", row["feedback"]["concept"]["first_alert_after_labels"])
    print("Wrote", dest)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out")
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()
    run(args.out, args.device)
