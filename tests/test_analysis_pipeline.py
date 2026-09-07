"""Tests for src/analysis_pipeline — payload shaping for the thin orchestrator.

``run_analysis`` is exercised end-to-end by ``tests/test_scripts_smoke.py``
via the script subprocess; these tests pin the pure payload builders.
"""

from __future__ import annotations

from pathlib import Path

from analysis_pipeline import (
    refinery_results_payload,
    reverse_assay_payload,
    token_plan_payload,
)
from composition import generate_token_plan
from config import load_gold_refinement_config
from refinery import CANONICAL_STAGES, run_refinery

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

_STAGE_ROW_FIELDS = {
    "order",
    "name",
    "input_purity",
    "output_purity",
    "karat",
    "metallurgical_operation",
    "manuscript_operation",
}


def _result_and_config():
    return run_refinery(), load_gold_refinement_config(_PROJECT_ROOT)


class TestRefineryResultsPayload:
    def test_fields_match_refinery_result(self):
        result, gr_config = _result_and_config()
        payload = refinery_results_payload(result, gr_config)

        assert payload["stage_count"] == result.stage_count
        assert payload["final_purity"] == result.final_purity
        assert payload["final_karat"] == result.final_karat.label
        assert payload["total_purity_gain"] == result.total_purity_gain
        assert payload["is_nine_nines_certified"] == result.is_nine_nines_certified
        assert payload["purity_sequence"] == list(result.purity_sequence)
        assert payload["reverse_assay_target"] == gr_config.reverse_assay_target

    def test_stage_rows_map_result_stages(self):
        result, gr_config = _result_and_config()
        payload = refinery_results_payload(result, gr_config)

        assert len(payload["stages"]) == len(result.stages)
        for row, stage in zip(payload["stages"], result.stages, strict=True):
            assert set(row) == _STAGE_ROW_FIELDS
            assert row["order"] == stage.order
            assert row["name"] == stage.name
            assert row["input_purity"] == stage.input_purity
            assert row["output_purity"] == stage.output_purity
            assert row["karat"] == stage.karat_grade.label
            assert row["metallurgical_operation"] == stage.metallurgical_operation
            assert row["manuscript_operation"] == stage.manuscript_operation


class TestTokenPlanPayload:
    def test_fields_match_token_plan(self):
        gr_config = load_gold_refinement_config(_PROJECT_ROOT)
        plan = generate_token_plan(gr_config)
        payload = token_plan_payload(plan)

        assert payload["seed"] == plan.seed
        assert payload["total_tokens"] == len(plan.choices)
        assert payload["category_counts"] == plan.category_counts
        assert payload["section_counts"] == plan.section_counts
        assert payload["choices"] == [c.as_dict() for c in plan.choices]


class TestReverseAssayPayload:
    def test_prefix_is_constrained_to_canonical_stages(self):
        result, gr_config = _result_and_config()
        payload = reverse_assay_payload(result, gr_config)

        canonical_names = [stage.name for stage in CANONICAL_STAGES]
        stage_names = payload["stage_names"]
        assert payload["schema_version"] == 1
        assert payload["target_purity"] == gr_config.reverse_assay_target
        assert payload["prefix_constrained"] is True
        assert stage_names, "reverse prefix must contain at least the first stage"
        assert stage_names == canonical_names[: len(stage_names)]
        assert payload["terminal_purity"] == CANONICAL_STAGES[len(stage_names) - 1].output_purity
