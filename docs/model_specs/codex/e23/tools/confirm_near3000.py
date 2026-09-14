"""Separate three-game confirmation for the shortlisted recurring family."""
import hashlib
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from select_near3000 import OUT, RAW, dump, key
import requests

SHORTLIST=[56218385,56222223,56223630]


def main():
    frozen=OUT/'SHORTLIST_PROTOCOL.json'
    if not frozen.exists():
        dump(frozen,dict(frozen_utc=datetime.now(timezone.utc).isoformat(),submissions=SHORTLIST,
          selection='Three candidates with >=3/5 identical D20 structures, >=4/5 identical D20 crop maps, zero animal removals in initial five games. Validate on chronological ranks 6–8 from the already frozen histories. No selection by outcome.',
          questions=['Do the shared 17-pasture or 14-pasture/3-coop D20 configurations recur?',
                     'Do 33 strawberry and 25 wheat cells recur at D20?',
                     'Are there animal removals in confirmation?']))
    original=json.loads((OUT/'PROFILES.json').read_text(encoding='utf-8'))
    family_counts=Counter(key(g['daily'][19]['structures']) for g in original if g['submission'] in SHORTLIST)
    families=[k for k,n in family_counts.most_common() if n>=3]
    jobs=[]
    for sid in SHORTLIST:
        h=json.loads((OUT/f'history_{sid}.json').read_text(encoding='utf-8'))
        games=sorted([g for g in h['episodes'] if g['state']=='COMPLETED' and g['type']=='EPISODE_TYPE_PUBLIC' and len({a['teamId'] for a in g['agents']})==2],key=lambda g:(g['createTime'],g['id']),reverse=True)[5:8]
        assert len(games)==3
        for g in games:
            a=next(a for a in g['agents'] if a['submissionId']==sid)
            jobs.append(dict(submission=sid,episode=g['id'],seat=a.get('index',0)))
    assert not ({g['episode'] for g in jobs}&{g['episode'] for g in original})
    def fetch(eid):
        p=RAW/f'{eid}.json'
        if not p.exists():
            r=requests.get(f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json',timeout=60);r.raise_for_status();assert r.json()['info']['EpisodeId']==eid;p.write_bytes(r.content)
        print('CONFIRM_FETCH',eid,flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(fetch,sorted({g['episode'] for g in jobs})))
    results=[]
    for g in jobs:
        raw=(RAW/f'{g["episode"]}.json').read_bytes();r=json.loads(raw);seat=g['seat']
        assert len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1])
        obs=[s[seat]['observation'] for s in r['steps']];f=obs[479]['farms'][seat]
        cells=[dict(x=x,y=y,**t) for y,row in enumerate(f['tiles']) for x,t in enumerate(row) if isinstance(t,dict)]
        structures=[[t['x'],t['y'],t['kind']] for t in cells if t['kind'] in ('PASTURE','COOP')]
        removals=0
        for before,after in zip(obs,obs[1:]):
            for y,row in enumerate(before['farms'][seat]['tiles']):
                for x,t in enumerate(row):
                    if isinstance(t,dict) and t.get('animal'):
                        u=after['farms'][seat]['tiles'][y][x]
                        if not isinstance(u,dict) or u.get('animal')!=t['animal']:removals+=1
        results.append(dict(**g,sha256=hashlib.sha256(raw).hexdigest(),name=r['info']['TeamNames'][seat],
          family_matches=key(structures) in families,structures=structures,
          crops=dict(Counter(t['crop'] for t in cells if t.get('crop'))),
          mix=dict(Counter(t['animal'] for t in cells if t.get('animal'))),animal_removals=removals))
    dump(OUT/'CONFIRMATION.json',dict(families=[json.loads(f) for f in families],games=results))
    lines=['','## Conferma separata: tre replay precedenti per candidato','',
      'Candidati e criteri congelati prima di leggere i nove replay aggiuntivi. Nessun episodio condiviso con i 53 dello screening. Conferma descrittiva, non test economico appaiato.', '',
      '| Submission | Replay | Famiglia esatta già osservata | Mix D20 | Colture D20 | Rimozioni |','|---|---|---|---|---|---:|']
    for g in results:lines.append(f'| {g["submission"]} | {g["episode"]} | {g["family_matches"]} | {g["mix"]} | {g["crops"]} | {g["animal_removals"]} |')
    (OUT/'CONFIRMATION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('\n'.join(lines),flush=True)


if __name__=='__main__':main()
