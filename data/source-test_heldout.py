# Held-out run, executed ONLY after the frozen manifest is committed.
# Protocol is read from heldout_manifest.json; nothing here chooses the split.
import os, json, time, hashlib
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import torch
torch.set_num_threads(1)
import torch.nn.functional as Fn
import numpy as np

OUT = "C:/Users/Majied/AppData/Local/hermes/cache/scratch/e21_icl"
W = "C:/Users/Majied/.kr8/REPOS/new-ai-e21-weights"
HUB = "C:/Users/Majied/jev-alt-bench/hf_cache/hub"
MAN = json.load(open(OUT + "/heldout_manifest.json", encoding="utf-8"))
sel = json.load(open(OUT + "/passages.json", encoding="utf-8"))

bywork = {}
for i, (pid, txt) in enumerate(sel):
    bywork.setdefault(pid, []).append(i)
work_ids = sorted(bywork.keys())
CLASSES = MAN["classes_order"]
assert CLASSES == work_ids[:4]
class_of = {}
for c in CLASSES:
    for i in bywork[c]:
        class_of[i] = CLASSES.index(c)

HELDOUT = MAN["heldout_queries"]
POOL = MAN["shot_pool"]
DEV_POOL = MAN["dev_pool"]
NS = MAN["shots"]
assert MAN["passages_file_sha256"] == hashlib.sha256(open(OUT + "/passages.json", "rb").read()).hexdigest()

def shots_for(n, q_idx):
    out = []; c = 0
    while len(out) < n:
        k = c % 4
        cands = [i for i in POOL if class_of[i] == k and i != q_idx]
        j = len(out) // 4
        if j < len(cands): out.append(cands[j])
        c += 1
        if c > 400: break
    return out[:n]

def excerpt(i):
    return sel[i][1][:260]

from transformers import AutoModelForCausalLM, AutoTokenizer
tok = AutoTokenizer.from_pretrained(W)
model = AutoModelForCausalLM.from_pretrained(W, dtype=torch.float32)
model.eval()
hs = int(model.config.hidden_size)

def short_ids(i, mt):
    return tok(sel[i][1], add_special_tokens=False, max_length=mt, truncation=True)["input_ids"]

def enc(ids):
    key = hashlib.sha256(("P:" + ",".join(map(str, ids))).encode()).hexdigest()[:16]
    hp = OUT + "/encP_" + key + ".pt"
    if os.path.exists(hp):
        return torch.load(hp, map_location="cpu", weights_only=True)
    with torch.no_grad():
        out = model(torch.tensor([ids]), output_hidden_states=True)
    h = out.hidden_states[-1][0].to(torch.float32)
    torch.save(h, hp)
    return h

content_key = {}
for i in POOL + HELDOUT + DEV_POOL:
    content_key[i] = enc(short_ids(i, 48))

TRAIN_N = 4
LAT, HID, K, STEP, LAM, RAD = 4, 16, 4, 0.1, 0.1, 2.0
counters = {"head_evals": 0, "grad_calls": 0}

def make_arm(seed):
    torch.manual_seed(seed)
    g = torch.Generator().manual_seed(seed)
    Fc = torch.randn(hs, LAT, generator=g) * 0.02
    qv = torch.randn(LAT, generator=g) * 0.1
    Fc.requires_grad_(True)
    qv.requires_grad_(True)
    head = torch.nn.Sequential(torch.nn.Linear(hs + LAT, HID), torch.nn.SiLU(),
                               torch.nn.Linear(HID, LAT + 1))
    out_head = torch.nn.Linear(hs + LAT + hs, 4)
    b1 = torch.tensor(1.0, requires_grad=True)
    al = torch.tensor(1.0, requires_grad=True)
    b0 = torch.tensor(0.5, requires_grad=True)
    return Fc, qv, head, out_head, b1, al, b0

def parts(head, Fc, qv, h, z):
    counters["head_evals"] += 1
    ff = torch.tanh(h @ Fc)
    o = head(torch.cat((h, z + ff), dim=-1))
    return o[..., 0], o[..., 1:]

def retrieval_feat(q, n, b1, al, b0, pool_idx):
    sp = shots_for(n, q) if pool_idx is None else [i for i in shots_for(n, q) if i in pool_idx]
    qk = content_key[q]
    d2 = torch.stack([((content_key[s] - qk) ** 2).sum() for s in sp])
    d2n = d2 / d2.mean()
    beta = b1 * (n ** al) + b0
    w = torch.softmax(-beta * (d2n - d2n.min()), dim=0)
    p = (w.unsqueeze(1) * torch.stack([content_key[s] for s in sp])).sum(0)
    return p

