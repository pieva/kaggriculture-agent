"""Read-only replay diagnosis: exact E18.28 shadow decisions, no policy tuning.

Browser downloads are inputs; only compact derived evidence is written. Local
opportunities are observed prerequisites, not additive realizable revenue.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from docs.model_specs.codex.e18.tools.e18_28_full_season_controller import (
    FullSeasonController, SHED_ACCESS,
)
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit, end_state
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import snapshot
from docs.model_specs.codex.e18.tools.e18_29_crop_service_audit import crop_service_audit
from experiments.e18.tools.common.replay_daily_operational_kpi import daily_operational_kpi

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[3]
PLAN = BASE / 'artifacts/derived/E18_28_FULL_SEASON_C_PLAN_V1.json'
OWNER = 'Pietro Valocchi'
MOVES = {'NORTH', 'SOUTH', 'EAST', 'WEST'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def commands(action, farm):
    action = action or {}
    hands = action.get('hands', [])
    return [action.get('farmer', ['PASS']), *[
        hands[i] if i < len(hands) else ['PASS'] for i in range(len(farm['hands']))
    ]]


def local_opportunities(tile, inventory, position):
    """Overlapping state flags; CARE is not proof of a monetizable bonus."""
    result = []
    if isinstance(tile, dict):
        if tile.get('kind') == 'PLANT' and not tile.get('watered_today'):
            result.append('WATER')
        if tile.get('yield_units', 0) > 0:
            result.append('HARVEST')
        if tile.get('animal'):
            if not tile.get('fed_today') and inventory.get('WHEAT', 0):
                result.append('FEED_WITH_CARRIED_WHEAT')
            if not tile.get('cared_today'):
                result.append('CARE')
            if tile.get('fertilizer_available'):
                result.append('COLLECT_FERTILIZER')
    if position in SHED_ACCESS and any(inventory.values()):
        result.append('DROP')
    return result


class PassTrace(FullSeasonController):
    """Observe inherited queue decisions without replacing any command."""

    def __init__(self, plan, seat):
        super().__init__(plan, seat)
        self.pass_events = []
        self.trace_step = 0
        self.block_attempts = []

    def _planned_or_recovery(self, row, farm, private, worker, key):
        command, emitted = super()._planned_or_recovery(row, farm, private, worker, key)
        if command == ['PASS']:
            self.block_attempts.append(row['opcode'])
        return command, emitted

    def _worker_command(self, day, turn, worker, farm, private):
        self.block_attempts = []
        result = super()._worker_command(day, turn, worker, farm, private)
        if result[0] != ['PASS']:
            return result
        key = (day, worker)
        pending = [r for r in self.routes.get(key, [])[self.cursors[key]:] if r['opcode'] != 'PASS']
        if not pending:
            reason = 'QUEUE_FINISHED'
        elif pending[0]['turn'] > turn:
            reason = 'WAIT_SCHEDULED_TURN'
        else:
            reason = 'BLOCKED_' + pending[0]['opcode']
        pos = self._position(farm, worker)
        inv = dict(self._inventory(private, worker))
        tile = self._tile(farm, pos) if pos is not None else None
        self.pass_events.append(dict(
            step=self.trace_step, day=day, turn=turn, worker=worker,
            position=pos, reason=reason, pending=len(pending),
            next_task=deepcopy(pending[0]) if pending else None,
            skipped_in_this_call=list(self.block_attempts),
            money=farm['money'], inventory=inv,
            shed_wheat=private.get('shed', {}).get('WHEAT', 0),
            local_opportunities=local_opportunities(tile, inv, pos),
            tile=deepcopy(tile),
        ))
        return result


def pass_summary(events):
    reasons = Counter(e['reason'] for e in events)
    by_worker = Counter(str(e['worker']) for e in events)
    local = Counter(op for e in events for op in e['local_opportunities'])
    unique = Counter(op for day, pos, op in {
        (e['day'], tuple(e['position']), op) for e in events for op in e['local_opportunities']
    })
    return dict(total=len(events), reasons=dict(reasons), by_worker=dict(by_worker),
                local_opportunity_slots=dict(local), unique_tile_days_by_op=dict(unique))


def analyze(path):
    replay = json.loads(path.read_text(encoding='utf-8'))
    episode = replay['info']['EpisodeId']
    assert str(episode) == path.stem
    names = replay['info']['TeamNames']
    assert names.count(OWNER) == 1
    assert len(replay['steps']) == 720
    assert all(r['status'] == 'DONE' for r in replay['steps'][-1])
    seat = names.index(OWNER)
    agent = PassTrace(json.loads(PLAN.read_text()), seat)
    errors = []
    action_daily = [Counter() for _ in range(30)]
    capacity_daily = [0] * 30
    for index in range(1, 720):
        obs = replay['steps'][index - 1][seat]['observation']
        recorded = replay['steps'][index][seat]['action']
        agent.trace_step = index
        predicted = agent(deepcopy(obs), replay['configuration'])
        if predicted != recorded:
            errors.append(dict(step=index, expected=recorded, shadow=predicted))
        farm = obs['farms'][seat]
        cmds = commands(recorded, farm)
        capacity_daily[obs['day']] += len(cmds)
        for cmd in cmds:
            op = cmd[0] if isinstance(cmd, list) and cmd else 'PASS'
            action_daily[obs['day']]['MOVE' if op in MOVES else op] += 1
    # Reject causal attribution if the shadow differs from the uploaded behavior.
    assert not errors, errors[:2]
    assert agent.error_count == 0
    assert sum(c['PASS'] for c in action_daily) == len(agent.pass_events)
    agent.finalize_metrics()
    ledger_error = None
    try:
        ledger = audit(replay, seat)
        other_ledger = audit(replay, 1 - seat)
    except AssertionError as exc:
        # A public JSON can lose dict insertion order, material when DROP hits
        # a full shed. Do not invent executed cash flows or discard the game.
        ledger_error = str(exc)
        ledger = other_ledger = None
    daily = [snapshot(replay, day, seat) for day in range(1, 31)]
    other_daily = [snapshot(replay, day, 1 - seat) for day in range(1, 31)]
    totals = Counter()
    for c in action_daily:
        totals.update(c)
    productive_unfinished = []
    for (day, worker), rows in agent.routes.items():
        pending = [r for r in rows[agent.cursors[(day, worker)]:] if r['opcode'] != 'PASS']
        if pending:
            productive_unfinished.append(dict(day=day, worker=worker, rows=pending))
    other_action_daily = [Counter() for _ in range(30)]
    other_capacity_daily = [0] * 30
    for index in range(1, 720):
        obs = replay['steps'][index-1][1-seat]['observation']
        cmds = commands(replay['steps'][index][1-seat]['action'], obs['farms'][1-seat])
        other_capacity_daily[obs['day']] += len(cmds)
        for cmd in cmds:
            op = cmd[0] if isinstance(cmd,list) and cmd else 'PASS'
            other_action_daily[obs['day']]['MOVE' if op in MOVES else op] += 1
    windows = {}
    for lo, hi in ((1,6),(7,12),(13,15),(15,30),(16,24),(25,30)):
        events = [e for e in agent.pass_events if lo <= e['day'] <= hi]
        windows[f'D{lo:02d}_D{hi:02d}'] = pass_summary(events)
        windows[f'D{lo:02d}_D{hi:02d}']['capacity'] = sum(capacity_daily[lo-1:hi])
    source = dict(path=str(path.resolve()), bytes=path.stat().st_size, sha256=sha(path),
                  replay_url=f'https://www.kaggle.com/competitions/episodes/{episode}/replay.json',
                  submission_id=56036993, episode_id=episode, seed=replay['info'].get('seed'))
    result = dict(source=source, seat=seat, opponent=names[1-seat],
                  result='LOSS' if replay['rewards'][seat] < replay['rewards'][1-seat] else
                         'WIN' if replay['rewards'][seat] > replay['rewards'][1-seat] else 'DRAW',
                  reward=replay['rewards'][seat], opponent_reward=replay['rewards'][1-seat],
                  shadow_parity_batches=719, shadow_errors=errors,
                  daily=daily, operational_daily=daily_operational_kpi(replay,seat,ledger) if ledger else None,
                  capacity_daily=capacity_daily, action_daily=action_daily, totals=dict(totals),
                  ledger=ledger, ledger_error=ledger_error, terminal=end_state(replay,seat),
                  crop_starvation=crop_service_audit(replay,seat),
                  opponent_daily=other_daily, opponent_ledger=other_ledger,
                  opponent_action_daily=other_action_daily, opponent_capacity_daily=other_capacity_daily,
                  pass_summary=pass_summary(agent.pass_events), pass_windows=windows,
                  pass_daily=[pass_summary([e for e in agent.pass_events if e['day']==d]) for d in range(1,31)],
                  pass_events=agent.pass_events,
                  unfinished_by_day=agent.unfinished_by_day,
                  productive_unfinished=productive_unfinished,
                  skipped_stale=dict(agent.skipped_stale), recovery=dict(agent.recovery_actions))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', nargs='+', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for path in args.paths:
        output = args.output / f'{path.stem}.json'
        if output.exists():
            previous = json.loads(output.read_text())
            assert previous['source']['sha256'] == sha(path)
            print(f'{path.stem}: cached', flush=True)
            continue
        result = analyze(path)
        result['analyzed_at_utc'] = datetime.now(timezone.utc).isoformat()
        result['analyzer_sha256'] = sha(Path(__file__))
        result['plan_sha256'] = sha(PLAN)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({k:result[k] for k in ('opponent','result','reward','opponent_reward','shadow_parity_batches')} |
                         {'episode':path.stem,'pass':result['pass_summary']['total'],
                          'causes':result['pass_summary']['reasons']}), flush=True)


if __name__ == '__main__':
    main()
