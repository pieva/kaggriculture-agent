"""Screen topology before full diagnostics; retain all selected episodes and provenance."""
import argparse
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path

from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import snapshot
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
from experiments.e18.tools.common.replay_daily_operational_kpi import daily_operational_kpi
from docs.model_specs.codex.e18.tools.e18_29_crop_service_audit import crop_service_audit

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[3]


def exact770(row):
    return row['pasture_topology']=={'Q0':7,'Q1':7,'Q2':0,'Q3':0} and row['unlocked_tiles']==75


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--episodes',nargs='+',type=int,required=True)
    parser.add_argument('--name',required=True)
    parser.add_argument('--label',required=True)
    parser.add_argument('--submission-id',type=int)
    parser.add_argument('--full',action='store_true')
    args=parser.parse_args()
    assert len(args.episodes)==len(set(args.episodes))
    profiles=[]
    for episode in args.episodes:
        path=ROOT/f'data/replays/json/{episode}.json'
        replay=json.loads(path.read_text(encoding='utf-8'))
        assert replay['info']['EpisodeId']==episode and len(replay['steps'])==720
        assert all(p['status']=='DONE' for p in replay['steps'][-1])
        names=[p['Name'] for p in replay['info']['Agents']]
        assert names.count(args.name)==1,'Exclude self-play and wrong identity'
        seat=names.index(args.name)
        days=[snapshot(replay,d,seat) for d in range(1,31)]
        row=dict(episode_id=episode,seat=seat,name=args.name,opponent=names[1-seat],
                 submission_id_from_browser_selection=args.submission_id,
                 seed=replay['configuration'].get('seed'),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                 bytes=path.stat().st_size,cache_path=str(path),
                 url=f'https://www.kaggle.com/competitions/episodes/{episode}/replay.json',
                 topology_daily=[dict(day=d['day'],pasture_topology=d['pasture_topology'],unlocked_tiles=d['unlocked_tiles']) for d in days],
                 exact770_final=exact770(days[-1]),exact770_d15_d30_share=sum(exact770(d) for d in days[14:])/16)
        if args.full:
            ledger=audit(replay,seat)
            assert ledger['cash_parity_errors']==0
            row.update(daily=days,ledger=ledger,terminal=end_state(replay,seat),
                       operational_daily=daily_operational_kpi(replay,seat,ledger),
                       crop_starvation=crop_service_audit(replay,seat),
                       reward=replay['steps'][-1][seat]['reward'],
                       opponent_reward=replay['steps'][-1][1-seat]['reward'],
                       statuses=[p['status'] for p in replay['steps'][-1]])
        profiles.append(row)
        print(json.dumps({k:row[k] for k in ('episode_id','name','opponent','exact770_final','exact770_d15_d30_share')},ensure_ascii=False),flush=True)
    output=BASE/f'artifacts/derived/E18_31_EXTERNAL_{args.label}.json'
    payload=dict(acquired_at_utc=datetime.now(timezone.utc).isoformat(),name=args.name,full_diagnostic=args.full,
                 selection='Recent competitive episodes selected in browser; no economic selection',
                 profiles=profiles,exposed=True,holdout=False,
                 stable_preliminary=(len(profiles)>=5 and sum(p['exact770_final'] for p in profiles)>=4 and
                     all(p['exact770_d15_d30_share']>=.8 for p in profiles if p['exact770_final'])))
    assert not output.exists(),'Use a fresh label; preserve frozen corpus'
    output.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(str(output),flush=True)


if __name__=='__main__':
    main()
