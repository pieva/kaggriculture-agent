"""Freeze all competitive completed episodes in the saved E20.9 history."""
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT/'docs/model_specs/codex/e22/reports/opponent_strategy_20260913'
RAW = ROOT/'data/replays/json/e22_opponents_20260913'
SID = 56202079


def main():
    history = json.loads((OUT/'history_56202079.json').read_text())
    teams = {t['id']:t['teamName'] for t in history['teams']}
    selected = [e for e in history['episodes'] if e['state']=='COMPLETED'
                and e['type']=='EPISODE_TYPE_PUBLIC' and len({a['teamId'] for a in e['agents']})==2]
    selected.sort(key=lambda e:(e['createTime'],e['id']))
    RAW.mkdir(parents=True,exist_ok=True)
    def fetch(e):
        p = RAW/f"{e['id']}.json"
        if not p.exists():
            response = requests.get(f"https://www.kaggle.com/competitions/episodes/{e['id']}/replay.json",timeout=45)
            response.raise_for_status()
            r = response.json()
            assert r['info']['EpisodeId']==e['id']
            p.write_bytes(response.content)
        raw = p.read_bytes();r=json.loads(raw)
        own=next(a for a in e['agents'] if a['submissionId']==SID)
        opp=next(a for a in e['agents'] if a['teamId']!=own['teamId'])
        seat=own.get('index',0)
        assert r['rewards'][seat]==own['reward'] and r['rewards'][1-seat]==opp['reward']
        result=dict(episode=e['id'],seat=seat,name=teams[opp['teamId']],opponent_submission=opp['submissionId'],
                    rating=opp['initialScore'],own_rating_before=own['initialScore'],own_rating_after=own['updatedScore'],
                    own_cash=own['reward'],opponent_cash=opp['reward'],margin=own['reward']-opp['reward'],
                    outcome='loss' if own['reward']<opp['reward'] else 'win' if own['reward']>opp['reward'] else 'draw',
                    complete=len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1]),
                    path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(raw).hexdigest())
        print(result['episode'],result['outcome'],ascii(result['name']),flush=True)
        return result
    with ThreadPoolExecutor(max_workers=3) as pool:
        games=list(pool.map(fetch,selected))
    (OUT/'COHORT.json').write_text(json.dumps(dict(acquired_utc=datetime.now(timezone.utc).isoformat(),submission=SID,
        protocol='All completed public non-self-play episodes in frozen history. Losses are focal, wins descriptive controls. No topology filtering. Ratings are opponent pre-match ratings, not current leaderboard ratings.',
        games=games),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
