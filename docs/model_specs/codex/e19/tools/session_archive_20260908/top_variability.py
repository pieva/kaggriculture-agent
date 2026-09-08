import json
from pathlib import Path
from collections import Counter
p=Path('docs/model_specs/codex/e19/artifacts/derived/new_top_screen_20260908')
out=[]
for path in sorted(p.glob('1*.json')):
 r=json.loads(path.read_text(encoding='utf-8'))
 for seat,name in enumerate(r['info']['TeamNames']):
  if name not in ['SpaTaro','Otter Vibe','binghua','Matthew Huang','Suliman Tadros','carbonapi','kwa','Tarang222','THUNDER THUNDER']:continue
  days=[]
  for d in range(1,31):
   obs=r['steps'][min(d*24-1,719)][seat]['observation']; f=obs['farms'][seat];q=Counter();a=Counter();plots=[]
   for y,row in enumerate(f['tiles']):
    for x,t in enumerate(row):
     if isinstance(t,dict):
      if t.get('kind')=='PASTURE':q[(y//5)*2+x//5]+=1;plots.append([x,y])
      if t.get('animal'):a[t['animal']]+=1
   days.append(dict(d=d,q=[q[i] for i in range(4)],animals=dict(a),plots=plots))
  changes=[days[0]]+[z for prev,z in zip(days,days[1:]) if z['q']!=prev['q']]
  out.append(dict(episode=int(path.stem),name=name,changes=[{k:v for k,v in z.items() if k!='plots'} for z in changes],unique_D15_D25=len(set(tuple(z['q']) for z in days[14:25])),q15=days[14]['q'],q25=days[24]['q'],q30=days[29]['q'],days=days))
(p/'variability.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
for x in out:
 if x['name'] in ['SpaTaro','Matthew Huang','Suliman Tadros','Otter Vibe']:
  print(json.dumps({k:v for k,v in x.items() if k!='days'}))
