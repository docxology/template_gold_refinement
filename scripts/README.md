# scripts

Thin orchestrator scripts for the gold-refinement exemplar: path bootstrap,
argument parsing, logging, and a single delegated call into `src/`. All
computation lives in `src/`. See [AGENTS.md](AGENTS.md) for the contract.

## Inventory

| Script | Purpose | Delegates to | Command |
|--------|---------|--------------|---------|
| `refinement_analysis.py` | Run the refinery analysis pipeline; write refinery results, token plan, reverse-assay report, receipts, figures, evidence registry, dashboard | `src/analysis_pipeline.py::run_analysis` | `uv run python scripts/refinement_analysis.py` |
| `z_generate_manuscript_variables.py` | Generate `{{TOKEN}}` variables, write `output/data/manuscript_variables.json`, inject into `output/manuscript/` | `src/manuscript_variables.py::generate_variables` + `save_variables`, `infrastructure.rendering.manuscript_injection::write_resolved_manuscript_tree` | `uv run python scripts/z_generate_manuscript_variables.py` (`--allow-draft` for draft mode) |
| `zz_generate_cover_visualization.py` | Generate the manuscript cover image and its report | `src/cover_visualization.py::write_cover_visualization` | `uv run python scripts/zz_generate_cover_visualization.py` |

## Outputs

- `refinement_analysis.py` — `output/data/refinery_results.json`,
  `output/reports/token_plan.json`, `output/reports/reverse_assay.json`,
  `output/reports/transmission_bookends.json`,
  `output/reports/analogy_boundary_receipt.json`,
  `output/reports/claim_support_registry.json`, `output/figures/*`,
  `output/dashboard.html`
- `z_generate_manuscript_variables.py` — `output/data/manuscript_variables.json`,
  `output/manuscript/*`
- `zz_generate_cover_visualization.py` — `output/figures/cover_visualization.png`,
  `output/reports/cover_visualization.json`
