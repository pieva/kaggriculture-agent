import json,sys,urllib.request,hashlib
from pathlib import Path
from collections import Counter
out=Path('docs/model_specs/codex/e19/artifacts/derived/new_top_screen_20260908');out.mkdir(parents=True,exist_ok=True)
for sid in sys.argv[1:]:
    p=out/f'{sid}.json'
    if not p.exists():p.write_bytes(urllib.request.urlopen(f'https://www.kaggle.com/competitions/episodes/{sid}/replay.json',timeout=60).read())
    r=json.loads(p.read_text(encoding='utf-8'))
    assert str(r['info']['EpisodeId'])==sid
    records=[]
    for seat,name in enumerate(r['info']['TeamNames']):
        ts=[]
        for day in range(15,31):
            s=r['steps'][min(day*24-1,len(r['steps'])-1)][seat]['observation']['farms'][seat]
            q=Counter()
            for y,row in enumerate(s['tiles']):
                for x,t in enumerate(row):
                    if isinstance(t,dict) and t.get('kind')=='PASTURE':q[(y//5)*2+x//5]+=1
            ts.append([q[i] for i in range(4)])
        records.append(dict(name=name,seat=seat,topology=ts[-1],stable770=sum(t==[7,7,0,0] for t in ts)))
    print(json.dumps(dict(episode=sid,profiles=records,info=r['info']),ensure_ascii=True))
