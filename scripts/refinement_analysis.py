#!/usr/bin/env python3
"""Thin orchestrator: run the gold-refinery analysis pipeline.

Executes the refinery stages, generates the token plan, writes
``output/data/refinery_results.json`` and ``output/reports/token_plan.json``,
and logs the purity progression.

All computation lives in ``src/analysis_pipeline``; this script only
coordinates I/O.

Exit codes:
    0   analysis completed successfully
    1   unexpected error
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "src"))
sys.path.insert(0, str(_PROJECT_ROOT))
sys.path.insert(0, str(_PROJECT_ROOT.parents[2]))

CLAIM_SUPPORT_REGISTRY_NAME = "claim_support_registry.json"


def main() -> int:
    """CLI entry point."""
    from analysis_pipeline import run_analysis

    return run_analysis(_PROJECT_ROOT, registry_name=CLAIM_SUPPORT_REGISTRY_NAME)


if __name__ == "__main__":
    raise SystemExit(main())