def run_arm(Fc, qv, head, out_head, h, r, kind, train=True):
    z = torch.zeros(LAT)
    for _ in range(K):
        if kind == "energy":
            zz = z if z.requires_grad else z.clone().requires_grad_(True)
            s, v = parts(head, Fc, qv, h, zz)
            E = s * (1.0 + (zz * qv).sum() + 0.5 * zz.square().sum()) + (zz * v).sum() + 0.5 * LAM * zz.square().sum()
            grad = torch.autograd.grad(E, zz, create_graph=train)[0]
            counters["grad_calls"] += 1
            z = z - STEP * grad
            if train:
                nrm = z.norm()
                scale = torch.clamp(RAD / torch.clamp(nrm, min=1e-6), max=1.0)
                z = z * scale
            else:
                nrm = float(z.detach().norm())
                if nrm > RAD: z = z.detach() * (RAD / nrm)
        else:
            s, v = parts(head, Fc, qv, h, z)
            z = z + STEP * (v + s * (z + qv) + LAM * z)
    return out_head(torch.cat((h, z + torch.tanh(h @ Fc), r), dim=-1))

def train_arm(kind, seed=101):
    # TRAINING SET = the dev pool, exactly as in the dev protocol (test_l1_adaptive_beta3.py).
    Fc, qv, head, out_head, b1, al, b0 = make_arm(seed)
    head_params = list(head.parameters())
    params = head_params + list(out_head.parameters()) + [Fc, qv, b1, al, b0]
    opt = torch.optim.Adam(params, lr=0.02)
    T = torch.tensor([class_of[i] for i in DEV_POOL])
    for step in range(60):
        idx = list(np.random.RandomState(step).choice(len(DEV_POOL), 8, replace=False))
        loss = 0.0
        for j in idx:
            i = DEV_POOL[j]
            h = content_key[i]
            r = retrieval_feat_dev(i, TRAIN_N, b1, al, b0)
            logits = run_arm(Fc, qv, head, out_head, h, r, kind, train=True)
            loss = loss + Fn.cross_entropy(logits.unsqueeze(0), T[j:j+1])
        opt.zero_grad(); (loss / len(idx)).backward()
        opt.step()
    return Fc, qv, head, out_head, b1, al, b0

def retrieval_feat_dev(q, n, b1, al, b0):
    sp = []
    c = 0
    while len(sp) < n:
        k = c % 4
        cands = [i for i in DEV_POOL if class_of[i] == k and i != q]
        j = len(sp) // 4
        if j < len(cands): sp.append(cands[j])
        c += 1
        if c > 400: break
    qk = content_key[q]
    d2 = torch.stack([((content_key[s] - qk) ** 2).sum() for s in sp])
    d2n = d2 / d2.mean()
    beta = b1 * (n ** al) + b0
    w = torch.softmax(-beta * (d2n - d2n.min()), dim=0)
    return (w.unsqueeze(1) * torch.stack([content_key[s] for s in sp])).sum(0)

t0 = time.perf_counter()
counts_e = dict(counters)
Fc, qv, head, out_head, b1, al, b0 = train_arm("energy")
wall_energy_train = round(time.perf_counter() - t0, 1)
counts_e = {k: counters[k] - counts_e[k] for k in counters}

t1 = time.perf_counter()
base = dict(counters)
FcD, qvD, headD, outD, b1D, alD, b0D = train_arm("direct")
wall_direct_train = round(time.perf_counter() - t1, 1)
counts_d = {k: counters[k] - base[k] for k in counters}

def eval_arm(Fc, qv, head, out_head, b1, al, b0, kind, use_retrieval):
    preds = {}
    for q in HELDOUT:
        for n in NS:
            r = retrieval_feat(q, n, b1.detach(), al.detach(), b0.detach(), POOL) if use_retrieval else torch.zeros(LAT)
            logits = run_arm(Fc, qv, head, out_head, content_key[q], r, kind, train=False)
            preds[(q, n)] = int(logits.argmax())
    return preds

def acc(preds):
    return {str(n): round(sum(1 for q in HELDOUT if preds[(q, n)] == class_of[q]) / len(HELDOUT), 4) for n in NS}

def per_class(preds, n):
    out = {}
    for c in range(4):
        qs = [q for q in HELDOUT if class_of[q] == c]
        out[str(c)] = sum(1 for q in qs if preds[(q, n)] == class_of[q])
    return out

energy_preds = eval_arm(Fc, qv, head, out_head, b1, al, b0, "energy", True)
direct_preds = eval_arm(FcD, qvD, headD, outD, b1D, alD, b0D, "direct", True)
energy_noretr_preds = eval_arm(Fc, qv, head, out_head, b1, al, b0, "energy", False)
direct_noretr_preds = eval_arm(FcD, qvD, headD, outD, b1D, alD, b0D, "direct", False)

