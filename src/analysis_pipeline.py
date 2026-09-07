"""Gold-refinery analysis pipeline: computation behind the thin orchestrator.

``scripts/refinement_analysis.py`` coordinates I/O only. Every stage of the
analysis run — refinery execution, token-plan generation, payload shaping for
``refinery_results.json`` / ``token_plan.json`` / the reverse-assay report,
validation receipts, figures, the evidence registry, and the dashboard —
lives here as importable, testable functions.
"""

from __future__ import annotations

import json
from pathlib import Path

try:
    from .analogy_boundary import validate_analogy_boundary
    from .composition import TokenPlan, generate_token_plan
    from .config import GoldRefinementConfig, load_gold_refinement_config
    from .dashboard import write_dashboard
    from .domain_adapter import load_domain_profile
    from .evidence import build_evidence_registry, write_evidence_registry
    from .figures import generate_all_figures
    from .refinery import RefineryResult, run_refinery, stages_to_target
    from .transmission import validate_transmission_bookends
except ImportError:  # pragma: no cover - plain-import fallback for script execution
    from analogy_boundary import validate_analogy_boundary  # type: ignore[no-redef]
    from composition import TokenPlan, generate_token_plan  # type: ignore[no-redef]
    from config import GoldRefinementConfig, load_gold_refinement_config  # type: ignore[no-redef]
    from dashboard import write_dashboard  # type: ignore[no-redef]
    from domain_adapter import load_domain_profile  # type: ignore[no-redef]
    from evidence import build_evidence_registry, write_evidence_registry  # type: ignore[no-redef]
    from figures import generate_all_figures  # type: ignore[no-redef]
    from refinery import RefineryResult, run_refinery, stages_to_target  # type: ignore[no-redef]
    from transmission import validate_transmission_bookends  # type: ignore[no-redef]


def refinery_results_payload(result: RefineryResult, gr_config: GoldRefinementConfig) -> dict[str, object]:
    """Build the ``refinery_results.json`` payload from a refinery run."""
    return {
        "stage_count": result.stage_count,
        "final_purity": result.final_purity,
        "final_karat": result.final_karat.label,
        "total_purity_gain": result.total_purity_gain,
        "is_nine_nines_certified": result.is_nine_nines_certified,
        "purity_sequence": list(result.purity_sequence),
        "reverse_assay_target": gr_config.reverse_assay_target,
        "stages": [
            {
                "order": s.order,
                "name": s.name,
                "input_purity": s.input_purity,
                "output_purity": s.output_purity,
                "karat": s.karat_grade.label,
                "metallurgical_operation": s.metallurgical_operation,
                "manuscript_operation": s.manuscript_operation,
            }
            for s in result.stages
        ],
    }


def token_plan_payload(token_plan: TokenPlan) -> dict[str, object]:
    """Build the ``token_plan.json`` payload from a generated token plan."""
    return {
        "seed": token_plan.seed,
        "total_tokens": len(token_plan.choices),
        "category_counts": token_plan.category_counts,
        "section_counts": token_plan.section_counts,
        "choices": [c.as_dict() for c in token_plan.choices],
    }


def reverse_assay_payload(result: RefineryResult, gr_config: GoldRefinementConfig) -> dict[str, object]:
    """Build the reverse-assay report payload for ``reverse_assay_target``."""
    reverse_prefix = stages_to_target(gr_config.reverse_assay_target, result.stages)
    return {
        "schema_version": 1,
        "target_purity": gr_config.reverse_assay_target,
        "stage_names": [stage.name for stage in reverse_prefix],
        "terminal_purity": reverse_prefix[-1].output_purity if reverse_prefix else result.stages[0].input_purity,
        "prefix_constrained": True,
    }


def run_analysis(project_root: Path, registry_name: str) -> int:
    """Run the full gold-refinery analysis pipeline under ``project_root``.

    Single delegated entry point for ``scripts/refinement_analysis.py``:
    executes the refinery, writes all result payloads, receipts, figures,
    the evidence registry, and the dashboard, and prints a progress log.
    """
    # Run the refinery
    result = run_refinery()

    # Generate the token plan
    gr_config = load_gold_refinement_config(project_root)
    token_plan = generate_token_plan(gr_config)

    # Write refinery results
    data_dir = project_root / "output" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    refinery_path = data_dir / "refinery_results.json"
    refinery_path.write_text(
        json.dumps(refinery_results_payload(result, gr_config), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote {refinery_path}")

    # Write token plan
    reports_dir = project_root / "output" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    plan_path = reports_dir / "token_plan.json"
    plan_path.write_text(
        json.dumps(token_plan_payload(token_plan), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote {plan_path}")

    reverse_path = project_root / gr_config.reverse_assay_report_path
    reverse_path.parent.mkdir(parents=True, exist_ok=True)
    reverse_path.write_text(
        json.dumps(reverse_assay_payload(result, gr_config), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote {reverse_path}")

    transmission = validate_transmission_bookends(project_root / "docs" / "manuscript")
    transmission_path = reports_dir / "transmission_bookends.json"
    transmission_path.write_text(json.dumps(transmission, indent=2), encoding="utf-8")
    print(f"Wrote {transmission_path}")

    analogy = validate_analogy_boundary(load_domain_profile(project_root))
    analogy_path = reports_dir / "analogy_boundary_receipt.json"
    analogy_path.write_text(json.dumps(analogy, indent=2), encoding="utf-8")
    print(f"Wrote {analogy_path}")

    # Generate figures
    figure_paths = generate_all_figures(project_root)
    for fp in figure_paths:
        print(f"Wrote {fp}")

    # Build evidence registry
    registry = build_evidence_registry(gr_config, project_root)
    registry_path = reports_dir / registry_name
    write_evidence_registry(registry, registry_path)
    print(f"Wrote {registry_path}")
    print(f"  Evidence: {registry.supported_claims}/{registry.total_claims} claims supported")

    # Build dashboard
    dashboard_path = write_dashboard(project_root)
    print(f"Wrote {dashboard_path}")

    # Summary
    print("\nRefinery pipeline complete:")
    print(f"  Stages: {result.stage_count}")
    print(f"  Final purity: {result.final_purity:.10f}")
    print(f"  Final karat: {result.final_karat.label}")
    print(f"  Nine-nines certified: {result.is_nine_nines_certified}")
    print(f"  Tokens generated: {len(token_plan.choices)}")

    return 0


__all__ = [
    "refinery_results_payload",
    "reverse_assay_payload",
    "run_analysis",
    "token_plan_payload",
]
