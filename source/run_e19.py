"""E19: locked no-cue AG News text-classifier adaptation pilot.

Read PROTOCOL_E19.md. This is a linear classifier, not an LLM or EBM.
"""
import argparse
import copy
import hashlib
import json
import platform
import subprocess
import time
from pathlib import Path

import numpy as np
import torch
from sklearn.feature_extraction.text import HashingVectorizer
from torch import nn
from torch.nn import functional as F

HERE = Path(__file__).resolve().parent
SEEDS = (31, 37, 41, 43, 47)
SOURCE = "https://huggingface.co/datasets/SetFit/ag_news/resolve/ca5ba619eb034211db5f70932b6702efd21e7c73/"
DIGESTS = {
    "train.jsonl": "ea432c816ef5219d8bd1e049d63f5e05ad76b35e5efd15420d48a96f15ddaa94",
    "test.jsonl": "68290dee715edcb5a28ff1f3fc933ea7649fb0f01263af94411cfec255c55284",
}
DIM, BATCH, OLD_STEPS, ADAPT_STEPS, LR, BLOCK = 4096, 64, 120, 100, .02, 32


def normal(text):
    return " ".join(text.lower().split())


def read_corpus(data_dir):
    rows = {}
    for name, digest in DIGESTS.items():
        path = data_dir / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"{name}: SHA-256 does not match pinned corpus")
        with path.open(encoding="utf-8") as stream:
            rows[name] = [json.loads(line) for line in stream]
    if len(rows["train.jsonl"]) != 120000 or len(rows["test.jsonl"]) != 7600:
        raise ValueError("unexpected AG News split sizes")
    train, test = rows["train.jsonl"], rows["test.jsonl"]
    test_text = {normal(row["text"]) for row in test}
    if len(test_text) != len(test):
        raise ValueError("test set contains duplicate normalized texts")
    cleaned, seen = [], set()
    collision = duplicate = 0
    for row in train:
        text = normal(row["text"])
        if text in test_text:
            collision += 1
        elif text in seen:
            duplicate += 1
        else:
            seen.add(text)
            cleaned.append(row)
    assert len(cleaned) + collision + duplicate == len(train)
    return cleaned, test, {"train_test_collision_rows": collision,
                            "train_internal_duplicate_rows": duplicate,
                            "cleaned_train_rows": len(cleaned)}


def pick(train, test, seed):
    by_class = {}
    for label in range(4):
        ids = np.asarray([i for i, row in enumerate(train) if row["label"] == label])
        by_class[label] = np.random.default_rng(seed + label).permutation(ids)
    a_train = np.concatenate([by_class[k][:800] for k in (0, 1)])
    a_val = np.concatenate([by_class[k][800:1000] for k in (0, 1)])
    b_train = np.concatenate([by_class[k][:800] for k in (2, 3)])
    b_val = np.concatenate([by_class[k][800:1000] for k in (2, 3)])
    all_ids = np.concatenate([a_train, a_val, b_train, b_val])
    selected = [train[int(i)] for i in all_ids]
    norms = [normal(row["text"]) for row in selected]
    assert len(set(norms)) == len(norms)
    assert not set(norms) & {normal(row["text"]) for row in test}
    rng = np.random.default_rng(seed + 19019)
    # Balanced B pool, disjoint from remaining adaptation data and validation.
    b_pool = np.concatenate([by_class[2][:256], by_class[3][:256]])
    b_pool = rng.permutation(b_pool)
    return {"a_train": [train[int(i)] for i in a_train],
            "a_val": [train[int(i)] for i in a_val],
            "b_train": [train[int(i)] for i in b_train],
            "b_val": [train[int(i)] for i in b_val],
            "b_pool": [train[int(i)] for i in b_pool],
            "a_test": [r for r in test if r["label"] in (0, 1)],
            "b_test": [r for r in test if r["label"] in (2, 3)]}


def to_tensors(split, vectorizer, device):
    x = vectorizer.transform(row["text"] for row in split).toarray().astype(np.float32)
    y = np.asarray([row["label"] % 2 for row in split], dtype=np.int64)
    return torch.from_numpy(x).to(device), torch.from_numpy(y).to(device)


