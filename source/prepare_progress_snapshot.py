"""Create a public, development-only status projection from pinned local receipts.

The input receipts remain in their owning worktrees. This export deliberately
omits local account identifiers, final data and model outputs. It is not a new
EXX summary or a substitute for a protocol, approval or final-test seal.
"""
import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path


def source_record(path):
    path = Path(path)
    data = path.read_bytes()
    return json.loads(data), hashlib.sha256(data).hexdigest()


def prepare(e20_path, e21_path, e22_path, as_of):
    timestamp = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
    offset = timestamp.utcoffset()
    if offset is None or offset.total_seconds() != 0:
        raise ValueError("as_of must be an aware UTC timestamp")
    e20, h20 = source_record(e20_path)
    e21, h21 = source_record(e21_path)
    e22, h22 = source_record(e22_path)
    if (e20["experiment"], e20["status"], e20["run_authorized"]) != ("E20", "BLOCKED", False):
        raise ValueError("E20 readiness no longer matches this blocked snapshot")
    if e20["blocker_count"] != len(e20["blockers"]):
        raise ValueError("E20 blocker count disagrees with the enumerated predicates")
    if (e21["paired_seed_count"], len(e21["raw_seed_records"])) != (5, 5):
        raise ValueError("E21 five-seed CPU fixture is not present")
    if e21["scientific_verdict"] != "NOT-RUN; APPROVALS/CUSTODY/LANGUAGE-INTEGRATION-BLOCKED":
        raise ValueError("E21 language verdict changed")
    if [r["seed"] for r in e21["raw_seed_records"]] != e21["seeds"]:
        raise ValueError("E21 raw seeds and summary seeds disagree")
    diffs = e21["paired_nll_control_minus_energy_k4"]["direct_k4"]
    if len(diffs) != len(e21["seeds"]):
        raise ValueError("E21 paired delta count differs from seed count")
    for row, delta in zip(e21["raw_seed_records"], diffs):
        actual = row["arms"]["direct_k4"]["nll_nats_per_token"] - row["arms"]["energy_k4"]["nll_nats_per_token"]
        if abs(actual - delta) > 1e-12:
            raise ValueError("E21 paired delta disagrees with a raw seed record")
    if (e22["status"], e22["base_examples"], e22["variants"]) != ("PUBLIC_DEVELOPMENT_INSTRUMENT_ONLY", 256, 768):
        raise ValueError("E22 development sweep has changed")
    if len(e22["cells"]) != 16 or sum(c["base_examples"] for c in e22["cells"].values()) != e22["base_examples"]:
        raise ValueError("E22 factor cells and base quota disagree")
    if sum(e22["counterfactual_directions"].values()) != e22["base_examples"]:
        raise ValueError("E22 intervention direction count disagrees")
    return {
        "schema": "new-ai-public-development-progress-v1",
        "as_of_utc": as_of,
        "scientific_verdict": "NO_CONFIRMED_LLM_RESULT",
        "e20": {
            "status": e20["status"],
            "missing_evidence_predicates": e20["blocker_count"],
            "run_authorized": e20["run_authorized"],
            "checker_scope": e20["scope"],
            "source_sha256": h20,
        },
        "e21": {
            "status": "LANGUAGE_CONFIRMATION_NOT_RUN",
            "scope": e21["scope"],
            "compute_match": e21["compute_match"],
            "seeds": e21["seeds"],
            "paired_direct_minus_energy_k4_nll": diffs,
            "mean_fixture_scores": {arm: e21["mean_fixture_scores"][arm] for arm in ("frozen_k0", "energy_k4", "direct_k4")},
            "training_wall_seconds_by_arm": e21["training_wall_seconds_by_arm"],
            "source_sha256": h21,
        },
        "e22": {
            "status": "PUBLIC_DEVELOPMENT_INSTRUMENT_ONLY",
            "model_outcome": None,
            "factor_cells": len(e22["cells"]),
            "base_examples": e22["base_examples"],
            "variants": e22["variants"],
            "distinct_structural_groups": e22["distinct_structural_groups"],
            "counterfactual_directions": e22["counterfactual_directions"],
            "per_cell_groups": {cell: record["distinct_structural_groups"] for cell, record in e22["cells"].items()},
            "output_sha256": e22["output_sha256"],
            "source_sha256": h22,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--e20", required=True, type=Path)
    parser.add_argument("--e21", required=True, type=Path)
    parser.add_argument("--e22", required=True, type=Path)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(prepare(args.e20, args.e21, args.e22, args.as_of), stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(args.out)


if __name__ == "__main__":
    main()
