# New AI hub preview — review before publication

Open `hub/index.html` after extracting the ZIP. The original results page is still `index.html` at the archive root. The four Archify views are embedded in the hub and can also be opened directly:

- `hub/blueprint-e19.html` — historical linear classifier; timing gate FAILED.
- `hub/blueprint-e20.html` — proposed language adaptation; not locked or run.
- `hub/blueprint-e21-v2.html` — proposed energy-versus-direct mechanism; unrun.
- `hub/blueprint-future-v3.html` — long-term composition; not implemented.

Three alternative visual directions are in `hub/design-demos/`: A Silver Lab (the fuller interactive hub), B Evidence Desk, and C Field Guide. They are design candidates, not three published sites. The full typed relation and evidence registry is `hub/blueprint-ledger.json`; source documents are in `hub/docs/`. The historical E19 JSON and source archive remain in `data/` and `source/`.

The Archify `finalize --quality showcase` gates passed for all four views, but automated browser checks do not constitute a scientific result. The long-term graph still has several visually crossing/detoured relations; the ledger preserves each relation unambiguously. Local desktop/mobile testing and link checks passed. **No live site deployment or owner design choice is implied by this ZIP.**

To run the structural checks from the extracted archive root: `python -m unittest discover -s hub -p test_hub.py -v`. Rendering the bundled HTML does not need a model, GPU, network or build step. For future revisions, `hub/build_blueprint.py` regenerates the four native Archify JSON projections from the checked-in ledger; Archify itself is an external tool, not bundled into this archive.