# Competitor: Qwen3-0.6B, frozen, in-context shots, same format/excerpts, CPU float32.
QWEN = HUB + "/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca"
LETTERS = ["a", "b", "c", "d"]
qtok = AutoTokenizer.from_pretrained(QWEN)
assert all(len(qtok.encode(L, add_special_tokens=False)) == 1 for L in LETTERS)
qmodel = AutoModelForCausalLM.from_pretrained(QWEN, torch_dtype=torch.float32)
qmodel.eval()
letter_ids = [qtok.encode(L, add_special_tokens=False)[0] for L in LETTERS]
q_preds = {}
q_tok_counts = {}
for n in NS:
    toks = 0
    for q in HELDOUT:
        parts = []
        for s in shots_for(n, q):
            parts.append("Passage: " + excerpt(s) + " -> " + LETTERS[class_of[s]] + "\n")
        parts.append("Passage: " + excerpt(q) + " -> ")
        ids = qtok("".join(parts), add_special_tokens=True)["input_ids"]
        toks += len(ids)
        with torch.no_grad():
            logits = qmodel(input_ids=torch.tensor([ids])).logits[0, -1]
        q_preds[(q, n)] = int(max(range(4), key=lambda k: float(logits[letter_ids[k]])))
    q_tok_counts[str(n)] = round(toks / len(HELDOUT), 1)
del qmodel

majority_class = int(MAN["baselines"]["majority_pool_class"])
majority_acc = {str(n): round(sum(1 for q in HELDOUT if majority_class == class_of[q]) / len(HELDOUT), 4) for n in NS}

res = {
    "energy_retrieval": acc(energy_preds),
    "direct_retrieval": acc(direct_preds),
    "energy_no_retrieval": acc(energy_noretr_preds),
    "direct_no_retrieval": acc(direct_noretr_preds),
    "qwen3_0.6b": acc(q_preds),
    "majority_constant": majority_acc,
    "chance": 0.25,
}
percls = {arm: {str(n): per_class(p, n) for n in NS}
          for arm, p in [("energy", energy_preds), ("direct", direct_preds),
                         ("qwen3", q_preds), ("energy_noretr", energy_noretr_preds)]}

A1 = res["energy_retrieval"]["8"] >= 0.50
A2 = res["energy_retrieval"]["8"] > res["qwen3_0.6b"]["8"]
A3 = res["energy_retrieval"]["8"] > res["energy_no_retrieval"]["8"]
A4 = all(percls["energy"]["8"][str(c)] >= 1 for c in range(4))
verdict = {
    "A1_energy_at_8_shots_ge_0p50": bool(A1),
    "A2_beats_best_competitor_qwen3_at_8": bool(A2),
    "A3_beats_no_memory_energy_head_at_8": bool(A3),
    "A4_per_class_coverage_at_8": bool(A4),
    "acceptance_held_out_superiority": bool(A1 and A2 and A3 and A4),
}

receipt = {
    "results": res,
    "per_class_correct_at_shots": percls,
    "per_query_predictions": {
        arm: {str(n): {str(q): {"pred": p[(q, n)], "label": class_of[q], "work": CLASSES[class_of[q]]}
                       for q in HELDOUT} for n in NS}
        for arm, p in [("energy", energy_preds), ("direct", direct_preds),
                       ("qwen3", q_preds), ("energy_noretr", energy_noretr_preds)]
    },
    "verdict": verdict,
    "protocol": "held-out split from the frozen preregistered manifest (committed before this run)",
    "heldout_queries": HELDOUT,
    "heldout_labels": [class_of[i] for i in HELDOUT],
    "heldout_per_class": MAN["heldout_per_class"],
    "overlap_checks": {"heldout_vs_dev_queries": MAN["overlap_heldout_dev_queries"],
                       "heldout_vs_dev_pool": MAN["overlap_heldout_dev_pool"],
                       "shot_pool_vs_dev_queries": MAN["shot_pool_overlap_dev_queries"],
                       "shot_pool_vs_dev_pool": MAN["shot_pool_overlap_dev_pool"]},
    "training_set": "dev pool (24 passages), identical to the dev protocol; never evaluated as queries",
    "qwen3_prompt_tokens_per_query": q_tok_counts,
    "compute_accounting": {
        "energy_train": {"head_evals": counts_e["head_evals"], "grad_calls": counts_e["grad_calls"], "wall_s": wall_energy_train},
        "direct_train": {"head_evals": counts_d["head_evals"], "grad_calls": counts_d["grad_calls"], "wall_s": wall_direct_train},
    },
    "cpu": True,
    "device_attestation": "CPU only: CUDA_VISIBLE_DEVICES='', torch.set_num_threads(1), float32 weights, no GPU allocation",
    "source_pins": MAN["source_pins"],
    "manifest_sha256": hashlib.sha256(open(OUT + "/heldout_manifest.json", "rb").read()).hexdigest(),
    "passages_file_sha256": hashlib.sha256(open(OUT + "/passages.json", "rb").read()).hexdigest(),
    "fixture_limitation_disclosure": "The dev fixture (receipts 7, 8, 9, 10) used 16 queries all from ONE class (pg2701); an always-c baseline scores 100% there. Dev numbers do not establish four-class capability. This held-out run is the first balanced 4-class measurement.",
}
json.dump(receipt, open(OUT + "/receipt11_heldout.json", "w", encoding="utf-8"), indent=1)
print(json.dumps({"results": res, "verdict": verdict, "per_class": percls}, indent=1), flush=True)
print("ALL DONE", flush=True)
