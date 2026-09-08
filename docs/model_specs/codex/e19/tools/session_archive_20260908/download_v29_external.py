import concurrent.futures
import json
import urllib.request
from pathlib import Path

out = Path('docs/model_specs/codex/e19/artifacts/derived/v29_external_20260908')
ids = [106724977,106724031,106723054,106721187,106722120,106720197,106719245,106718139,106718295,106717343,106716406]
def get(i):
    p = out / f'{i}.json'
    if not p.exists():
        data = urllib.request.urlopen(f'https://www.kaggle.com/competitions/episodes/{i}/replay.json', timeout=60).read()
        r = json.loads(data)
        assert r['info']['EpisodeId'] == i
        p.write_bytes(data)
    r = json.loads(p.read_text(encoding='utf-8'))
    return [i, r['info']['TeamNames'], r['rewards'], len(r['steps'])]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    print(json.dumps(list(pool.map(get, ids)), indent=2))
