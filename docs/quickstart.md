# Quickstart

## Prerequisites

```bash
# From this repository root
uv sync --extra dev
```

## Run the refinery pipeline

```bash
# 1. Run the analysis (generates refinery data, token plan, figures)
uv run python scripts/refinement_analysis.py

# 2. Run tests
uv run pytest tests/ -v
```

The manuscript-injection step (`scripts/z_generate_manuscript_variables.py`,
which substitutes `{{TOKEN}}` placeholders into `output/manuscript/`) imports
the shared `infrastructure.rendering.manuscript_injection` module. It therefore
runs only from a clone of [docxology/template](https://github.com/docxology/template);
the standalone smoke tests skip it.

## Full pipeline (from the template monorepo root)

```bash
./run.sh --project templates/template_gold_refinement --pipeline --core-only
```

## Verify outputs

```bash
# Check refinery results
python -m json.tool output/data/refinery_results.json

# Check manuscript variables
python -m json.tool output/data/manuscript_variables.json

# Verify no unresolved tokens
grep -r "{{" output/manuscript/ || echo "All resolved"
```

## Coverage gate

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
```
