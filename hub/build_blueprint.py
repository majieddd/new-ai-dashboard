"""Project the evidence ledger into four static Archify architecture views.

The ledger carries all 14 logical components and 34 typed links. The viewer
shows a bounded main path per view; other links remain discoverable in JSON.
No status on this diagram is derived from running model telemetry.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "blueprint-ledger.json"
POSITIONS = {
    "e19": {"stream": (40, 320), "core": (350, 320), "detector": (660, 80),
            "router": (660, 320), "adapter": (925, 320),
            "evaluator": (925, 570), "telemetry": (660, 820),
            "publishing": (925, 820)},
    "e20": {"stream": (40, 320), "core": (350, 320), "detector": (660, 80),
            "router": (660, 320), "adapter": (970, 320), "replay": (970, 570),
            "evaluator": (1280, 320), "telemetry": (1280, 570),
            "publishing": (1280, 820)},
    "e21": {"stream": (40, 320), "core": (350, 320), "energy": (660, 110),
            "direct": (660, 560), "evaluator": (970, 320),
            "telemetry": (970, 600), "publishing": (1280, 320),
            "promotion": (1280, 100)},
    "future": {"stream": (40, 380), "core": (310, 380), "energy": (310, 80),
               "direct": (40, 680), "detector": (40, 980), "router": (310, 680),
               "adapter": (580, 380), "replay": (580, 680), "tiers": (310, 980),
               "evaluator": (850, 380), "telemetry": (580, 80),
               "publishing": (850, 680), "promotion": (850, 80),
               "freeze_swap": (580, 980)},
}
# Sparse main paths keep the Archify view legible; the source ledger retains
# every edge's direction, full payload, evidence, gate, boundary and failure.
VISIBLE = {
    "e19": ("e01", "e02", "e08", "e09", "e10", "e17", "e23", "e24"),
    "e20": ("e01", "e02", "e04", "e08", "e09", "e10", "e11", "e12", "e17", "e23", "e24"),
    "e21": ("e01", "e14", "e15", "e18", "e19", "e23", "e24", "e25"),
    "future": ("e01", "e02", "e04", "e08", "e09", "e14", "e15", "e23", "e24", "e25", "e27", "e28", "e30", "e31"),
}
TITLES = {
    "e19": "E19 · Historical classifier / timing FAIL",
    "e20": "E20 · Proposed language adaptation / unrun",
    "e21": "E21 · Proposed energy versus direct update / unrun",
    "future": "Future · Unimplemented composition, not a running system",
}
LABELS = {
    "stream": "Allowed stream", "core": "Frozen core", "energy": "Energy refiner",
    "direct": "Direct control", "detector": "Feedback monitor", "router": "Prefix router",
    "adapter": "Growth slots", "replay": "Replay control", "promotion": "Human release gate",
    "freeze_swap": "A/B freeze-swap", "evaluator": "Evaluator", "telemetry": "Cost ledger",
    "publishing": "Public record", "tiers": "Expert tiers",
}

def build():
    model = json.loads(LEDGER.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in model["nodes"]}
    edges = {e["id"]: e for e in model["edges"]}
    assert len(nodes) == 14 and len(edges) == 34
    assert all(not n["running_now"] for n in nodes.values())
    assert not any(e["from"] == x["from"] and e["to"] == x["to"]
                   for e in edges.values() for x in model["forbidden_links"])
    dest = HERE / "diagrams"
    dest.mkdir(exist_ok=True)
    for view in model["views"]:
        name = view["id"]
        ids = view["nodes"]
        assert set(ids) == set(POSITIONS[name]) and 8 <= len(ids) <= 14
        components = []
        for ident in ids:
            n = nodes[ident]
            # E19 is a classifier, so its core/evaluator cannot inherit the LM/seal label.
            sub = n["view_labels"][name]
            components.append({"id":ident,"type":n["type"],"label":LABELS[ident],
                               "sublabel":sub,"tag":model["status_labels"][n["view_status"][name]],
                               "pos":list(POSITIONS[name][ident]),"size":[188,78]})
        connections = []
        for eid in VISIBLE[name]:
            e = edges[eid]
            assert name in e["views"] and e["from"] in ids and e["to"] in ids
            connections.append({"id":eid,"from":e["from"],"to":e["to"],
                                "label":e["type"].replace("_", " "),
                                "variant":"default" if name == "e19" else "dashed"})
        cards = []
        for ident in ids:
            n = nodes[ident]
            cards.append({"dot":"slate", "title":f"{LABELS[ident]} · {name.upper()}",
                          "items":[n["view_labels"][name],
                                   model["status_labels"][n["view_status"][name]],
                                   "Gate: " + model["gates"][n["gate"]]["rule"],
                                   "Boundary: " + model["boundaries"][n["boundary"]],
                                   "Failure: " + model["failures"][n["failure"]],
                                   "Evidence: " + ", ".join(n["evidence"])]})
        spec = {"schema_version":1,"diagram_type":"architecture",
                "meta":{"title":TITLES[name],"subtitle":"Static authored hypothesis map; arrows are not live traffic or scientific proof.",
                        "output":f"blueprint-{name}.html","animation":"none",
                        "visual_preset":"blueprint","locale":"en","quality_profile":"showcase"},
                "components":components,"connections":connections,"cards":cards}
        path = dest / f"blueprint-{name}.json"
        path.write_text(json.dumps(spec, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
        print(name, len(components), len(connections), path)

if __name__ == "__main__":
    build()