class Adapter(nn.Module):
    def __init__(self, base, old_centroid, support_centroid):
        super().__init__()
        self.base = base
        for param in base.parameters():
            param.requires_grad_(False)
        self.delta = nn.Linear(DIM, 2, bias=False)
        nn.init.zeros_(self.delta.weight)
        self.register_buffer("old_centroid", F.normalize(old_centroid.mean(0), dim=0))
        self.register_buffer("new_centroid", F.normalize(support_centroid.mean(0), dim=0))

    def route(self, x):
        return (x @ self.new_centroid > x @ self.old_centroid).float().unsqueeze(-1)

    def forward(self, x):
        return self.base(x) + self.route(x) * self.delta(x)


def fit(model, x, y, indices, device):
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.Adam(params, lr=LR)
    model.train()
    if device.type == "cuda":
        torch.cuda.synchronize(device)
    start = time.perf_counter()
    for ids in indices:
        opt.zero_grad(set_to_none=True)
        loss = F.cross_entropy(model(x[ids]), y[ids])
        loss.backward()
        opt.step()
    if device.type == "cuda":
        torch.cuda.synchronize(device)
    return time.perf_counter() - start


def score(model, x, y):
    model.eval()
    with torch.no_grad():
        return float((model(x).argmax(-1) == y).float().mean())


def block_errors(base, x, y, size=BLOCK):
    assert len(x) % size == 0
    base.eval()
    with torch.no_grad():
        errors = (base(x).argmax(-1) != y).reshape(-1, size)
    return errors.sum(-1).cpu().tolist()


def choose_feedback(old_blocks, new_blocks):
    threshold = max(old_blocks)
    hit = next((i + 1 for i, count in enumerate(new_blocks[:3]) if count > threshold), None)
    return hit, threshold


