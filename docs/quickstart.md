# Build and verify the gold-refinement exemplar

## Standalone analysis and tests

Install Git and uv. The project pins Python 3.13 for standalone development.
From the repository root, install the locked dependencies and run the analysis
and coverage gate:

```bash
uv sync --locked --extra dev
uv run --no-sync python scripts/refinement_analysis.py
uv run --no-sync pytest tests/ --cov=src --cov-fail-under=90
```

Analysis uses [the manuscript configuration](manuscript/config.yaml), the
experiment plan and domain profile in the repository root, and the claim ledger
in [data/](../data/README.md). It generates the refinery data, token plan,
dashboard, and figures described in [output conventions](output_conventions.md).

## Render this checkout

Install Pandoc, a matching `pandoc-crossref` filter, and XeLaTeX with the required
TeX packages. The local check used Pandoc 3.1.13, pandoc-crossref 0.3.17.1
(built for Pandoc 3.1.13), and TeX Live 2025. See the pinned
[format guide](https://github.com/docxology/template/blob/87704feae0a4490ef7dad9c931d268e8c30273c2/docs/usage/output-formats.md)
for system requirements. The shared renderer and its manuscript hydration subprocess require Python 3.14 or newer.

Run these commands from a clean checkout of this project. The detached copy
keeps regenerated files separate from the tracked release snapshots in your
working checkout. Place the copy inside `projects/working/` so the renderer's
hydration subprocess can read the project.

```bash
project_root="$(pwd -P)"
verification_dir="$(mktemp -d)"
project_copy="$verification_dir/template/projects/working/template_gold_refinement"
git clone https://github.com/docxology/template.git "$verification_dir/template"
git -C "$verification_dir/template" checkout --detach 87704feae0a4490ef7dad9c931d268e8c30273c2
mkdir -p "$verification_dir/template/projects/working"
git clone --no-hardlinks "$project_root" "$project_copy"
git -C "$project_copy" checkout --detach "$(git -C "$project_root" rev-parse HEAD)"

export SOURCE_DATE_EPOCH=1782345600
cd "$project_copy"
uv sync --locked --extra dev --python 3.14
uv run --no-sync --python 3.14 python scripts/refinement_analysis.py

cd "$verification_dir/template"
uv sync --locked --no-dev
uv run --no-sync python scripts/pipeline/stage_03_render.py --project working/template_gold_refinement
uv run --no-sync python scripts/pipeline/stage_04_validate.py --project working/template_gold_refinement
```

Stage 03 invokes the variable generator and hydrates the [authored sections](manuscript/README.md)
from `docs/manuscript/` into `output/manuscript/` before rendering. Stage 04
validates the project-local outputs and records their source provenance.

Inspect these files under `"$project_copy/output"`:

- `pdf/template_gold_refinement_combined.pdf` and `web/index.html` for the
  paper's ordered sections, bibliography, and registered figures
- `figures/figure_registry.json` and `reports/figure_quality_report.json`
  for the figure inventory and quality checks
- `reports/validation_report.json` and `reports/rendered_provenance.json`
  for Stage 04 results and source bindings
