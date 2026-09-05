#!/usr/bin/env python3
"""Build the 75-tile × 720-step E18.16 baseline trajectory matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from kaggle_environments import make

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agricola.strategy.codex.codex_e18_770_exact_cap_critical_feed import (
    create_codex_e18_770_exact_cap_critical_feed,
)

DEFAULT_JSON = (
    ROOT
    / "docs/model_specs/codex/e18/artifacts/derived/"
    / "E18_16_BASE_TRAJECTORY_MATRIX_S180903001_P0.json"
)
DEFAULT_SEED = 180903001
MOVE_DELTAS = {
    "NORTH": (0, -1),
    "SOUTH": (0, 1),
    "EAST": (1, 0),
    "WEST": (-1, 0),
}
ACTION_CODES = {
    "NORTH": "N",
    "SOUTH": "S",
    "EAST": "E",
    "WEST": "W",
    "PASS": "PA",
    "WATER": "WT",
    "HARVEST": "HV",
    "DIG": "DG",
    "FERTILIZE": "FZ",
    "BUILD_PASTURE": "BP",
    "BUILD_COOP": "BC",
    "FEED": "FD",
    "CARE": "CR",
    "COLLECT_FERTILIZER": "CF",
    "PICKUP": "PU",
    "DROP": "DP",
    "PLACE": "PL",
}
PLANT_CODES = {
    "WHEAT": "PW",
    "CARROT": "PC",
    "TOMATO": "PT",
    "STRAWBERRY": "PS",
    "MELON": "PM",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _positions(farm: dict[str, Any]) -> list[tuple[int, int]]:
    return [
        tuple(farm.get("farmer", [4, 4])),
        *(tuple(value) for value in farm.get("hands", []) or []),
    ]


def _unit_commands(action: dict[str, Any] | None) -> list[list[Any]]:
    action = action or {}
    return [
        action.get("farmer", ["PASS"]) or ["PASS"],
        *(action.get("hands", []) or []),
    ]


def _quadrant(x: int, y: int) -> str:
    return "Q0" if x < 5 and y < 5 else "Q1" if y < 5 else "Q2" if x < 5 else "Q3"


def _tiles() -> list[dict[str, Any]]:
    values = []
    for quadrant in ("Q0", "Q1", "Q2"):
        for y in range(10):
            for x in range(10):
                if _quadrant(x, y) != quadrant:
                    continue
                values.append(
                    {
                        "index": len(values),
                        "quadrant": quadrant,
                        "x": x,
                        "y": y,
                        "label": f"{quadrant} ({x},{y})",
                    }
                )
    if len(values) != 75:
        raise AssertionError(f"expected 75 tiles, found {len(values)}")
    return values


def _code(command: list[Any]) -> str:
    opcode = str(command[0]) if command else "PASS"
    if opcode == "PLANT" and len(command) > 1:
        return PLANT_CODES.get(str(command[1]), "PX")
    if opcode == "PLACE" and len(command) > 1:
        return f"L{str(command[1])[:1]}"
    return ACTION_CODES.get(opcode, opcode[:2])


def _event_payload(
    *,
    step: int,
    tile_index: int,
    unit: int,
    source: tuple[int, int],
    command: list[Any],
) -> list[Any]:
    opcode = str(command[0]) if command else "PASS"
    target = source
    if opcode in MOVE_DELTAS:
        dx, dy = MOVE_DELTAS[opcode]
        target = (source[0] + dx, source[1] + dy)
    return [
        step,
        tile_index,
        unit,
        _code(command),
        opcode,
        list(command[1:]),
        target[0],
        target[1],
    ]


def _run(seed: int, player: int) -> dict[str, Any]:
    policies = []
    controllers = []
    for seat in (0, 1):
        context = {
            "run_id": f"E18-16-BASE-TRAJECTORY-S{seed}-P{seat}",
            "episode_id": f"E18-16-BASE-TRAJECTORY-S{seed}-P{seat}",
            "seed": seed,
            "player_position": seat,
        }
        policy = create_codex_e18_770_exact_cap_critical_feed(
            run_context=context
        )
        policies.append(policy)
        controllers.append(
            policy.codex_e18_770_exact_cap_critical_feed_instance
        )
    env = make(
        "kaggriculture",
        configuration={
            "episodeSteps": 720,
            "seed": seed,
            "turnsPerDay": 24,
        },
        debug=False,
    )
    env.run(policies)
    if len(env.steps) != 720:
        raise AssertionError(f"expected 720 records, found {len(env.steps)}")

    tiles = _tiles()
    tile_lookup = {
        (int(tile["x"]), int(tile["y"])): int(tile["index"])
        for tile in tiles
    }
    events: list[list[Any]] = []
    action_counts: Counter[str] = Counter()
    code_counts: Counter[str] = Counter()
    off_matrix: Counter[str] = Counter()
    peak_hands = 0
    action_digest = hashlib.sha256()
    for record_index in range(1, len(env.steps)):
        action_step = record_index - 1
        before_record = env.steps[record_index - 1][player]
        record = env.steps[record_index][player]
        before_farm = before_record["observation"]["farms"][player]
        positions = _positions(before_farm)
        peak_hands = max(peak_hands, max(0, len(positions) - 1))
        action = record.get("action") or {}
        action_digest.update(
            json.dumps(action, sort_keys=True, separators=(",", ":")).encode(
                "utf-8"
            )
        )
        action_digest.update(b"\n")
        for unit, command in enumerate(_unit_commands(action)):
            if unit >= len(positions) or not command:
                continue
            source = positions[unit]
            opcode = str(command[0])
            action_counts[opcode] += 1
            code_counts[_code(command)] += 1
            tile_index = tile_lookup.get(source)
            if tile_index is None:
                off_matrix[opcode] += 1
                continue
            events.append(
                _event_payload(
                    step=action_step,
                    tile_index=tile_index,
                    unit=unit,
                    source=source,
                    command=command,
                )
            )

    telemetry = controllers[player].telemetry_snapshot()
    if peak_hands != 12:
        raise AssertionError(f"expected peak_hands=12, found {peak_hands}")
    if int(telemetry.get("error_count", 0) or 0) != 0:
        raise AssertionError("E18.16 emitted an internal error")
    return {
        "schema_version": "e18.codex.base_trajectory_matrix.v1",
        "candidate": "CODEX-E18.16-770-EXACT-CAP-CRITICAL-FEED-V1",
        "scenario": {
            "seed": seed,
            "player": player,
            "opponent": "E18.16_MIRROR",
            "records": 720,
            "action_steps": 719,
            "turns_per_day": 24,
            "days": 30,
            "included_quadrants": ["Q0", "Q1", "Q2"],
            "tile_count": 75,
            "peak_hands": peak_hands,
            "executing_unit_slots": peak_hands + 1,
        },
        "semantics": {
            "cell_position": "SOURCE_TILE_BEFORE_REQUESTED_ACTION",
            "farmer_unit": 0,
            "hand_slots": "1..12; slot identity resets with daily hiring",
            "event_fields": [
                "step",
                "tile_index",
                "unit",
                "code",
                "opcode",
                "arguments",
                "target_x",
                "target_y",
            ],
            "step_719": "terminal observation; no subsequent requested action",
            "off_matrix": "actions sourced in Q3 are counted but not projected into the 75-tile matrix",
        },
        "tiles": tiles,
        "events": events,
        "action_counts": dict(sorted(action_counts.items())),
        "code_counts": dict(sorted(code_counts.items())),
        "off_matrix_action_counts": dict(sorted(off_matrix.items())),
        "provenance": {
            "action_stream_sha256": action_digest.hexdigest().upper(),
            "source": "src/agricola/strategy/codex/codex_e18_770_exact_cap_critical_feed.py",
            "source_sha256": _sha256(
                ROOT
                / "src/agricola/strategy/codex/"
                / "codex_e18_770_exact_cap_critical_feed.py"
            ),
            "config": "docs/model_specs/codex/e18/configs/CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED_V1.json",
            "config_sha256": _sha256(
                ROOT
                / "docs/model_specs/codex/e18/configs/"
                / "CODEX_E18_16_770_EXACT_CAP_CRITICAL_FEED_V1.json"
            ),
        },
    }


def _html(payload: dict[str, Any]) -> str:
    data = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    return f'''<div id="trajectory-matrix-e1816">
  <h2>E18.16 · traiettorie base 75 × 720</h2>
  <div class="viz-controls">
    <label class="form-label" for="trajectory-day">Giorno
      <select class="form-select" id="trajectory-day"></select>
    </label>
    <label class="form-check form-switch">
      <input class="form-check-input" id="trajectory-pass" type="checkbox">
      <span class="form-check-label">Mostra PASS</span>
    </label>
  </div>
  <div class="matrix-meta text-small text-muted"></div>
  <canvas class="season-overview" role="img" aria-label="Matrice completa di 75 tile per 720 step"></canvas>
  <div class="season-axis text-small text-muted"><span>S0 · D1</span><span>S240 · D11</span><span>S480 · D21</span><span>S719 · D30</span></div>
  <div class="worker-legend" aria-label="Colori unità"></div>
  <div class="action-legend text-small" aria-label="Codici azione"></div>
  <div class="day-title" aria-live="polite"></div>
  <div class="table-responsive"><div class="day-matrix" role="grid" aria-label="Dettaglio giornaliero 75 tile per 24 step"></div></div>
  <div class="selection-detail text-small text-muted" aria-live="polite">Seleziona una cella colorata per il dettaglio.</div>
</div>

<style>
  #trajectory-matrix-e1816 {{ width: 100%; color: var(--foreground); }}
  #trajectory-matrix-e1816 h2 {{ margin-bottom: 0.75rem; }}
  #trajectory-matrix-e1816 .viz-controls {{ margin-bottom: 0.5rem; }}
  #trajectory-matrix-e1816 .matrix-meta {{ margin-bottom: 0.5rem; }}
  #trajectory-matrix-e1816 .season-overview {{ display: block; width: 100%; height: 390px; border: 1px solid var(--border); }}
  #trajectory-matrix-e1816 .season-axis {{ display: flex; justify-content: space-between; margin-top: 0.25rem; }}
  #trajectory-matrix-e1816 .worker-legend,
  #trajectory-matrix-e1816 .action-legend {{ display: flex; flex-wrap: wrap; gap: 0.35rem 0.7rem; margin-top: 0.75rem; }}
  #trajectory-matrix-e1816 .worker-key {{ display: inline-flex; align-items: center; gap: 0.25rem; white-space: nowrap; }}
  #trajectory-matrix-e1816 .worker-swatch {{ width: 0.75rem; height: 0.75rem; background: var(--wc); }}
  #trajectory-matrix-e1816 .day-title {{ margin: 1rem 0 0.4rem; font-weight: 500; }}
  #trajectory-matrix-e1816 .day-matrix {{ display: grid; grid-template-columns: 6.75rem repeat(24, 2rem); min-width: 54.75rem; align-items: stretch; }}
  #trajectory-matrix-e1816 .grid-head,
  #trajectory-matrix-e1816 .tile-label,
  #trajectory-matrix-e1816 .action-cell {{ min-height: 1.75rem; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid var(--border); border-right: 1px solid var(--border); }}
  #trajectory-matrix-e1816 .grid-head {{ color: var(--muted-foreground); }}
  #trajectory-matrix-e1816 .tile-label {{ justify-content: flex-start; padding-left: 0.35rem; white-space: nowrap; color: var(--muted-foreground); }}
  #trajectory-matrix-e1816 .tile-label.quadrant-start {{ border-top: 2px solid var(--foreground); }}
  #trajectory-matrix-e1816 .action-cell.quadrant-start {{ border-top: 2px solid var(--foreground); }}
  #trajectory-matrix-e1816 .event-code {{ width: 100%; min-height: 1.7rem; display: flex; align-items: center; justify-content: center; background: color-mix(in srgb, var(--wc) 24%, transparent); box-shadow: inset 3px 0 var(--wc); color: var(--foreground); font-weight: 500; }}
  #trajectory-matrix-e1816 .selection-detail {{ margin-top: 0.6rem; min-height: 1.25rem; }}
  #trajectory-matrix-e1816 .w0 {{ --wc: var(--foreground); }}
  #trajectory-matrix-e1816 .w1 {{ --wc: var(--viz-series-1); }}
  #trajectory-matrix-e1816 .w2 {{ --wc: var(--viz-series-2); }}
  #trajectory-matrix-e1816 .w3 {{ --wc: var(--viz-series-3); }}
  #trajectory-matrix-e1816 .w4 {{ --wc: var(--viz-series-4); }}
  #trajectory-matrix-e1816 .w5 {{ --wc: var(--viz-series-5); }}
  #trajectory-matrix-e1816 .w6 {{ --wc: var(--viz-series-6); }}
  #trajectory-matrix-e1816 .w7 {{ --wc: color-mix(in srgb, var(--viz-series-1) 58%, var(--foreground)); }}
  #trajectory-matrix-e1816 .w8 {{ --wc: color-mix(in srgb, var(--viz-series-2) 58%, var(--foreground)); }}
  #trajectory-matrix-e1816 .w9 {{ --wc: color-mix(in srgb, var(--viz-series-3) 58%, var(--foreground)); }}
  #trajectory-matrix-e1816 .w10 {{ --wc: color-mix(in srgb, var(--viz-series-4) 58%, var(--foreground)); }}
  #trajectory-matrix-e1816 .w11 {{ --wc: color-mix(in srgb, var(--viz-series-5) 58%, var(--foreground)); }}
  #trajectory-matrix-e1816 .w12 {{ --wc: color-mix(in srgb, var(--viz-series-6) 58%, var(--foreground)); }}
  @media (max-width: 480px) {{
    #trajectory-matrix-e1816 .season-overview {{ height: 300px; }}
    #trajectory-matrix-e1816 .season-axis span:nth-child(2),
    #trajectory-matrix-e1816 .season-axis span:nth-child(3) {{ display: none; }}
  }}
</style>

<script>
  (() => {{
    const root = document.getElementById('trajectory-matrix-e1816');
    if (!root) return;
    const data = {data};
    const daySelect = root.querySelector('#trajectory-day');
    const passToggle = root.querySelector('#trajectory-pass');
    const canvas = root.querySelector('.season-overview');
    const matrix = root.querySelector('.day-matrix');
    const dayTitle = root.querySelector('.day-title');
    const detail = root.querySelector('.selection-detail');
    const meta = root.querySelector('.matrix-meta');
    const workerLegend = root.querySelector('.worker-legend');
    const actionLegend = root.querySelector('.action-legend');
    let selectedDay = 1;

    const unitLabel = unit => unit === 0 ? 'Farmer' : `M${{String(unit).padStart(2, '0')}}`;
    const eventText = event => {{
      const [step, tileIndex, unit, code, opcode, args, tx, ty] = event;
      const tile = data.tiles[tileIndex];
      const suffix = args.length ? ` ${{args.join(' ')}}` : '';
      return `S${{step}} · D${{Math.floor(step / 24) + 1}} H${{step % 24}} · ${{tile.label}} · ${{unitLabel(unit)}} · ${{opcode}}${{suffix}} → (${{tx}},${{ty}})`;
    }};

    for (let day = 1; day <= 30; day += 1) {{
      const option = document.createElement('option');
      option.value = String(day);
      option.textContent = `D${{day}} · S${{(day - 1) * 24}}–${{Math.min(719, day * 24 - 1)}}`;
      daySelect.appendChild(option);
    }}
    const offMatrix = Object.values(data.off_matrix_action_counts).reduce((sum, value) => sum + value, 0);
    meta.textContent = `Seed ${{data.scenario.seed}} · player ${{data.scenario.player}} · E18.16 mirror · 12 slot hands + farmer · ${{data.events.length}} azioni richieste proiettate · ${{offMatrix}} originate in Q3 fuori matrice`;

    for (let unit = 0; unit <= 12; unit += 1) {{
      const key = document.createElement('span');
      key.className = `worker-key w${{unit}} text-small`;
      key.innerHTML = `<span class="worker-swatch" aria-hidden="true"></span>${{unitLabel(unit)}}`;
      workerLegend.appendChild(key);
    }}
    const codeLabels = [
      'N/S/E/W movimento', 'PA pass', 'WT water', 'HV harvest', 'DG dig',
      'PW/PC/PT/PS/PM plant', 'FD feed', 'CR care', 'CF fertilizer',
      'BP/BC build', 'PU pickup', 'DP drop', 'LC/LS/LG place'
    ];
    codeLabels.forEach(label => {{
      const span = document.createElement('span');
      span.textContent = label;
      actionLegend.appendChild(span);
    }});

    const eventMap = new Map();
    data.events.forEach(event => {{
      const key = `${{event[0]}}:${{event[1]}}`;
      if (!eventMap.has(key)) eventMap.set(key, []);
      eventMap.get(key).push(event);
    }});

    const colorFor = unit => {{
      const swatch = workerLegend.querySelector(`.w${{unit}} .worker-swatch`);
      return getComputedStyle(swatch).backgroundColor;
    }};

    const drawOverview = () => {{
      const rect = canvas.getBoundingClientRect();
      const ratio = window.devicePixelRatio || 1;
      canvas.width = Math.max(1, Math.round(rect.width * ratio));
      canvas.height = Math.max(1, Math.round(rect.height * ratio));
      const ctx = canvas.getContext('2d');
      ctx.scale(ratio, ratio);
      ctx.clearRect(0, 0, rect.width, rect.height);
      const cellW = rect.width / 720;
      const cellH = rect.height / 75;
      data.events.forEach(event => {{
        if (!passToggle.checked && event[4] === 'PASS') return;
        ctx.fillStyle = colorFor(event[2]);
        ctx.fillRect(event[0] * cellW, event[1] * cellH, Math.max(1, cellW), Math.max(1, cellH));
      }});
      const border = getComputedStyle(root).getPropertyValue('--border').trim();
      const foreground = getComputedStyle(root).getPropertyValue('--foreground').trim();
      ctx.strokeStyle = border;
      ctx.lineWidth = 1;
      for (let day = 1; day < 30; day += 1) {{
        const x = day * 24 * cellW;
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, rect.height); ctx.stroke();
      }}
      ctx.strokeStyle = foreground;
      [25, 50].forEach(row => {{
        const y = row * cellH;
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(rect.width, y); ctx.stroke();
      }});
      const x0 = (selectedDay - 1) * 24 * cellW;
      ctx.strokeStyle = foreground;
      ctx.lineWidth = 2;
      ctx.strokeRect(x0, 0, 24 * cellW, rect.height);
    }};

    const makeCell = (tile, step, events, quadrantStart) => {{
      const cell = document.createElement('div');
      cell.className = `action-cell${{quadrantStart ? ' quadrant-start' : ''}}`;
      const visible = (events || []).filter(event => passToggle.checked || event[4] !== 'PASS');
      if (!visible.length) return cell;
      const primary = visible[0];
      const button = document.createElement('button');
      button.type = 'button';
      button.className = `btn viz-tile event-code w${{primary[2]}}`;
      button.textContent = visible.length === 1 ? primary[3] : `${{primary[3]}}+${{visible.length - 1}}`;
      const description = visible.map(eventText).join(' | ');
      button.setAttribute('aria-label', description);
      button.setAttribute('data-tooltip', description);
      button.addEventListener('click', () => {{ detail.textContent = description; }});
      cell.appendChild(button);
      return cell;
    }};

    const renderDay = () => {{
      matrix.replaceChildren();
      const blank = document.createElement('div');
      blank.className = 'grid-head text-small';
      blank.textContent = 'Tile / ora';
      matrix.appendChild(blank);
      for (let hour = 0; hour < 24; hour += 1) {{
        const head = document.createElement('div');
        head.className = 'grid-head text-small tabular-nums';
        head.textContent = String(hour);
        matrix.appendChild(head);
      }}
      const firstStep = (selectedDay - 1) * 24;
      data.tiles.forEach((tile, tileIndex) => {{
        const quadrantStart = tileIndex === 0 || tileIndex === 25 || tileIndex === 50;
        const label = document.createElement('div');
        label.className = `tile-label text-small${{quadrantStart ? ' quadrant-start' : ''}}`;
        label.textContent = tile.label;
        matrix.appendChild(label);
        for (let hour = 0; hour < 24; hour += 1) {{
          const step = firstStep + hour;
          matrix.appendChild(makeCell(tile, step, eventMap.get(`${{step}}:${{tileIndex}}`), quadrantStart));
        }}
      }});
      dayTitle.textContent = `D${{selectedDay}} · step ${{firstStep}}–${{Math.min(719, firstStep + 23)}}`;
      detail.textContent = 'Seleziona una cella colorata per il dettaglio.';
      drawOverview();
    }};

    daySelect.addEventListener('change', () => {{ selectedDay = Number(daySelect.value); renderDay(); }});
    passToggle.addEventListener('change', renderDay);
    canvas.addEventListener('click', event => {{
      const rect = canvas.getBoundingClientRect();
      const step = Math.min(719, Math.max(0, Math.floor((event.clientX - rect.left) / rect.width * 720)));
      selectedDay = Math.floor(step / 24) + 1;
      daySelect.value = String(selectedDay);
      renderDay();
    }});
    new ResizeObserver(drawOverview).observe(canvas);
    renderDay();
  }})();
</script>
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--player", type=int, choices=(0, 1), default=0)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--html-output", type=Path, required=True)
    args = parser.parse_args()
    payload = _run(args.seed, args.player)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    args.html_output.parent.mkdir(parents=True, exist_ok=True)
    args.html_output.write_text(_html(payload), encoding="utf-8")
    print(f"wrote {args.json_output}")
    print(f"wrote {args.html_output}")
    print(json.dumps({
        "events": len(payload["events"]),
        "action_counts": payload["action_counts"],
        "off_matrix_action_counts": payload["off_matrix_action_counts"],
        "action_stream_sha256": payload["provenance"]["action_stream_sha256"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
