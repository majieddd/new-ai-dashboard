"""E16: corrected synthetic sequence-rule instrument, NOT an LLM or EBM win.

A no-replay two-task diagnostic: train on copy-first, then on copy-last.
Arms share the same pretrained weights, new-task examples, minibatch order and
optimizer-step budget. The adapter is a scheduled/fixed-capacity control (not a
stress-triggered discovery); it is only applied when the explicit task cue says
copy-last. Test data are never used for tuning. Measured times are reported;
equal optimizer steps do NOT imply equal FLOPs, time or parameter budgets.
"""

import argparse
import copy
import hashlib
import json
import os
import platform
import random
import subprocess
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn
import torch.nn.functional as F

from tasks_v2 import DIM, RULES, make_stream

HERE = Path(__file__).resolve().parent
SEEDS = (1, 7, 42, 123, 999)
OLD_STEPS = 140
NEW_STEPS = 140
BATCH = 64


class Base(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(DIM, 64), nn.ReLU(), nn.Linear(64, 8))

    def forward(self, x):
        return self.net(x)


class TaskAdapter(nn.Module):
    """Frozen host + physically added, zero-initialized task-conditional head."""
    def __init__(self, base):
        super().__init__()
        self.base = base
        for param in self.base.parameters():
            param.requires_grad_(False)
        self.adapter = nn.Linear(DIM, 8, bias=False)
        nn.init.zeros_(self.adapter.weight)

    def forward(self, x):
        return self.base(x) + x[:, -1:].clone() * self.adapter(x)


def accuracy(model, x, y):
    model.eval()
    with torch.no_grad():
        return round(float((model(x).argmax(1) == y).float().mean()), 6)


def sync(device):
    if device.type == "cuda":
        torch.cuda.synchronize(device)


def fit(model, x, y, indexes, lr, device):
    trainable = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(trainable, lr=lr, weight_decay=0.0)
    model.train()
    sync(device)
    start = time.perf_counter()
    for batch in indexes:
        optimizer.zero_grad(set_to_none=True)
        loss = F.cross_entropy(model(x[batch]), y[batch])
        loss.backward()
        optimizer.step()
    sync(device)
    return round(time.perf_counter() - start, 4)


def evaluate(seed, device, old_steps=OLD_STEPS, new_steps=NEW_STEPS):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(seed)
        torch.cuda.reset_peak_memory_stats(device)
    stream = make_stream(seed)
    tensors = {rule: {split: (torch.from_numpy(v[0]).to(device),
                              torch.from_numpy(v[1]).to(device))
                      for split, v in stream[rule].items()}
               for rule in RULES}
    a, b = (tensors[name] for name in RULES)
    # Explicit independent RNGs: same batches/order for both adaptation arms.
    rng_old = np.random.default_rng(seed + 19000)
    rng_new = np.random.default_rng(seed + 19001)
    old_batches = [rng_old.integers(len(a["train"][0]), size=BATCH) for _ in range(old_steps)]
    new_batches = [rng_new.integers(len(b["train"][0]), size=BATCH) for _ in range(new_steps)]
    base = Base().to(device)
    old_seconds = fit(base, *a["train"], old_batches, 0.01, device)
    before = {"old_test": accuracy(base, *a["test"]),
              "old_val": accuracy(base, *a["val"]),
              "new_test": accuracy(base, *b["test"])}
    frozen = {"old_test": before["old_test"], "new_test": before["new_test"],
              "old_val": before["old_val"], "new_val": accuracy(base, *b["val"]),
              "trainable_params": 0, "total_params": sum(p.numel() for p in base.parameters()),
              "adapt_seconds": 0.0}
    fine = copy.deepcopy(base)
    fine_seconds = fit(fine, *b["train"], new_batches, 0.01, device)
    full = {"old_test": accuracy(fine, *a["test"]), "new_test": accuracy(fine, *b["test"]),
            "old_val": accuracy(fine, *a["val"]), "new_val": accuracy(fine, *b["val"]),
            "trainable_params": sum(p.numel() for p in fine.parameters()),
            "total_params": sum(p.numel() for p in fine.parameters()),
            "adapt_seconds": fine_seconds}
    scheduled = TaskAdapter(copy.deepcopy(base)).to(device)
    with torch.no_grad():
        assert torch.equal(base(a["test"][0]), scheduled(a["test"][0]))
        assert torch.equal(base(b["test"][0]), scheduled(b["test"][0]))
    adapter_seconds = fit(scheduled, *b["train"], new_batches, 0.01, device)
    with torch.no_grad():
        assert torch.equal(base(a["test"][0]), scheduled(a["test"][0])), "old path must be bit-identical"
    adapter = {"old_test": accuracy(scheduled, *a["test"]),
               "new_test": accuracy(scheduled, *b["test"]),
               "old_val": accuracy(scheduled, *a["val"]),
               "new_val": accuracy(scheduled, *b["val"]),
               "trainable_params": sum(p.numel() for p in scheduled.parameters() if p.requires_grad),
               "total_params": sum(p.numel() for p in scheduled.parameters()),
               "adapt_seconds": adapter_seconds}
    return {"seed": seed, "before": before,
            "arms": {"frozen": frozen, "full_finetune": full, "scheduled_adapter": adapter},
            "old_train_seconds": old_seconds,
            "peak_allocated_bytes": torch.cuda.max_memory_allocated(device) if device.type == "cuda" else None,
            "split_sizes": {k: len(v[0]) for k, v in a.items()}}