def one(seed, train, test, vectorizer, device):
    torch.manual_seed(seed)
    np.random.seed(seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(seed)
    split = pick(train, test, seed)
    tensors = {k: to_tensors(v, vectorizer, device) for k, v in split.items()}
    a_x, a_y = tensors["a_train"]
    av_x, av_y = tensors["a_val"]
    b_x, b_y = tensors["b_pool"]
    at_x, at_y = tensors["a_test"]
    bt_x, bt_y = tensors["b_test"]
    base = nn.Linear(DIM, 2).to(device)
    batches = np.random.default_rng(seed + 19100).integers(len(a_x), size=(OLD_STEPS, BATCH))
    old_seconds = fit(base, a_x, a_y, batches, device)
    old_before = score(base, at_x, at_y)
    old_blocks = block_errors(base, av_x[:384], av_y[:384])
    new_blocks = block_errors(base, b_x[:96], b_y[:96])
    feedback, threshold = choose_feedback(old_blocks, new_blocks)
    random_block = int(np.random.default_rng(seed + 19101).integers(1, 4))
    density = 1 - (av_x @ F.normalize(a_x.mean(0), dim=0))
    alarm = float(torch.quantile(density, .95))
    b_density = 1 - (b_x[:32] @ F.normalize(a_x.mean(0), dim=0))
    density_report = {"old_val_fpr": float((density > alarm).float().mean()),
                      "new_first_block_alarm_rate": float((b_density > alarm).float().mean())}
    batch_ids = np.random.default_rng(seed + 19102).integers(384, size=(ADAPT_STEPS, BATCH))
    arms = {"frozen": {"old_test": old_before, "new_test": score(base, bt_x, bt_y),
                        "adapt_seconds": 0.0, "trigger_after_labels": None,
                        "total_params": sum(p.numel() for p in base.parameters()), "trainable_params": 0}}
    starts = {"scheduled": 1, "random": random_block, "feedback": feedback}
    for name, block in starts.items():
        if block is None:
            arms[name] = {**arms["frozen"], "trigger_after_labels": None}
            continue
        start = block * BLOCK
        end = start + 384
        assert end <= len(b_x)
        adapted = Adapter(copy.deepcopy(base), a_x, b_x[start - BLOCK:start]).to(device)
        with torch.no_grad():
            assert torch.equal(adapted(at_x[:64]), base(at_x[:64]))
            assert torch.equal(adapted(bt_x[:64]), base(bt_x[:64]))
        seconds = fit(adapted, b_x[start:end], b_y[start:end], batch_ids, device)
        arms[name] = {"old_test": score(adapted, at_x, at_y),
                      "new_test": score(adapted, bt_x, bt_y),
                      "router_old_rate": float(adapted.route(at_x).mean()),
                      "router_new_rate": float(adapted.route(bt_x).mean()),
                      "adapt_seconds": seconds, "trigger_after_labels": start,
                      "total_params": sum(p.numel() for p in adapted.parameters()),
                      "trainable_params": sum(p.numel() for p in adapted.parameters() if p.requires_grad)}
    start = BLOCK
    full = copy.deepcopy(base)
    seconds = fit(full, b_x[start:start+384], b_y[start:start+384], batch_ids, device)
    arms["full_finetune"] = {"old_test": score(full, at_x, at_y),
                             "new_test": score(full, bt_x, bt_y),
                             "adapt_seconds": seconds, "trigger_after_labels": BLOCK,
                             "total_params": sum(p.numel() for p in full.parameters()),
                             "trainable_params": sum(p.numel() for p in full.parameters())}
    for arm in arms.values():
        arm["balanced_test"] = (arm["old_test"] + arm["new_test"]) / 2
        arm["old_drop_points"] = 100 * (old_before - arm["old_test"])
    return {"seed": seed, "old_before_test": old_before,
            "old_val_before": score(base, av_x, av_y),
            "new_val_before": score(base, *tensors["b_val"]),
            "old_train_seconds": old_seconds,
            "feedback_threshold_old_val_errors_per_32": threshold,
            "old_val_block_errors": old_blocks,
            "new_first_3_block_errors": new_blocks,
            "density_probe": density_report,
            "arms": arms}


def run(data_dir, out, device):
    torch.set_num_threads(1)
    dev = torch.device(device)
    if dev.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("requested GPU unavailable")
    dest = Path(out)
    if dest.exists():
        raise FileExistsError(f"immutable outcome exists: {dest}")
    train, test, cleaning = read_corpus(Path(data_dir))
    vectorizer = HashingVectorizer(n_features=DIM, ngram_range=(1, 2),
                                   alternate_sign=False, norm="l2")
    rows = []
    for seed in SEEDS:
        row = one(seed, train, test, vectorizer, dev)
        rows.append(row)
        print(seed, {k: [round(v["old_test"], 4), round(v["new_test"], 4)]
                     for k, v in row["arms"].items()}, flush=True)
    script = (HERE / "run_e19.py", HERE / "PROTOCOL_E19.md", HERE / "test_e19.py")
    git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=HERE,
                         text=True, capture_output=True, check=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=HERE,
                           text=True, capture_output=True, check=True).stdout.strip()
    result = {"experiment": "E19", "scope": "AG News no-cue linear classifier pilot; NOT LLM/EBM",
              "dataset_url": SOURCE, "dataset_sha256": DIGESTS,
              "cleaning": cleaning,
              "protocol": {"seeds": list(SEEDS), "feature_dim": DIM, "base_steps": OLD_STEPS,
                           "adapt_steps": ADAPT_STEPS, "batch": BATCH, "lr": LR,
                           "block": BLOCK, "adapt_examples": 384,
                           "text_split": "official AG News test, no tuning"},
              "provenance": {"git_base": git, "working_tree_dirty": bool(dirty),
                             "source_sha256": {s.name: hashlib.sha256(s.read_bytes()).hexdigest() for s in script},
                             "torch": torch.__version__, "numpy": np.__version__,
                             "python": platform.python_version(), "device": device,
                             "device_name": torch.cuda.get_device_name(dev) if dev.type == "cuda" else platform.processor()},
              "runs": rows}
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--out", default=str(HERE / "results/E19/summary.json"))
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()
    run(args.data_dir, args.out, args.device)
