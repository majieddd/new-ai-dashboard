"""E17 exploratory correction of E16 adapter undertraining.

The E16 results were inspected before choosing the adapter LR here; therefore
this is NOT an independent confirmation of a preregistered novelty mechanism.
Final test seeds 13,17,19,23,29 are distinct from E16's 1,7,42,123,999.
"""
import copy
import hashlib
import json
import platform
import random
import subprocess
from pathlib import Path

import numpy as np
import torch

from run_e16 import Base, TaskAdapter, accuracy, fit, BATCH, HERE
from tasks_v2 import RULES, make_stream

SEEDS = (13, 17, 19, 23, 29)
OLD_STEPS = 140
NEW_STEPS = 140
ADAPTER_LR = 0.15
FULL_LR = 0.01


def one(seed, device):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(seed)
    stream = make_stream(seed)
    a, b = [{split: (torch.from_numpy(row[0]).to(device), torch.from_numpy(row[1]).to(device))
             for split, row in stream[rule].items()} for rule in RULES]
    rng_old = np.random.default_rng(seed + 19000)
    rng_new = np.random.default_rng(seed + 19001)
    i_old = [rng_old.integers(len(a["train"][0]), size=BATCH) for _ in range(OLD_STEPS)]
    i_new = [rng_new.integers(len(b["train"][0]), size=BATCH) for _ in range(NEW_STEPS)]
    base = Base().to(device)
    fit(base, *a["train"], i_old, FULL_LR, device)
    before = accuracy(base, *a["test"])
    frozen = {"old_test": before, "new_test": accuracy(base, *b["test"]),
              "new_val": accuracy(base, *b["val"]), "trainable_params": 0}
    full = copy.deepcopy(base)
    full_time = fit(full, *b["train"], i_new, FULL_LR, device)
    fine = {"old_test": accuracy(full, *a["test"]), "new_test": accuracy(full, *b["test"]),
            "new_val": accuracy(full, *b["val"]),
            "trainable_params": sum(p.numel() for p in full.parameters()), "adapt_seconds": full_time}
    adapted = TaskAdapter(copy.deepcopy(base)).to(device)
    with torch.no_grad():
        assert torch.equal(base(b["test"][0]), adapted(b["test"][0]))
    adapt_time = fit(adapted, *b["train"], i_new, ADAPTER_LR, device)
    with torch.no_grad():
        assert torch.equal(base(a["test"][0]), adapted(a["test"][0]))
    adapter = {"old_test": accuracy(adapted, *a["test"]),
               "new_test": accuracy(adapted, *b["test"]),
               "new_val": accuracy(adapted, *b["val"]),
               "trainable_params": sum(p.numel() for p in adapted.parameters() if p.requires_grad),
               "adapt_seconds": adapt_time}
    return {"seed": seed, "old_before_test": before,
            "arms": {"frozen": frozen, "full_finetune": fine, "scheduled_adapter": adapter}}


def run(out=None, device="cuda"):
    torch.set_num_threads(1)
    dev = torch.device(device)
    rows = []
    for seed in SEEDS:
        row = one(seed, dev)
        rows.append(row)
        print(seed, {k: (v["old_test"], v["new_test"]) for k,v in row["arms"].items()}, flush=True)
    status = subprocess.run(["git", "status", "--porcelain"], cwd=HERE, text=True, capture_output=True, check=True).stdout
    code = [HERE / s for s in ("run_e16.py", "run_e17.py", "tasks_v2.py")]
    result = {"experiment": "E17", "scope": "exploratory learning-rate correction; fixed task-cued adapter, not EBM/LLM/self-evolution",
              "prior_test_inspected": "E16 (seeds 1,7,42,123,999)",
              "protocol": {"seeds": list(SEEDS), "old_steps": OLD_STEPS, "new_steps": NEW_STEPS,
                           "batch": BATCH, "full_lr": FULL_LR, "adapter_lr": ADAPTER_LR,
                           "replay": "none", "task_cue": "explicit", "test_selection": "none",
                           "compute": "equal optimizer steps/examples, NOT matched GPU time/FLOPs"},
              "provenance": {"git_base": subprocess.run(["git", "rev-parse", "HEAD"], cwd=HERE,
                             text=True, capture_output=True, check=True).stdout.strip(),
                             "working_tree_dirty": bool(status),
                             "source_sha256": {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in code},
                             "torch": torch.__version__, "numpy": np.__version__, "python": platform.python_version(),
                             "device": device, "device_name": torch.cuda.get_device_name(dev) if dev.type == "cuda" else platform.processor()},
              "runs": rows}
    dest = Path(out) if out else HERE / "results" / "E17" / "summary.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise FileExistsError(f"refusing to overwrite historical result {dest}")
    dest.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {dest}", flush=True)
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--out")
    args = parser.parse_args()
    run(args.out, args.device)