def run(seeds=SEEDS, device="cuda", old_steps=OLD_STEPS,
        new_steps=NEW_STEPS, out=None):
    dev = torch.device(device)
    if dev.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    torch.set_num_threads(1)
    git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=HERE, capture_output=True, text=True, check=True).stdout.strip()
    status = subprocess.run(["git", "status", "--porcelain"], cwd=HERE, capture_output=True, text=True, check=True).stdout
    sources = (HERE / "tasks_v2.py", HERE / "run_e16.py")
    sha = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sources}
    provenance = {"git_base": git, "working_tree_dirty": bool(status), "source_sha256": sha,
                  "torch": torch.__version__, "numpy": np.__version__,
                  "device": str(dev), "device_name": torch.cuda.get_device_name(dev) if dev.type == "cuda" else platform.processor(),
                  "platform": platform.platform(), "python": platform.python_version(),
                  "command": f"python run_e16.py --seeds {','.join(map(str, seeds))} --device {device} --old-steps {old_steps} --new-steps {new_steps}"}
    rows = []
    for seed in seeds:
        rec = evaluate(int(seed), dev, old_steps, new_steps)
        rows.append(rec)
        print(f"seed {seed}: old(before)={rec['before']['old_test']:.3f} "
              f"adapter old/new={rec['arms']['scheduled_adapter']['old_test']:.3f}/"
              f"{rec['arms']['scheduled_adapter']['new_test']:.3f} "
              f"fine old/new={rec['arms']['full_finetune']['old_test']:.3f}/"
              f"{rec['arms']['full_finetune']['new_test']:.3f}", flush=True)
    summary = {"experiment": "E16", "scope": "corrected synthetic instrument / scheduled adapter control, not EBM, LLM, or self-evolution",
               "protocol": {"seeds": list(seeds), "old_steps": old_steps, "new_steps": new_steps,
                            "batch": BATCH, "test_selection": "none", "replay": "none",
                            "rule_cue": "explicit", "train_budget": "matched steps/examples, not matched FLOPs or GPU time"},
               "provenance": provenance, "runs": rows}
    dest = Path(out) if out else HERE / "results" / "E16" / "summary.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise FileExistsError(f"E16 is immutable: refusing to replace {dest}")
    dest.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote {dest} ({len(rows)} seeds)", flush=True)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default=",".join(map(str, SEEDS)))
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--old-steps", type=int, default=OLD_STEPS)
    parser.add_argument("--new-steps", type=int, default=NEW_STEPS)
    parser.add_argument("--out")
    args = parser.parse_args()
    run(tuple(int(x) for x in args.seeds.split(",")), args.device,
        args.old_steps, args.new_steps, args.out)
