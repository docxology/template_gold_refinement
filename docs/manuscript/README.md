# Manuscript

This directory holds the authored sources for `template_gold_refinement`.
Use the [build guide](../quickstart.md#render-this-checkout) to generate a
hydrated copy in `output/manuscript/`, then render and validate PDF and HTML.
See [manuscript status](MANUSCRIPT_STATUS.md) for the publication role and
[syntax](SYNTAX.md) for source conventions.

## Files

| File | Role |
|------|------|
| [`00_000_transmission_begin.md`](00_000_transmission_begin.md) | Opening transmission bookend |
| [`00_abstract.md`](00_abstract.md) | Abstract with purity summary |
| [`01_introduction.md`](01_introduction.md) | Introduction: ore to nine-nines |
| [`02_methodology.md`](02_methodology.md) | Methodology: the refinery pipeline |
| [`03_results.md`](03_results.md) | Results: purity progression and karat grading |
| [`04_discussion.md`](04_discussion.md) | Discussion: load-bearing vs rhetorical |
| [`05_conclusion.md`](05_conclusion.md) | Conclusion: certification and forking |
| [`06_reproducibility.md`](06_reproducibility.md) | Reproducibility: seeded regeneration |
| [`07_scope.md`](07_scope.md) | Scope: related work and limitations |
| [`08_evaluation.md`](08_evaluation.md) | Evaluation: QA probes, audit rules, and integrity gates |
| [`09_authoring_contract.md`](09_authoring_contract.md) | Authoring contract: human review and responsible forks |
| [`99_999_transmission_end.md`](99_999_transmission_end.md) | Closing transmission bookend |
| [`config.yaml`](config.yaml) | Paper metadata and gold_refinement block |
| [`config.yaml.example`](config.yaml.example) | Fork template |
| [`preamble.md`](preamble.md) | LaTeX preamble |
| [`references.bib`](references.bib) | BibTeX bibliography |
| [`layer_contract.yaml`](layer_contract.yaml) | Layer boundary contract |

## Generated-variable discipline

Manuscript source files should contain prose, cross-reference labels, and
`{{TOKEN}}` placeholders. Generated numbers, figure blocks, formalism rows,
claim-support summaries, evidence-tier summaries, and figure-quality summaries
come from `src/manuscript_variables.py` and `output/data/manuscript_variables.json`.

Do not hard-code figure numbers, equation numbers, table numbers, generated
counts, support rates, evidence fact counts, or figure-quality totals in
manuscript prose. Use `[@fig:...]`, `[@eq:...]`, `[@tbl:...]`, and generated
variables so prerender, registry, evidence, and citation gates can detect drift.

## Visual QA text

Results and reproducibility sections intentionally describe
`output/reports/figure_quality_report.json`. That report is generated from
source-owned figure specs and records PNG/SVG presence, dimensions, nonblank
pixel checks, color variance, and registry parity. If a fork changes figures,
update the `src/figures/` package, regenerate Stage 02, and let the manuscript consume
the refreshed variables rather than editing rendered Markdown.

Provide an accessibility description in each figure specification. Stage 03
reads it from the generated registry when it builds HTML.
