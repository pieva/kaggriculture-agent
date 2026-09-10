"""Frozen initial E20.1 public cohort selected from Kaggle's Games UI."""
import hashlib
import json
from pathlib import Path
import urllib.request
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parents[5]
IDS=[107467627,107466614,107465615,107463609,107464613,107462621,107461647,107460660,107459667,107458688,107457696,107456701,107455731,107454738,107453756,107452758,107451752,107450796,107449822,107448855,107447896,107446770]
RAW=ROOT/'data/replays/json/e20_1_first_20260910'
OUT=ROOT/'docs/model_specs/codex/e20/reports/external_first_20260910'

def acquire(ep):
    path=RAW/f'{ep}.json'
    url=f'https://www.kaggle.com/competitions/episodes/{ep}/replay.json'
    if not path.exists():path.write_bytes(urllib.request.urlopen(url,timeout=60).read())
    raw=path.read_bytes();r=json.loads(raw)
    assert r['info']['EpisodeId']==ep
    names=r['info']['TeamNames'];selfplay=names.count('Pietro Valocchi')==2
    seat=None if selfplay else names.index('Pietro Valocchi')
    return dict(episode=ep,seat=seat,selfplay=selfplay,teams=names,rewards=r['rewards'],
                statuses=r['statuses'],steps=len(r['steps']),seed=r['info']['seed'],
                raw_path=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),url=url)

if __name__=='__main__':
    RAW.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(acquire,IDS))
    cohort=dict(submission_id=56142698,rating_observed=944,observed_utc=datetime.now(timezone.utc).isoformat(),
                selection='All 22 completed episodes visible at initial inspection, newest 107467627; 21 competitive, one self-play retained separately. Jessica Jennifer in-progress excluded at cutoff. No outcome filtering.',games=rows)
    (OUT/'cohort.json').write_text(json.dumps(cohort,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
