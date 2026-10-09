# Frozen held-out split, derived deterministically from passages.json only.
# Preregistered BEFORE any held-out run. Balanced: 2 queries per class (4 classes),
# fully disjoint from every dev set (dev queries AND dev pool).
import json, hashlib, collections

OUT = "C:/Users/Majied/AppData/Local/hermes/cache/scratch/e21_icl"
sel = json.load(open(OUT + "/passages.json", encoding="utf-8"))
bywork = {}
for i, (pid, txt) in enumerate(sel):
    bywork.setdefault(pid, []).append(i)
work_ids = sorted(bywork.keys())
CLASSES = work_ids[:4]
class_of = {}
for c in CLASSES:
    for i in bywork[c]:
        class_of[i] = CLASSES.index(c)

# Dev fixture (receipts 7, 8, 9, and the beta3 energy arm) reproduced exactly from source.
dev_queries = [i for i in range(len(sel)) if i in class_of][:16]
dev_pool = [i for i in range(len(sel)) if i % 2 == 0 and i in class_of and i not in set(dev_queries)]
dev_used = set(dev_queries) | set(dev_pool)

# Held-out queries: for each class, the 2 lowest-index passages that appear in NO dev
# set (neither dev queries nor dev pool) -> fully disjoint from every dev measurement.
heldout = []
for c in range(4):
    cand = [i for i in bywork[CLASSES[c]] if i not in dev_used]
    heldout += cand[:2]
heldout = sorted(heldout)
hq = set(heldout)

# Shot pool for the held-out run: every passage that is not a held-out query and not a
# dev query. Dev-pool passages MAY appear as shots (disclosed): they were never evaluated
# as queries, so they carry no query-level leakage.
pool = [i for i in range(len(sel)) if i not in hq and i not in set(dev_queries)]

per_class = collections.Counter(class_of[i] for i in heldout)
pool_per_class = collections.Counter(class_of[i] for i in pool)
majority_pool_class = max(range(4), key=lambda c: pool_per_class[c])

manifest = {
    "protocol": "held-out split, preregistered 2026-10-09 before any run",
    "classes_order": CLASSES,
    "label_to_work": {str(c): CLASSES[c] for c in range(4)},
    "heldout_queries": heldout,
    "heldout_labels": [class_of[i] for i in heldout],
    "heldout_per_class": {str(c): per_class[c] for c in range(4)},
    "dev_queries": dev_queries,
    "dev_queries_labels": [class_of[i] for i in dev_queries],
    "dev_pool": dev_pool,
    "overlap_heldout_dev_queries": len(hq & set(dev_queries)),
    "overlap_heldout_dev_pool": len(hq & set(dev_pool)),
    "shot_pool": pool,
    "shot_pool_per_class": {str(c): pool_per_class[c] for c in range(4)},
    "shot_pool_overlap_dev_queries": len(set(pool) & set(dev_queries)),
    "shot_pool_overlap_dev_pool": len(set(pool) & set(dev_pool)),
    "shots": [1, 2, 4, 8],
    "shot_schedule": "shots_for(n, q): round-robin over classes k = c % 4, taking candidate j = len(out)//4 from the class-k pool; identical to the dev source (test_baseline_remaining.py / test_l1_adaptive_beta3.py)",
    "excerpt": "260 characters of the passage text (the actual receipt7 source behaviour; its '48-token' label misdescribed it)",
    "prompt_format": "Passage: <excerpt> -> <letter>\\n ... then 'Passage: <excerpt> -> ' ; competitor letters a/b/c/d must be single tokens (asserted)",
    "arms": {
        "energy": "beta3 repaired arm, seed 101, 60 Adam steps, trained on the DEV pool (24 passages) — training set identical to the dev protocol; evaluation on the held-out queries only",
        "direct": "same architecture and training, direct (non-energy) update, seed 101",
        "competitor": "Qwen3-0.6B (596M, frozen, in-context shots, CPU, float32) — the best measured same-size competitor on the dev fixture (37.5% max, receipt7)"
    },
    "baselines": {
        "chance": 0.25,
        "majority_pool_constant": "predict the shot-pool-majority class for every held-out query",
        "majority_pool_class": str(majority_pool_class),
        "no_retrieval_energy_head": "trained energy arm with the retrieval feature set to zero",
        "no_retrieval_direct_head": "trained direct arm with the retrieval feature set to zero"
    },
    "acceptance_threshold": {
        "A1_energy_at_8_shots": "energy arm accuracy on the held-out set at 8 shots >= 0.50 (>= 4 of 8)",
        "A2_beats_best_competitor": "energy arm at 8 shots strictly > Qwen3-0.6B at 8 shots on the same held-out queries",
        "A3_beats_no_memory": "energy arm at 8 shots strictly > no-retrieval energy head at 8 shots",
        "A4_per_class_coverage": "at 8 shots, at least 1 correct in EACH of the 4 classes (anti-single-class guard)",
        "rule": "ALL four must hold to claim held-out superiority. Any failure is published as a negative result; the numbers are reported verbatim either way."
    },
    "source_pins": {
        "passages_file_sha256": hashlib.sha256(open(OUT + "/passages.json", "rb").read()).hexdigest(),
        "derive_script_sha256": hashlib.sha256(open(OUT + "/build_heldout_manifest.py", "rb").read()).hexdigest(),
        "run_script_sha256": hashlib.sha256(open(OUT + "/test_heldout.py", "rb").read()).hexdigest(),
        "beta3_source_sha256": hashlib.sha256(open(OUT + "/test_l1_adaptive_beta3.py", "rb").read()).hexdigest(),
        "weights_sha256": "7aaff6661428bed033abba9522bec81938678642cca3181fe752b6ca9e1e540f"
    },
    "original_published_pins_recorded": {
        "receipt7_deployed_sha256": "c198cb7dd5a1cecdd6b71727ee3b989bf9d22d41a553f96e817c2ce4a1c7e171",
        "receipt9_deployed_sha256": "426dd6b9d33350ed02427c6519ddd7982436fafadae36ab878a0f5415f2f7a94",
        "receipt8_deployed_sha256": "4eab187f8d3ab8332c4b89e4055e42577764efc1fb37133a41cfd89a9794fddf",
        "receipt10_deployed_sha256": "3e6831400efae190a0606c54c99e1abe158c225c5ad34c3cb9a7d63881cf4488"
    }
}
print(json.dumps(manifest, indent=1))
json.dump(manifest, open(OUT + "/heldout_manifest.json", "w", encoding="utf-8"), indent=1)
