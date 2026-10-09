import os, json, time, hashlib, sys
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import torch
torch.set_num_threads(1)
import torch.nn.functional as Fn
import numpy as np

# L1 dev revision 2: energy updates are UNROLLED DIFFERENTIABLY (create_graph=True)
# so the classification loss reaches head/qv/Fc. Historical receipt6 preserved untouched.
OUT = "C:/Users/Majied/AppData/Local/hermes/cache/scratch/e21_icl"
W = "C:/Users/Majied/.kr8/REPOS/new-ai-e21-weights"
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
queries = [i for i in range(len(sel)) if i in class_of][:16]
qset = set(queries)
pool = [i for i in range(len(sel)) if i % 2 == 0 and i in class_of and i not in qset]

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
for i in pool + queries:
    content_key[i] = enc(short_ids(i, 48))[-1]

NS = [1, 2, 4, 8]
TRAIN_N = 4
def shots_for(n, q_idx):
    out = []; c = 0
    while len(out) < n:
        k = c % 4
        cands = [i for i in pool if class_of[i] == k and i != q_idx]
        j = len(out) // 4
        if j < len(cands): out.append(cands[j])
        c += 1
        if c > 400: break
    return out[:n]

def acc(preds):
    return {n: round(sum(1 for q in queries if preds[(q, n)] == class_of[q]) / len(queries), 4) for n in NS}

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

def retrieval_feat(q, n, b1, al, b0):
    sp = shots_for(n, q)
    qk = content_key[q]
    d2 = torch.stack([((content_key[s] - qk) ** 2).sum() for s in sp])
    d2n = d2 / d2.mean()  # measured cause of inert schedule: raw d2 ~1e3 saturates softmax -> grad wrt beta is -0.0
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
                scale = torch.clamp(RAD / torch.clamp(nrm, min=1e-6), max=1.0)  # safe at z=0, no NaN grad
                z = z * scale
            else:
                nrm = float(z.detach().norm())
                if nrm > RAD: z = z.detach() * (RAD / nrm)
        else:
            s, v = parts(head, Fc, qv, h, z)
            z = z + STEP * (v + s * (z + qv) + LAM * z)
    return out_head(torch.cat((h, z + torch.tanh(h @ Fc), r), dim=-1))

def train_arm(kind, seed=101):
    Fc, qv, head, out_head, b1, al, b0 = make_arm(seed)
    head_params = list(head.parameters())
    params = head_params + list(out_head.parameters()) + [Fc, qv, b1, al, b0]
    opt = torch.optim.Adam(params, lr=0.02)
    T = torch.tensor([class_of[i] for i in pool])
    names = [f"head{i}" for i in range(len(head_params))] + ["Fc", "qv", "b1", "al", "b0"]
    before = {name: p.detach().clone() for name, p in zip(names, [Fc, qv] + head_params + [b1, al, b0])}
    grad_gate = []
    for step in range(60):
        idx = list(np.random.RandomState(step).choice(len(pool), 8, replace=False))
        loss = 0.0
        for j in idx:
            i = pool[j]
            h = content_key[i]
            r = retrieval_feat(i, TRAIN_N, b1, al, b0)
            logits = run_arm(Fc, qv, head, out_head, h, r, kind, train=True)
            loss = loss + Fn.cross_entropy(logits.unsqueeze(0), T[j:j+1])
        opt.zero_grad(); (loss / len(idx)).backward()
        if step == 0:  # regression gate: finite nonzero energy-head gradients
            for name, p in zip(["Fc", "qv"] + [f"head{i}" for i in range(len(head_params))], [Fc, qv] + head_params):
                g = p.grad
                gn = float(g.norm()) if g is not None else float("nan")
                grad_gate.append({"param": name, "grad_norm": gn,
                                  "finite": bool(g is not None and torch.isfinite(g).all() and gn > 0)})
        opt.step()
    deltas = {}
    for name, p in zip(names, [Fc, qv] + head_params + [b1, al, b0]):
        deltas[name] = round(float((p.detach() - before[name]).norm()), 6)
    preds = {}
    for q in queries:
        for n in NS:
            r = retrieval_feat(q, n, b1.detach(), al.detach(), b0.detach())
            logits = run_arm(Fc, qv, head, out_head, content_key[q], r, kind, train=False)
            preds[(q, n)] = int(logits.argmax())
    sched = {"b1": round(float(b1.detach()), 4), "alpha": round(float(al.detach()), 4),
             "b0": round(float(b0.detach()), 4),
             "beta_at_shots": {str(n): round(float(b1.detach() * (n ** al.detach()) + b0.detach()), 4) for n in NS}}
    return preds, sched, grad_gate, deltas

