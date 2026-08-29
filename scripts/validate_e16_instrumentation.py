"""Build the E0 report and pre-training manifests; never runs Stage A."""

from __future__ import annotations

from pathlib import Path

from agricola.e16.config import load_frozen_config
from agricola.e16.runner import (
    RESULTS_ROOT,
    run_e0,
    write_implementation_manifest,
    write_planned_stage_a_manifest,
)


def render_report(report: dict) -> str:
    lines = [
        "# E16 E0 Instrumentation Report",
        "",
        "Evidence role: E0_NON_ANALYTIC_SMOKE",
        "",
        f"E0_STATUS: {report['status']}",
        "",
        "This smoke output is excluded from TRAINING, bounds, and model-spec updates.",
        "",
        "## Checks",
        "",
    ]
    for name, passed in report["checks"].items():
        lines.append(f"- {'PASS' if passed else 'FAIL'}: `{name}`")
    lines.extend(["", "## Watering smoke metrics", ""])
    for episode in report["smoke_episodes"]:
        metrics = episode["telemetry"]
        lines.append(
            f"- P{episode['treatment_seat']}: status={metrics['watering_metric_status']}, "
            f"effects={metrics['successful_watering_effects']}, "
            f"needs={metrics['watering_need_denominator']}, "
            f"execution_rate={metrics['watering_execution_rate']:.6f}, "
            f"continuity={metrics['watering_continuity']:.6f}"
        )
    lines.extend(
        [
            "",
            "## Provenance",
            "",
            f"- Event count: {report['event_count']}",
            "- Smoke episodes: "
            + ", ".join(
                f"`{episode['episode_id']}`" for episode in report["smoke_episodes"]
            ),
            "- T0 steps: "
            + ", ".join(
                str(episode["telemetry"]["t0_step"])
                for episode in report["smoke_episodes"]
            ),
            f"- Generated: {report['generated_at']}",
            "",
            "E16-A-R1 was not run. The original Stage A evidence remains preserved.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    report = run_e0()
    path = RESULTS_ROOT / "instrumentation" / "E16_E0_REPORT.md"
    path.write_text(render_report(report), encoding="utf-8")
    config = load_frozen_config()
    write_implementation_manifest(config, report["status"])
    write_planned_stage_a_manifest(config)
    print(f"E0_STATUS={report['status']}")
    print(f"REPORT={Path(path)}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
