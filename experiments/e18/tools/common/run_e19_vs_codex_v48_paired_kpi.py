#!/usr/bin/env python3
"""Live paired matches: each line's newest candidate vs Codex V48 (770),
producing per-game profiles for a 22-panel D1-D30 KPI report (E18 standard
V4.1, experiments/e18/reports/common/E18_AGENT_COMPARISON_REPORT_STANDARD_V4_IT.md).

A standing verification instrument, not a one-off: REGISTRY below maps a
candidate name to its factory and source file, and PAIRINGS is derived
from it -- adding a new candidate is a single dict entry, immediately
runnable with `--only NAME` and reportable by
build_e19_vs_codex_v48_kpi_reports.py. Each pairing runs over the E18
development seed set (both seats, 14 games per pairing) -- the same seeds
and seat policy every prior common tournament in this round has used
(experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json, seed_policy.development).

Registered so far:

- CLAUDE_E18_4  (agricola.strategy.claude.e18_capacity_certified_v4)
- ANTIGRAVITY_E19_1 (agricola.strategy.antigravity.antigravity_e19_hybrid_livestock_v1)
- COPILOT_E18_8_V5 (agricola.strategy.copilot.e18_economic_recovery_v5)
- CLAUDE_E18_5 (agricola.strategy.claude.e18_wheat_market_fix_v5)

vs the single external reference:

- CODEX_V48 (submission/submission_codex_e18_770_v48_external.py, the
  published Kaggle bundle referenced by docs/PROJECT_STATE.md)

No holdout or final-confirmation seed is consumed. This is a live,
paired, real-engine benchmark -- NOT a comparison against an external
replay -- so both sides of every match are audited symmetrically with the
same post-hoc reconciliation tooling Codex's own reports already use
(deterministic re-execution of engine._commit_unit/_do_hire/_do_buy_land
against the recorded action stream, verified against the recorded cash
at every step): these are pure, agent-neutral analysis functions over a
completed replay, not any agent's strategy code, so reusing them here
carries no policy dependency for any of the four lines being compared.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kaggle_environments import make

from agricola.strategy.antigravity.antigravity_e19_hybrid_livestock_v1 import (
    create_antigravity_e19_agent,
)
from agricola.strategy.antigravity.antigravity_e19_2_hybrid_livestock import (
    create_antigravity_e19_2_agent,
)
from agricola.strategy.claude.e18_capacity_certified_v4 import (
    create_claude_e18_capacity_certified_v4,
)
from agricola.strategy.claude.e18_wheat_market_fix_v5 import (
    create_claude_e18_wheat_market_fix_v5,
)
from agricola.strategy.copilot.e18_economic_recovery_v5 import (
    create_copilot_e18_economic_recovery_v5,
)
from agricola.strategy.copilot.e18_economic_recovery_v6 import (
    create_copilot_e18_economic_recovery_v6,
)
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import (
    snapshot,
)
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import (
    audit,
    end_state,
)
from docs.model_specs.codex.e18.tools.e18_29_crop_service_audit import (
    crop_service_audit,
)
from experiments.e18.tools.common.replay_daily_operational_kpi import (
    daily_operational_kpi,
)

ROOT = Path(__file__).resolve().parents[4]
CODEX_BUNDLE = ROOT / "submission/submission_codex_e18_770_v48_external.py"
MANIFEST = ROOT / "experiments/e18/manifest/E18_COMMON_MANIFEST_V1.json"
OUT = ROOT / "experiments/e18/artifacts/derived/common/e19_vs_codex_v48_paired_kpi_20260909"

CLAUDE = "CLAUDE_E18_4"
ANTIGRAVITY = "ANTIGRAVITY_E19_1"
ANTIGRAVITY_V2 = "ANTIGRAVITY_E19_2"
COPILOT = "COPILOT_E18_8_V5"
CLAUDE_V5 = "CLAUDE_E18_5"
COPILOT_V6 = "COPILOT_E18_10_V6"
CODEX = "CODEX_V48"

# Registry: add a new candidate here (factory + source) and it is
# immediately playable with --only NAME and reportable by
# build_e19_vs_codex_v48_kpi_reports.py -- this pair of scripts is meant
# to stay a standing verification instrument for this line's own
# candidates against Codex V48, not a one-off for this session's three.
REGISTRY: dict[str, dict[str, Any]] = {
    CLAUDE: dict(
        factory=create_claude_e18_capacity_certified_v4,
        source=ROOT / "src/agricola/strategy/claude/e18_capacity_certified_v4.py",
    ),
    ANTIGRAVITY: dict(
        factory=create_antigravity_e19_agent,
        source=ROOT
        / "src/agricola/strategy/antigravity/antigravity_e19_hybrid_livestock_v1.py",
    ),
    ANTIGRAVITY_V2: dict(
        factory=create_antigravity_e19_2_agent,
        source=ROOT
        / "src/agricola/strategy/antigravity/antigravity_e19_2_hybrid_livestock.py",
    ),
    COPILOT: dict(
        factory=create_copilot_e18_economic_recovery_v5,
        source=ROOT / "src/agricola/strategy/copilot/e18_economic_recovery_v5.py",
    ),
    CLAUDE_V5: dict(
        factory=create_claude_e18_wheat_market_fix_v5,
        source=ROOT / "src/agricola/strategy/claude/e18_wheat_market_fix_v5.py",
    ),
    COPILOT_V6: dict(
        factory=create_copilot_e18_economic_recovery_v6,
        source=ROOT / "src/agricola/strategy/copilot/e18_economic_recovery_v6.py",
    ),
}
PAIRINGS = tuple(REGISTRY)
SOURCES = {name: entry["source"] for name, entry in REGISTRY.items()} | {CODEX: CODEX_BUNDLE}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _codex_factory():
    module_globals = runpy.run_path(str(CODEX_BUNDLE))
    return module_globals["create_agent"]


def _candidate_factory(name: str):
    return REGISTRY[name]["factory"]


def _profile(replay: dict[str, Any], seat: int) -> dict[str, Any]:
    daily = [snapshot(replay, day, seat) for day in range(1, 31)]
    ledger = audit(replay, seat)
    return {
        "seat": seat,
        "reward": replay["rewards"][seat],
        "daily": daily,
        "ledger": ledger,
        "operational_daily": daily_operational_kpi(replay, seat, ledger),
        "terminal": end_state(replay, seat),
        "crop_starvation": crop_service_audit(replay, seat),
    }


def run_case(candidate_name: str, seed: int, candidate_seat: int) -> Path:
    codex_seat = 1 - candidate_seat
    candidate_policy = _candidate_factory(candidate_name)(
        run_context={
            "run_id": f"E19-VS-CODEX-V48-S{seed}-P{candidate_seat}-{candidate_name}",
            "episode_id": f"E19-VS-CODEX-V48-S{seed}-P{candidate_seat}-{candidate_name}",
            "seed": seed,
            "player_position": candidate_seat,
        }
    )
    codex_policy = _codex_factory()(
        run_context={"player_position": codex_seat, "seed": seed}
    )
    players = [None, None]
    players[candidate_seat] = candidate_policy
    players[codex_seat] = codex_policy

    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed, "turnsPerDay": 24},
        debug=False,
    )
    env.run(players)
    replay = env.toJSON()
    assert len(replay["steps"]) == 720
    assert all(row["status"] == "DONE" for row in replay["steps"][-1])

    data = {
        "candidate": candidate_name,
        "seed": seed,
        "candidate_seat": candidate_seat,
        "codex_seat": codex_seat,
        "configuration": replay["configuration"],
        "sides": {
            "candidate": _profile(replay, candidate_seat),
            "codex": _profile(replay, codex_seat),
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{candidate_name}_{seed}_{candidate_seat}.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "candidate": candidate_name,
                "seed": seed,
                "candidate_seat": candidate_seat,
                "candidate_cash": data["sides"]["candidate"]["reward"],
                "codex_cash": data["sides"]["codex"]["reward"],
            }
        ),
        flush=True,
    )
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=PAIRINGS, default=None)
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seeds = [int(value) for value in manifest["seed_policy"]["development"]]
    reserved = {
        *map(int, manifest["seed_policy"]["holdout"]["seeds"]),
        *map(int, manifest["seed_policy"]["final_confirmation"]["seeds"]),
    }
    if set(seeds).intersection(reserved):
        raise RuntimeError("development matrix overlaps a reserved seed")
    assert manifest["seed_policy"]["failed_run_replacement"] == "FORBIDDEN"

    pairings = (args.only,) if args.only else PAIRINGS
    all_cases = [
        (name, seed, seat)
        for name in pairings
        for seed in seeds
        for seat in (0, 1)
    ]
    cases = [
        case for case in all_cases if not (OUT / f"{case[0]}_{case[1]}_{case[2]}.json").exists()
    ]
    skipped = len(all_cases) - len(cases)
    total = len(all_cases)
    if skipped:
        print(f"{skipped}/{total} case(s) already present, skipping", flush=True)
    failures: list[str] = []
    OUT.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(run_case, name, seed, seat): (name, seed, seat) for name, seed, seat in cases}
        done = skipped
        for future in as_completed(futures):
            name, seed, seat = futures[future]
            done += 1
            try:
                future.result()
                print(f"[{done:02d}/{total}] {name} seed={seed} seat={seat} OK", flush=True)
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{name} seed={seed} seat={seat}: {exc!r}")
                print(f"[{done:02d}/{total}] {name} seed={seed} seat={seat} FAILED: {exc!r}", flush=True)

    provenance = {
        name: {
            "source": str(SOURCES[name].relative_to(ROOT)).replace("\\", "/"),
            "source_sha256": _sha256(SOURCES[name]),
        }
        for name in (*PAIRINGS, CODEX)
    }
    (OUT / "provenance.json").write_text(
        json.dumps(
            {
                "seeds": seeds,
                "seats": [0, 1],
                "pairings": list(PAIRINGS),
                "opponent": CODEX,
                "match_count": total,
                "holdout_consumed": False,
                "final_confirmation_consumed": False,
                "provenance": provenance,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    if failures:
        raise RuntimeError(f"{len(failures)} case(s) failed: {failures}")
    print(f"wrote {total} profiles to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
