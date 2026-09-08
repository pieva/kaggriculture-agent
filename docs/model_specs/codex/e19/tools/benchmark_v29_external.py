"""Frozen first external V29 cohort: replay-derived paired KPI, no policy changes."""
import json
import hashlib
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit, end_state
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import snapshot
from docs.model_specs.codex.e18.tools.e18_29_crop_service_audit import crop_service_audit
from experiments.e18.tools.common.replay_daily_operational_kpi import daily_operational_kpi

BASE = ROOT / 'docs/model_specs/codex/e19'
RAW = BASE / 'artifacts/derived/v29_external_20260908'
OUT = BASE / 'reports/v29_external_20260908'
IDS = [106724977,106724031,106723054,106721187,106722120,106720197,106719245,106718139,106718295,106717343,106716406]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for episode in IDS:
        path = RAW / f'{episode}.json'
        r = json.loads(path.read_text(encoding='utf-8'))
        names = r['info']['TeamNames']
        assert names.count('Pietro Valocchi') == 1
        assert len(r['steps']) == 720 and r['statuses'] == ['DONE', 'DONE']
        seat = names.index('Pietro Valocchi')
        item = dict(episode_id=episode, names=names, seat=seat, rewards=r['rewards'], seed=r['info']['seed'], sha256=hashlib.sha256(path.read_bytes()).hexdigest(), sides={})
        for label, s in [('candidate', seat), ('opponent', 1-seat)]:
            ledger = audit(r, s)
            item['sides'][label] = dict(daily=[snapshot(r,d,s) for d in range(1,31)], ledger=ledger, terminal=end_state(r,s), crop_starvation=crop_service_audit(r,s), operational_daily=daily_operational_kpi(r,s,ledger))
        records.append(item)
        print(episode, names, r['rewards'], flush=True)
    (OUT / 'profiles.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
