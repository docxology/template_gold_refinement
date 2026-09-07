# scripts/ — Thin Orchestrators

Technical specification for the gold-refinement exemplar's analysis scripts.

## Overview

Thin orchestrators that coordinate I/O and delegate to `src/`. No business
logic here — all computation lives in `src/`.

## Script Inventory

| Script | Purpose | Delegates to | Command |
|--------|---------|--------------|---------|
| `refinement_analysis.py` | Run the refinery analysis pipeline; write refinery results, token plan, reverse-assay report, receipts, figures, evidence registry, dashboard | `src/analysis_pipeline.py::run_analysis` | `uv run python scripts/refinement_analysis.py` |
| `z_generate_manuscript_variables.py` | Generate `{{TOKEN}}` variables, write `output/data/manuscript_variables.json`, inject into `output/manuscript/` | `src/manuscript_variables.py`, `infrastructure.rendering.manuscript_injection` | `uv run python scripts/z_generate_manuscript_variables.py` |
| `zz_generate_cover_visualization.py` | Generate the manuscript cover image (`output/figures/cover_visualization.png`) | `src/cover_visualization.py` | `uv run python scripts/zz_generate_cover_visualization.py` |

## Design Contract

- Scripts are orchestration only: path bootstrap, argument parsing, logging,
  and a single delegated call into a `src/` entrypoint.
- Data/model/plot/analysis logic lives in `src/` (importable and tested).
- Payload shaping and stage orchestration for the analysis run live in
  `src/analysis_pipeline.py` (`refinery_results_payload`, `token_plan_payload`,
  `reverse_assay_payload`, `run_analysis`); the script keeps only the path
  bootstrap and the delegated call.
- All reusable script behavior must be covered by tests in `tests/`
  (`test_scripts_smoke.py` exercises every script end-to-end).

## Run Order

The `z_`/`zz_` prefixes encode run order: both scripts run **after** analysis
and consume `output/data/refinery_results.json`; `zz_generate_cover_visualization.py`
runs last, after manuscript variables are generated, so the cover reflects the
same run's data.

## Commands

```bash
# Run the refinery analysis
uv run python scripts/refinement_analysis.py

# Generate manuscript variables (requires analysis outputs)
uv run python scripts/z_generate_manuscript_variables.py

# Draft mode (allows N/A fallbacks when analysis is missing)
uv run python scripts/z_generate_manuscript_variables.py --allow-draft

# Generate the cover visualization (requires analysis outputs)
uv run python scripts/zz_generate_cover_visualization.py
```
