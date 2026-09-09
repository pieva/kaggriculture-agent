"""Download explicitly enumerated public replay IDs; preserve existing cache."""
import concurrent.futures
import json
import sys
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'data/replays/json/top_v51_20260909'
OUT.mkdir(parents=True,exist_ok=True)
def get(ep):
    p=OUT/f'{ep}.json'
    if not p.exists():
        raw=urllib.request.urlopen(f'https://www.kaggle.com/competitions/episodes/{ep}/replay.json',timeout=60).read()
        r=json.loads(raw)
        assert r['info']['EpisodeId']==ep
        p.write_bytes(raw)
    r=json.loads(p.read_text(encoding='utf-8'))
    assert r['info']['EpisodeId']==ep
    print(ep,json.dumps(r['info']['TeamNames'],ensure_ascii=True),r['rewards'],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(get,sorted({ep for g in json.loads((ROOT/'docs/model_specs/codex/e19/reports/top_v51_20260909/cohorts.json').read_text()) for ep in g['episodes']})))
