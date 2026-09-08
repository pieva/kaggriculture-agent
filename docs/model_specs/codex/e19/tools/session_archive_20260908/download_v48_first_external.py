import json,urllib.request,hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
out=Path('docs/model_specs/codex/e19/artifacts/derived/v48_external_20260908');out.mkdir(parents=True,exist_ok=True)
ids=[106836902,106835909,106834967,106834008,106833072,106832085,106831168,106830224]
def get(ep):
 p=out/f'{ep}.json'
 if not p.exists():p.write_bytes(urllib.request.urlopen(f'https://www.kaggle.com/competitions/episodes/{ep}/replay.json',timeout=60).read())
 r=json.loads(p.read_text(encoding='utf-8'));assert r['info']['EpisodeId']==ep
 seat=r['info']['TeamNames'].index('Pietro Valocchi')
 return dict(episode=ep,seat=seat,opponent=r['info']['TeamNames'][1-seat],cash=r['rewards'][seat],opponent_cash=r['rewards'][1-seat],statuses=r['statuses'],steps=len(r['steps']),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(get,ids))
result=dict(submission_id=56101593,rating_observed=822.1,observed_utc=datetime.now(timezone.utc).isoformat(),selection='All eight completed non-self matches visible at first inspection; no outcome filtering',games=rows)
(out/'first_cohort.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