t0 = time.perf_counter()
counts_e = dict(counters); counters["head_evals"] = 0; counters["grad_calls"] = 0
energy_beta, sched_e, gate_e, delta_e = train_arm("energy")
wall_e = round(time.perf_counter() - t0, 1)
counts_e = {k: counters[k] - counts_e[k] for k in counters}

t1 = time.perf_counter()
base_e = dict(counters)
direct_beta, sched_d, gate_d, delta_d = train_arm("direct")
wall_d = round(time.perf_counter() - t1, 1)
counts_d = {k: counters[k] - base_e[k] for k in counters}

res = {"energy_adaptive_beta": acc(energy_beta), "direct_adaptive_beta": acc(direct_beta)}
mono = lambda a: all(a[NS[i]] >= a[NS[i-1]] - 1e-9 for i in range(1, len(NS)))
gate_ok = all(g["finite"] for g in gate_e) and all(g["finite"] for g in gate_d)
upd_ok = all(v > 0 for v in delta_e.values())
verdict = {
    "energy_head_gradients_finite_nonzero": bool(gate_ok),
    "energy_head_parameters_actually_updated": bool(upd_ok),
    "energy_monotone_in_shots": bool(mono(res["energy_adaptive_beta"])),
    "energy_ge_direct_at_matched_steps": bool(res["energy_adaptive_beta"][8] >= res["direct_adaptive_beta"][8]),
    "energy_beats_no_retrieval_baseline_0p5625": bool(res["energy_adaptive_beta"][8] > 0.5625),
    "acceptance": bool(gate_ok and upd_ok and res["energy_adaptive_beta"][8] > 0.5625),
}
receipt = {
    "results": res, "verdict": verdict,
    "baselines_no_retrieval": {"energy_head": 0.5625, "direct_head": 0.625},
    "compute_accounting": {
        "energy_arm": {"head_evals": counts_e["head_evals"], "grad_calls": counts_e["grad_calls"], "wall_s": wall_e},
        "direct_arm": {"head_evals": counts_d["head_evals"], "grad_calls": counts_d["grad_calls"], "wall_s": wall_d},
        "note": "energy arm pays K extra second-order gradient calls per forward (unrolled energy); matched Adam steps is NOT matched compute"},
    "grad_gate_step0": {"energy": gate_e, "direct": gate_d},
    "param_deltas_after_training": {"energy": delta_e, "direct": delta_d},
    "queries": len(queries), "classes": CLASSES, "shots": NS, "train_n": TRAIN_N,
    "energy_schedule": sched_e, "direct_schedule": sched_d,
    "historical_receipt6_preserved": True,
    "weights_sha256_16": hashlib.sha256(open(W + "/model.safetensors", "rb").read()).hexdigest()[:16],
    "passages_manifest_sha256": hashlib.sha256(json.dumps(sel).encode()).hexdigest(),
    "cpu": {"model_device": str(model.device), "param_device": str(next(model.parameters()).device)}}
json.dump(receipt, open(OUT + "/receipt8_energy_unrolled.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(receipt, indent=1), flush=True)
