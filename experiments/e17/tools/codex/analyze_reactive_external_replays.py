"""Forensic benchmark of the ten external E17 reactive Kaggle replays.

The extractor is analysis-only. Replay actions are treated as requested
commands; farm snapshots are treated as executed state.  It reuses the frozen
E17 Top-3 parser so that the external probe and the discovery corpus share the
same definitions.
"""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
from collections import Counter, defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import analyze_top3_replays as base

ROOT = Path(__file__).resolve().parents[4]
REPLAY_DIR = ROOT / "data" / "replays" / "json"
OUT_DIR = ROOT / "experiments" / "e17" / "artifacts" / "discovery" / "codex"
REPORT_PATH = (
    ROOT
    / "experiments"
    / "e17"
    / "reports"
    / "codex"
    / "E17_REACTIVE_EXTERNAL_REPLAY_BENCHMARK_IT.md"
)
TOP3_METRICS_PATH = OUT_DIR / "E17_TOP3_REPLAY_METRICS.json"
TOP3_DAILY_PATH = OUT_DIR / "E17_QUADRANT_DAILY_TIMELINE.csv"

EPISODE_IDS = (
    104857899,
    104860472,
    104863004,
    104863880,
    104864729,
    104865577,
    104866465,
    104867319,
    104868160,
    104869022,
)
OWNER_NAME = "Pietro Valocchi"
ANALYSIS_END_DAY = 28
MILESTONE_DAYS = (0, 5, 10, 15, 20, 25, 28, 29)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_fingerprint(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def owner_trajectory_fingerprints(
    raw: dict[str, Any], player_id: int
) -> dict[str, str]:
    requested_actions: list[Any] = []
    structural_states: list[dict[str, Any]] = []
    for step_index, step in enumerate(raw.get("steps") or []):
        if not isinstance(step, list) or player_id >= len(step):
            continue
        record = step[player_id]
        if not isinstance(record, dict):
            continue
        requested_actions.append(record.get("action"))
        farm = base.farm_for(record, player_id)
        day, hour = base.clock(record, step_index)
        structural_states.append(
            {
                "day": day,
                "hour": hour,
                "farmer": farm.get("farmer"),
                "hands": farm.get("hands"),
                "tiles": farm.get("tiles"),
                "unlocked_quadrants": farm.get("unlocked_quadrants"),
            }
        )
    return {
        "requested_action_stream_sha256": canonical_fingerprint(requested_actions),
        "executed_structural_trajectory_sha256": canonical_fingerprint(
            structural_states
        ),
    }


def mean(values: Iterable[float]) -> float:
    materialized = list(values)
    return round(statistics.mean(materialized), 2) if materialized else 0.0


def median(values: Iterable[float]) -> float | None:
    materialized = list(values)
    return round(statistics.median(materialized), 2) if materialized else None


def ratio(numerator: float, denominator: float) -> float | None:
    if not denominator:
        return None
    return round(100 * numerator / denominator, 2)


def pearson(left: list[float], right: list[float]) -> float | None:
    if len(left) != len(right) or len(left) < 2:
        return None
    left_mean = statistics.mean(left)
    right_mean = statistics.mean(right)
    numerator = sum((x - left_mean) * (y - right_mean) for x, y in zip(left, right))
    left_scale = sum((x - left_mean) ** 2 for x in left) ** 0.5
    right_scale = sum((y - right_mean) ** 2 for y in right) ** 0.5
    if not left_scale or not right_scale:
        return None
    return round(numerator / (left_scale * right_scale), 4)


def row_lookup(
    daily_rows: list[dict[str, Any]],
) -> dict[tuple[int, int, int, str], dict[str, Any]]:
    return {
        (
            int(row["episode_id"]),
            int(row["player_id"]),
            int(row["day"]),
            str(row["quadrant_slot"]),
        ): row
        for row in daily_rows
    }


def quadrant_livestock_profile(
    summary: dict[str, Any],
    daily_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    q2_unlock = summary.get("q2_unlock") or {}
    start_day = int(q2_unlock.get("day", ANALYSIS_END_DAY))
    selected = [
        row
        for row in daily_rows
        if row["episode_id"] == summary["episode_id"]
        and row["player_id"] == summary["player_id"]
        and start_day <= row["day"] <= ANALYSIS_END_DAY
    ]
    animal_tile_days = {
        slot: sum(
            row["animal_total"] for row in selected if row["quadrant_slot"] == slot
        )
        for slot in ("Q0", "Q1", "Q2")
    }
    observed_days = max(
        1,
        len({row["day"] for row in selected}),
    )
    lookup = row_lookup(daily_rows)

    def snapshot(day: int, slot: str) -> dict[str, Any]:
        return lookup.get(
            (summary["episode_id"], summary["player_id"], day, slot),
            {},
        )

    q2_d28 = snapshot(ANALYSIS_END_DAY, "Q2")
    q2_d29 = snapshot(29, "Q2")
    total_tile_days = sum(animal_tile_days.values())
    return {
        "episode_id": summary["episode_id"],
        "player_id": summary["player_id"],
        "q2_unlock_day": start_day,
        "observed_days_q2_to_d28": observed_days,
        "q0_animal_tile_days": animal_tile_days["Q0"],
        "q1_animal_tile_days": animal_tile_days["Q1"],
        "q2_animal_tile_days": animal_tile_days["Q2"],
        "mean_q0_animals": round(animal_tile_days["Q0"] / observed_days, 2),
        "mean_q1_animals": round(animal_tile_days["Q1"] / observed_days, 2),
        "mean_q2_animals": round(animal_tile_days["Q2"] / observed_days, 2),
        "q2_vs_q0_animal_pct": ratio(animal_tile_days["Q2"], animal_tile_days["Q0"]),
        "q2_share_of_3q_animal_pct": ratio(animal_tile_days["Q2"], total_tile_days),
        "q2_d28_animals": int(q2_d28.get("animal_total", 0)),
        "q2_d29_animals": int(q2_d29.get("animal_total", 0)),
        "q2_d28_crops": int(q2_d28.get("crop_total", 0)),
        "q2_d29_crops": int(q2_d29.get("crop_total", 0)),
        "q2_d28_idle": int(q2_d28.get("idle_total", 0)),
        "q2_d29_idle": int(q2_d29.get("idle_total", 0)),
        "q2_d28_goose": int(q2_d28.get("GOOSE", 0)),
        "q2_d28_cow": int(q2_d28.get("COW", 0)),
        "q2_d28_sheep": int(q2_d28.get("SHEEP", 0)),
    }


def top3_livestock_reference() -> list[dict[str, Any]]:
    if not TOP3_METRICS_PATH.exists() or not TOP3_DAILY_PATH.exists():
        return []
    metrics = json.loads(TOP3_METRICS_PATH.read_text(encoding="utf-8"))
    with TOP3_DAILY_PATH.open(encoding="utf-8", newline="") as handle:
        daily = list(csv.DictReader(handle))
    daily_lookup: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in daily:
        normalized = dict(row)
        for key in ("episode_id", "player_id", "day", "animal_total"):
            normalized[key] = int(normalized[key])
        daily_lookup[(normalized["episode_id"], normalized["player_id"])].append(
            normalized
        )

    per_agent: dict[str, dict[str, float | int]] = defaultdict(
        lambda: {"episodes": 0, "days": 0, "q0": 0, "q1": 0, "q2": 0}
    )
    for summary in metrics["participant_summaries"]:
        name = summary["player_name"]
        if name not in base.TOP3:
            continue
        q2_unlock = summary.get("q2_unlock") or {}
        start_day = int(q2_unlock.get("day", ANALYSIS_END_DAY))
        rows = [
            row
            for row in daily_lookup[(summary["episode_id"], summary["player_id"])]
            if start_day <= row["day"] <= ANALYSIS_END_DAY
        ]
        day_count = len({row["day"] for row in rows})
        aggregate = per_agent[name]
        aggregate["episodes"] += 1
        aggregate["days"] += day_count
        for slot in ("Q0", "Q1", "Q2"):
            aggregate[slot.lower()] += sum(
                row["animal_total"] for row in rows if row["quadrant_slot"] == slot
            )

    result: list[dict[str, Any]] = []
    for name in base.TOP3:
        aggregate = per_agent[name]
        days = int(aggregate["days"])
        q0 = float(aggregate["q0"])
        q1 = float(aggregate["q1"])
        q2 = float(aggregate["q2"])
        total = q0 + q1 + q2
        result.append(
            {
                "agent": name,
                "source": "E17 Top-3 discovery corpus",
                "episodes": int(aggregate["episodes"]),
                "observed_days": days,
                "mean_q0_animals": round(q0 / days, 2) if days else 0.0,
                "mean_q1_animals": round(q1 / days, 2) if days else 0.0,
                "mean_q2_animals": round(q2 / days, 2) if days else 0.0,
                "q2_vs_q0_animal_pct": ratio(q2, q0),
                "q2_share_of_3q_animal_pct": ratio(q2, total),
            }
        )
    return result


def aggregate_owner(
    owner_summaries: list[dict[str, Any]],
    livestock: list[dict[str, Any]],
) -> dict[str, Any]:
    by_episode = {row["episode_id"]: row for row in livestock}
    groups = {
        "ALL": owner_summaries,
        "WIN": [row for row in owner_summaries if row["result"] == "WIN"],
        "LOSS": [row for row in owner_summaries if row["result"] == "LOSS"],
    }
    rows: list[dict[str, Any]] = []
    for label, group in groups.items():
        related = [by_episode[row["episode_id"]] for row in group]
        q0_tile_days = sum(row["q0_animal_tile_days"] for row in related)
        q1_tile_days = sum(row["q1_animal_tile_days"] for row in related)
        q2_tile_days = sum(row["q2_animal_tile_days"] for row in related)
        observed_days = sum(row["observed_days_q2_to_d28"] for row in related)
        total_tile_days = q0_tile_days + q1_tile_days + q2_tile_days
        rows.append(
            {
                "group": label,
                "episodes": len(group),
                "mean_score": mean(row["score"] for row in group),
                "mean_opponent_score": mean(row["opponent_score"] for row in group),
                "mean_margin": mean(row["score_margin"] for row in group),
                "median_q1_step": median(
                    row["q1_unlock"]["step"] for row in group if row["q1_unlock"]
                ),
                "median_q2_step": median(
                    row["q2_unlock"]["step"] for row in group if row["q2_unlock"]
                ),
                "mean_final_hands": mean(row["final_hands"] for row in group),
                "mean_moves": mean(row["movement_actions_issued"] for row in group),
                "mean_move_share_active_pct": mean(
                    row["movement_share_of_active_unit_commands_pct"] for row in group
                ),
                "animal_escapes": sum(row["animal_escapes_total"] for row in group),
                "mean_final_crops": mean(row["final_crops_total"] for row in group),
                "mean_final_animals": mean(row["final_animals_total"] for row in group),
                "mean_q0_animals_q2_to_d28": round(q0_tile_days / observed_days, 2)
                if observed_days
                else 0.0,
                "mean_q1_animals_q2_to_d28": round(q1_tile_days / observed_days, 2)
                if observed_days
                else 0.0,
                "mean_q2_animals_q2_to_d28": round(q2_tile_days / observed_days, 2)
                if observed_days
                else 0.0,
                "q2_vs_q0_animal_pct": ratio(q2_tile_days, q0_tile_days),
                "q2_share_of_3q_animal_pct": ratio(q2_tile_days, total_tile_days),
                "mean_q2_d28_animals": mean(row["q2_d28_animals"] for row in related),
                "mean_q2_d29_animals": mean(row["q2_d29_animals"] for row in related),
            }
        )
    q2_ratios = [
        float(by_episode[row["episode_id"]]["q2_vs_q0_animal_pct"] or 0.0)
        for row in owner_summaries
    ]
    scores = [float(row["score"]) for row in owner_summaries]
    margins = [float(row["score_margin"]) for row in owner_summaries]
    return {
        "groups": rows,
        "correlations_observational": {
            "q2_vs_q0_animal_pct_vs_score": pearson(q2_ratios, scores),
            "q2_vs_q0_animal_pct_vs_margin": pearson(q2_ratios, margins),
        },
    }


def format_number(value: float | None) -> str:
    if value is None:
        return "—"
    if isinstance(value, float) and not value.is_integer():
        return f"{value:,.2f}"
    return f"{int(value):,}"


def format_pct(value: float | None) -> str:
    return "—" if value is None else f"{float(value):.1f}%"


def format_unlock(event: dict[str, Any] | None) -> str:
    if not event:
        return "—"
    return f"D{event['day']}:H{event['hour']:02d}"


def build_markdown(metrics: dict[str, Any]) -> str:
    owner = metrics["owner_summaries"]
    livestock_by_episode = {
        row["episode_id"]: row for row in metrics["owner_q2_livestock"]
    }
    aggregate = metrics["owner_aggregate"]
    aggregate_rows = {row["group"]: row for row in aggregate["groups"]}
    all_row = aggregate_rows["ALL"]
    win_row = aggregate_rows["WIN"]
    loss_row = aggregate_rows["LOSS"]
    lines = [
        "# E17 — benchmark esterno della submission Codex reattiva",
        "",
        "## Verdetto sintetico",
        "",
        (
            f"Il corpus contiene **{len(owner)} episodi esterni unici**, bilanciati in "
            f"**{win_row['episodes']} vittorie e {loss_row['episodes']} sconfitte**. "
            f"Lo score medio osservato è **{format_number(all_row['mean_score'])}**; "
            f"la media delle sconfitte (**{format_number(loss_row['mean_score'])}**) supera "
            f"quella delle vittorie (**{format_number(win_row['mean_score'])}**), quindi "
            "lo score assoluto non è una misura autonoma di qualità strategica: forza e "
            "interazione dell'avversario sono confondenti rilevanti."
        ),
        "",
        (
            "La candidata mantiene una zootecnia Q2 intermedia: tra lo sblocco "
            f"di Q2 e D28, Q2 vale **{format_pct(all_row['q2_vs_q0_animal_pct'])}** "
            "degli animal-tile-days di Q0. È sotto tetsuya, sopra Crop Dusta e molto "
            "sopra OceanMix: non esiste quindi un'unica quota vincente, ma una leva "
            "causale da sottoporre ad ablation."
        ),
        "",
        (
            "Gli hash completi mostrano **una sola sequenza di comandi richiesta** "
            "nei dieci replay, a fronte di "
            f"**{metrics['validation']['unique_owner_structural_trajectories']} traiettorie "
            "strutturali eseguite**; la traiettoria dominante ricorre in "
            f"{metrics['validation']['dominant_owner_structural_trajectory_count']}/10 "
            "episodi. Le guardie non hanno quindi prodotto una divergenza osservabile "
            "dell'action stream in questo campione, ma ciò non prova che la policy non "
            "possa reagire in altri stati."
        ),
        "",
        "## Protocollo e limiti epistemici",
        "",
        "- corpus: replay Kaggle della submission reattiva, ruolo `EXTERNAL_DIAGNOSTIC`;",
        "- clock: giorni e ore zero-based del replay; D29 è separato perché può includere liquidazione terminale;",
        "- stato di farm, tile, denaro, hands e sblocchi: `OBSERVED/EXECUTED_STATE`;",
        "- azioni presenti nel replay: `REQUESTED`, non prova automatica dell'esecuzione;",
        "- fughe: `DERIVED` col criterio EOD stretto condiviso col benchmark Top-3;",
        "- correlazioni e differenze W/L: osservazionali, non effetti causali identificati.",
        "",
        "## Risultati per episodio — Pietro Valocchi",
        "",
        "| Episodio | Esito | Score | Avversario | Score avv. | Margine | Q1 | Q2 | Hands | Move/attive | Fughe | Crop finali | Animali finali |",
        "|---:|---|---:|---|---:|---:|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in owner:
        lines.append(
            f"| {row['episode_id']} | {row['result']} | {format_number(row['score'])} | "
            f"{row['opponent_name']} | {format_number(row['opponent_score'])} | "
            f"{format_number(row['score_margin'])} | {format_unlock(row['q1_unlock'])} | "
            f"{format_unlock(row['q2_unlock'])} | {row['final_hands']} | "
            f"{format_pct(row['movement_share_of_active_unit_commands_pct'])} | "
            f"{row['animal_escapes_total']} | {row['final_crops_total']} | "
            f"{row['final_animals_total']} |"
        )

    lines.extend(
        [
            "",
            "## Confronto vittorie e sconfitte",
            "",
            "| Gruppo | N | Score medio | Score avv. | Margine | Q1 mediano (step) | Q2 mediano (step) | Hands | Move/attive | Fughe | Animali Q0/Q1/Q2 da Q2 a D28 | Q2/Q0 |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|",
        ]
    )
    for label in ("ALL", "WIN", "LOSS"):
        row = aggregate_rows[label]
        lines.append(
            f"| {label} | {row['episodes']} | {format_number(row['mean_score'])} | "
            f"{format_number(row['mean_opponent_score'])} | {format_number(row['mean_margin'])} | "
            f"{format_number(row['median_q1_step'])} | {format_number(row['median_q2_step'])} | "
            f"{format_number(row['mean_final_hands'])} | "
            f"{format_pct(row['mean_move_share_active_pct'])} | {row['animal_escapes']} | "
            f"{row['mean_q0_animals_q2_to_d28']:.2f}/"
            f"{row['mean_q1_animals_q2_to_d28']:.2f}/"
            f"{row['mean_q2_animals_q2_to_d28']:.2f} | "
            f"{format_pct(row['q2_vs_q0_animal_pct'])} |"
        )

    lines.extend(
        [
            "",
            "## Quota allevamento Q2 per episodio",
            "",
            "Le medie coprono ogni giorno dallo sblocco Q2 a D28 incluso. `D28→D29` rende visibile l'eventuale liquidazione terminale.",
            "",
            "| Episodio | Esito | Animali medi Q0/Q1/Q2 | Q2/Q0 | Quota Q2 sul totale | Q2 D28→D29 | Crop Q2 D28→D29 | Specie Q2 D28 G/C/S |",
            "|---:|---|---|---:|---:|---:|---:|---|",
        ]
    )
    for summary in owner:
        row = livestock_by_episode[summary["episode_id"]]
        lines.append(
            f"| {summary['episode_id']} | {summary['result']} | "
            f"{row['mean_q0_animals']:.2f}/{row['mean_q1_animals']:.2f}/{row['mean_q2_animals']:.2f} | "
            f"{format_pct(row['q2_vs_q0_animal_pct'])} | "
            f"{format_pct(row['q2_share_of_3q_animal_pct'])} | "
            f"{row['q2_d28_animals']}→{row['q2_d29_animals']} | "
            f"{row['q2_d28_crops']}→{row['q2_d29_crops']} | "
            f"{row['q2_d28_goose']}/{row['q2_d28_cow']}/{row['q2_d28_sheep']} |"
        )

    lines.extend(
        [
            "",
            "## Confronto con gli archetipi Top-3",
            "",
            "Il confronto usa la stessa finestra, lo stesso parser e le stesse definizioni, ma corpus e avversari diversi.",
            "",
            "| Agente | Corpus | Episodi | Animali medi Q0/Q1/Q2 | Q2/Q0 | Quota Q2 sul totale 3Q |",
            "|---|---|---:|---|---:|---:|",
            (
                f"| Codex reattivo | external diagnostic | {all_row['episodes']} | "
                f"{all_row['mean_q0_animals_q2_to_d28']:.2f}/"
                f"{all_row['mean_q1_animals_q2_to_d28']:.2f}/"
                f"{all_row['mean_q2_animals_q2_to_d28']:.2f} | "
                f"{format_pct(all_row['q2_vs_q0_animal_pct'])} | "
                f"{format_pct(all_row['q2_share_of_3q_animal_pct'])} |"
            ),
        ]
    )
    for row in metrics["top3_livestock_reference"]:
        lines.append(
            f"| {row['agent']} | Top-3 discovery | {row['episodes']} | "
            f"{row['mean_q0_animals']:.2f}/{row['mean_q1_animals']:.2f}/{row['mean_q2_animals']:.2f} | "
            f"{format_pct(row['q2_vs_q0_animal_pct'])} | "
            f"{format_pct(row['q2_share_of_3q_animal_pct'])} |"
        )

    correlations = aggregate["correlations_observational"]
    lines.extend(
        [
            "",
            "## Lettura per E17.2",
            "",
            (
                f"- `DERIVED`: correlazione esplorativa Q2/Q0–score = "
                f"**{correlations['q2_vs_q0_animal_pct_vs_score']}**; Q2/Q0–margine = "
                f"**{correlations['q2_vs_q0_animal_pct_vs_margin']}**. Con N=10 e "
                "avversari diversi e nove profili Q2 identici, il coefficiente non è "
                "interpretabile come segnale causale."
            ),
            (
                f"- `OBSERVED/DERIVED`: sono state rilevate "
                f"**{all_row['animal_escapes']} fughe**; qualunque riduzione di Q2 deve "
                "conservare il gate assoluto di zero fughe."
            ),
            "- `HYPOTHESIS`: una Q2 zootecnica pari a circa due terzi di Q0 può sottrarre tile, servicing e movimento a colture o liquidità senza produrre un ritorno marginale equivalente.",
            "- `HYPOTHESIS`: l'effetto può dipendere dal timing Q2 e dalla contesa; ridurre Q2 non va confuso con ritardare Q2.",
            "",
            "### Ablation raccomandata",
            "",
            "Congelare tutto salvo il cap zootecnico di Q2 e confrontare livelli preregistrati `0%`, `~40%`, `~63%` (controllo attuale) e `~75%` di Q0. Mantenere invariati timing Q2, workforce, specie, liquidazione e guardie reattive. Misurare denaro, margine, animal/crop tile-days per quadrante, move/produttive, ordini falliti e fughe su seed development seat-balanced; usare i replay esterni solo per formulare l'ipotesi, non per selezionare retroattivamente il vincitore.",
            "",
            "## Artefatti riproducibili",
            "",
            "- `experiments/e17/artifacts/discovery/codex/E17_REACTIVE_EXTERNAL_REPLAY_METRICS.json`;",
            "- `experiments/e17/artifacts/discovery/codex/E17_REACTIVE_EXTERNAL_PARTICIPANTS.csv`;",
            "- `experiments/e17/artifacts/discovery/codex/E17_REACTIVE_EXTERNAL_Q2_LIVESTOCK.csv`;",
            "- `experiments/e17/artifacts/discovery/codex/E17_REACTIVE_EXTERNAL_DAILY_TIMELINE.csv`;",
            "- `experiments/e17/artifacts/discovery/codex/E17_REACTIVE_EXTERNAL_ESCAPE_EVENTS.csv`;",
            "- `experiments/e17/tools/codex/analyze_reactive_external_replays.py`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    provenance: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    daily_rows: list[dict[str, Any]] = []
    escape_events: list[dict[str, Any]] = []

    for episode_id in EPISODE_IDS:
        path = REPLAY_DIR / f"{episode_id}.json"
        if not path.exists():
            replay_url = (
                "https://www.kaggle.com/competitions/episodes/"
                f"{episode_id}/replay.json"
            )
            raise FileNotFoundError(
                f"{path} is a non-versioned diagnostic cache; "
                f"download it from {replay_url}"
            )
        with path.open(encoding="utf-8") as handle:
            raw = json.load(handle)
        info = raw.get("info") or {}
        names = list(info.get("TeamNames") or [])
        rewards = [int(value) for value in (raw.get("rewards") or [])]
        statuses = list(raw.get("statuses") or [])
        steps = raw.get("steps") or []
        if int(info.get("EpisodeId")) != episode_id:
            raise ValueError(f"EpisodeId mismatch in {path}")
        if len(names) != 2 or names.count(OWNER_NAME) != 1:
            raise ValueError(f"Expected one {OWNER_NAME!r} seat in {path}: {names}")
        if len(rewards) != 2 or statuses != ["DONE", "DONE"] or len(steps) != 720:
            raise ValueError(f"Invalid terminal replay structure in {path}")
        owner_player_id = names.index(OWNER_NAME)
        trajectory_fingerprints = owner_trajectory_fingerprints(raw, owner_player_id)
        provenance.append(
            {
                "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256_file(path),
                "episode_id": episode_id,
                "seed": int(info.get("seed")),
                "agents": names,
                "rewards": rewards,
                "statuses": statuses,
                "steps": len(steps),
                "schema_version": raw.get("schema_version"),
                "module_version": raw.get("module_version"),
                **trajectory_fingerprints,
            }
        )
        for player_id, player_name in enumerate(names):
            summary, player_daily, player_escapes = base.analyze_player(
                raw,
                episode_id=episode_id,
                seed=int(info.get("seed")),
                player_id=player_id,
                player_name=player_name,
                opponent_name=names[1 - player_id],
                score=rewards[player_id],
                opponent_score=rewards[1 - player_id],
            )
            summaries.append(summary)
            daily_rows.extend(player_daily)
            escape_events.extend(player_escapes)

    summaries.sort(key=lambda row: (row["episode_id"], row["player_id"]))
    daily_rows.sort(
        key=lambda row: (
            row["episode_id"],
            row["player_id"],
            row["day"],
            row["quadrant_slot"],
        )
    )
    owner_summaries = [row for row in summaries if row["player_name"] == OWNER_NAME]
    owner_daily = [row for row in daily_rows if row["player_name"] == OWNER_NAME]
    owner_escapes = [row for row in escape_events if row["player_name"] == OWNER_NAME]
    livestock = [
        quadrant_livestock_profile(summary, owner_daily) for summary in owner_summaries
    ]
    top3_reference = top3_livestock_reference()
    structural_fingerprint_counts = Counter(
        row["executed_structural_trajectory_sha256"] for row in provenance
    )
    metrics = {
        "schema": "e17_codex_reactive_external_benchmark.v1",
        "role": "EXTERNAL_DIAGNOSTIC_OBSERVATIONAL",
        "submission_id": 559631298,
        "candidate": "CODEX-E17.1-3Q-REACTIVE-GUARDED-V1",
        "owner_name": OWNER_NAME,
        "method": {
            "parser": "shared E17 Top-3 forensic parser",
            "requested_vs_executed": "actions=requested; farm snapshots=executed state",
            "action_fingerprint": "canonical SHA-256 of the 720 requested action payloads",
            "structural_fingerprint": "canonical SHA-256 of farmer, hands, tiles and unlocks across 720 observed states; cash excluded",
            "q2_livestock_window": "Q2 unlock day through D28 inclusive; D29 reported separately",
            "quadrant_mapping": {
                slot: quadrant for slot, quadrant in base.QUADRANT_SLOTS
            },
            "escape": "DERIVED occupied at-risk tile to same empty structure across EOD",
        },
        "provenance": provenance,
        "owner_summaries": owner_summaries,
        "all_participant_summaries": summaries,
        "owner_q2_livestock": livestock,
        "owner_aggregate": aggregate_owner(owner_summaries, livestock),
        "top3_livestock_reference": top3_reference,
        "owner_escape_events": owner_escapes,
        "validation": {
            "episodes": len(provenance),
            "unique_episode_ids": len({row["episode_id"] for row in provenance}),
            "unique_seeds": len({row["seed"] for row in provenance}),
            "owner_seats": len(owner_summaries),
            "owner_wins": sum(row["result"] == "WIN" for row in owner_summaries),
            "owner_losses": sum(row["result"] == "LOSS" for row in owner_summaries),
            "owner_player0": sum(row["player_id"] == 0 for row in owner_summaries),
            "owner_player1": sum(row["player_id"] == 1 for row in owner_summaries),
            "all_terminal": all(
                row["statuses"] == ["DONE", "DONE"] for row in provenance
            ),
            "all_720_steps": all(row["steps"] == 720 for row in provenance),
            "unique_owner_action_streams": len(
                {row["requested_action_stream_sha256"] for row in provenance}
            ),
            "unique_owner_structural_trajectories": len(structural_fingerprint_counts),
            "dominant_owner_structural_trajectory_count": max(
                structural_fingerprint_counts.values(), default=0
            ),
        },
    }
    validation = metrics["validation"]
    expected = {
        "episodes": 10,
        "unique_episode_ids": 10,
        "unique_seeds": 10,
        "owner_seats": 10,
        "owner_wins": 5,
        "owner_losses": 5,
        "owner_player0": 5,
        "owner_player1": 5,
        "all_terminal": True,
        "all_720_steps": True,
    }
    if any(validation[key] != value for key, value in expected.items()):
        raise AssertionError(f"Corpus validation mismatch: {validation!r}")
    if len(top3_reference) != 3:
        raise AssertionError("Top-3 comparison artifacts are missing or incomplete")
    if any(not row["q1_unlock"] or not row["q2_unlock"] for row in owner_summaries):
        raise AssertionError("At least one owner replay did not reach 3Q")
    if any(row["final_cash_observed"] != row["score"] for row in owner_summaries):
        raise AssertionError("Final observed cash does not match replay reward")

    (OUT_DIR / "E17_REACTIVE_EXTERNAL_REPLAY_METRICS.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    base.write_csv(
        OUT_DIR / "E17_REACTIVE_EXTERNAL_PARTICIPANTS.csv",
        [base.scalar_summary_row(row) for row in summaries],
    )
    base.write_csv(OUT_DIR / "E17_REACTIVE_EXTERNAL_Q2_LIVESTOCK.csv", livestock)
    base.write_csv(OUT_DIR / "E17_REACTIVE_EXTERNAL_DAILY_TIMELINE.csv", owner_daily)
    base.write_csv(
        OUT_DIR / "E17_REACTIVE_EXTERNAL_ESCAPE_EVENTS.csv",
        owner_escapes,
        fieldnames=[
            "episode_id",
            "player_id",
            "player_name",
            "species",
            "quadrant_slot",
            "quadrant",
            "row",
            "col",
            "pre_eod_step",
            "eod_after_day",
            "pre_eod_hour",
            "structure_before",
            "animal_before",
            "consecutive_unfed_before",
            "fed_today_before",
            "feed_executed_before_pre_eod_snapshot",
            "pickup_executed_before_pre_eod_snapshot",
            "eod_feed_requests",
            "eod_pickup_requests",
            "first_observed_absent_day",
            "first_observed_absent_step",
            "structure_after",
            "animal_after",
            "evidence",
        ],
    )
    REPORT_PATH.write_text(build_markdown(metrics), encoding="utf-8")
    print(
        json.dumps(
            {
                "validation": validation,
                "aggregate": metrics["owner_aggregate"],
                "report": str(REPORT_PATH.relative_to(ROOT)).replace("\\", "/"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
