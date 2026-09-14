"""Freeze a fresh near-3000 cohort and screen recurring configurations."""
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
import requests

ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT/'docs/model_specs/codex/e23/reports/near3000_20260914'
RAW = ROOT/'data/replays/json/e23_near3000_20260914'
SELECTION = [
    ('HowardLeeTW',2995.4,56202668),('Orbital Terraformer',2991.9,56205640),
    ('redblackbst',2991.3,56221758),('Mengfei Li',2990.1,56173067),
    ('DSM',2987.4,56204618),('Unknown Mother-Goose',2984.3,56221927),
    ('Catalyst',2977.8,56218385),('Otter Vibe',2977.4,56097405),
    ('feel the agi',2970.1,56132899),('Thomas Tschinkel',2969.1,56222223),
    ('Deodims & Co',2950.5,56223630)]


def dump(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')


def key(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'))


def acquire():
    OUT.mkdir(parents=True,exist_ok=True); RAW.mkdir(parents=True,exist_ok=True)
    protocol = dict(frozen_utc=datetime.now(timezone.utc).isoformat(),
        selection='All eleven visible leaderboard teams with 2950 <= displayed score < 3000, ranks 5–15. IDs verified through each team game-history URL. Five latest completed public non-self-play games per exact submission; no outcome or geometry filtering.',
        source='https://www.kaggle.com/competitions/kaggriculture/leaderboard',
        selections=[dict(name=n,score=s,submission=i) for n,s,i in SELECTION])
    if not (OUT/'PROTOCOL.json').exists(): dump(OUT/'PROTOCOL.json',protocol)
    jobs=[]
    for name,score,sid in SELECTION:
        path=OUT/f'history_{sid}.json'
        if not path.exists():
            response=requests.post('https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes',json={'submissionId':sid},timeout=45)
            response.raise_for_status(); dump(path,response.json())
        history=json.loads(path.read_text(encoding='utf-8'))
        games=sorted([g for g in history['episodes'] if g['state']=='COMPLETED' and g['type']=='EPISODE_TYPE_PUBLIC' and len({a['teamId'] for a in g['agents']})==2],key=lambda g:(g['createTime'],g['id']),reverse=True)[:5]
        assert len(games)==5
        for game in games:
            agent=next(a for a in game['agents'] if a['submissionId']==sid)
            jobs.append(dict(name=name,score=score,submission=sid,episode=game['id'],seat=agent.get('index',0),metadata=game))
    def fetch(eid):
        path=RAW/f'{eid}.json'
        if not path.exists():
            r=requests.get(f'https://www.kaggle.com/competitions/episodes/{eid}/replay.json',timeout=60);r.raise_for_status()
            data=r.json();assert data['info']['EpisodeId']==eid
            path.write_bytes(r.content)
        print('FETCHED',eid,flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(fetch,sorted({g['episode'] for g in jobs})))
    dump(OUT/'COHORT.json',jobs)
    return jobs


def analyze(jobs):
    profiles=[]; streams={}
    for job in jobs:
        raw=(RAW/f'{job["episode"]}.json').read_bytes();r=json.loads(raw)
        assert len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1])
        assert r['info']['EpisodeId']==job['episode']
        seat=job['seat']; obs=[s[seat]['observation'] for s in r['steps']]
        daily=[];starts=[];previous_crop={};removals=[]
        for step in range(1,720):
            before,after=obs[step-1:step+1]
            for y,row in enumerate(after['farms'][seat]['tiles']):
                for x,tile in enumerate(row):
                    old=before['farms'][seat]['tiles'][y][x]
                    old=old if isinstance(old,dict) else {};tile=tile if isinstance(tile,dict) else {}
                    if old.get('crop'):previous_crop[x,y]=old['crop']
                    if old.get('animal') and tile.get('animal')!=old['animal']:
                        removals.append(dict(day=before['day']+1,x=x,y=y,animal=old['animal'],unfed=old.get('consecutive_unfed'),fed=old.get('fed_today')))
                    if tile.get('crop') and (tile['crop'],tile.get('planted_day'))!=(old.get('crop'),old.get('planted_day')) and tile.get('planted_day')==before['day']:
                        starts.append([before['day']+1,x,y,previous_crop.get((x,y)),tile['crop']])
        for day in range(1,31):
            o=obs[day*24-1];f=o['farms'][seat]
            cells=[dict(x=x,y=y,kind=t['kind'],animal=t.get('animal'),crop=t.get('crop')) for y,row in enumerate(f['tiles']) for x,t in enumerate(row) if isinstance(t,dict)]
            structures=[[t['x'],t['y'],t['kind']] for t in cells if t['kind'] in ('PASTURE','COOP')]
            animals=[[t['x'],t['y'],t['animal']] for t in cells if t['animal']]
            crops=[[t['x'],t['y'],t['crop']] for t in cells if t['crop']]
            daily.append(dict(day=day,structures=structures,animals=animals,crops=crops,
                quadrants=f['unlocked_quadrants'],money=f['money'],prices=o['market']['prices']))
        actions=[s[seat]['action'] for s in r['steps'][1:]]
        streams[job['submission'],job['episode']]=[key([a.get('farmer'),a.get('hands')]) for a in actions]
        profiles.append(dict(**job,sha256=hashlib.sha256(raw).hexdigest(),team_name=r['info']['TeamNames'][seat],
                             daily=daily,crop_starts=starts,animal_removals=removals))
        print('ANALYZED',job['submission'],job['episode'],flush=True)
    dump(OUT/'PROFILES.json',profiles)
    summary=[]
    for name,score,sid in SELECTION:
        games=[g for g in profiles if g['submission']==sid]
        modes={}
        for d in [12,20,25,29]:
            modes[d]={field:Counter(key(g['daily'][d-1][field]) for g in games).most_common(1)[0][1] for field in ['structures','animals','crops']}
        similarity=[]
        for lo,hi in [(0,264),(264,456),(456,719)]:
            similarity.append(mean(sum(a==b for a,b in zip(streams[sid,g['episode']][lo:hi],streams[sid,h['episode']][lo:hi]))/(hi-lo) for g,h in itertools.combinations(games,2)))
        crop_patterns=Counter()
        for g in games:crop_patterns.update(set(key(c) for c in g['crop_starts']))
        stable_starts=sum(n>=4 for n in crop_patterns.values())
        summary.append(dict(name=name,submission=sid,score=score,modes=modes,action_similarity=similarity,
                            animal_removals=sum(len(g['animal_removals']) for g in games),crop_starts_in_at_least4=stable_starts,
                            exact_crop_patterns=[dict(pattern=json.loads(k),n=n) for k,n in crop_patterns.items() if n>=4]))
    clusters=defaultdict(list)
    for g in profiles:
        clusters[key(g['daily'][19]['structures'])].append(dict(submission=g['submission'],episode=g['episode']))
    shared=sorted([dict(structures=json.loads(k),members=v,submissions=sorted({g['submission'] for g in v}),n=len(v)) for k,v in clusters.items()],key=lambda x:(len(x['submissions']),x['n']),reverse=True)
    dump(OUT/'SUMMARY.json',dict(submissions=summary,shared_d20_structures=shared))
    lines=['# E23 — nuovo gruppo 2950–3000','',
        'Selezione dalla classifica live del 14 settembre 2026: tutti gli undici team fra 2950 incluso e 3000 escluso, posizioni 5–15. Cinque ultimi replay pubblici competitivi per submission, senza selezione per vittoria o geometria. Score congelati alla selezione.', '',
        f'{len(profiles)} replay-lato, {len({g["episode"] for g in profiles})} episodi distinti. Integrità, identità e completezza verificate; questa selezione non ripete l’audit economico completo.', '',
        'Stabilità = numero di replay con la stessa configurazione esatta più frequente a D20, coordinate comprese. Le tre colonne possono riferirsi a gruppi diversi. Comandi = identità del batch di tutti i lavoratori, media delle dieci coppie per submission. Rimozioni = animali scomparsi/cambiati; non sono classificate come rotazione deliberata.', '',
        '| Team | Submission | Score | Strutture D20 | Animali D20 | Colture D20 | Comandi D1–11 / D12–19 / D20–30 | Rimozioni animali |',
        '|---|---|---:|---:|---:|---:|---|---:|']
    for s in summary:
        m=s['modes'][20]
        lines.append(f'| {s["name"]} | {s["submission"]} | {s["score"]} | {m["structures"]}/5 | {m["animals"]}/5 | {m["crops"]}/5 | '+ ' / '.join(f'{x:.1%}' for x in s['action_similarity'])+f' | {s["animal_removals"]} |')
    lines+=['','## Famiglie condivise fra submission','', 'Geometrie esatte delle strutture a D20; stesso impianto non significa stesso mix o stesso calendario.', '']
    for cluster in shared:
        if len(cluster['submissions'])<2:continue
        counts=Counter(x[2] for x in cluster['structures'])
        lines.append(f'- {dict(counts)}: {cluster["n"]} replay, {len(cluster["submissions"])} submission: '+', '.join(map(str,cluster['submissions']))+'.')
    lines+=['','Le ricorrenze costituiscono lo screening. Prima di replicare una famiglia, verificare successioni, tempi, economia e confermare su altri replay della stessa submission. Non assumere che una mappa finale copiata produca lo stesso risultato.','']
    (OUT/'REPORT.md').write_text('\n'.join(lines),encoding='utf-8')


if __name__=='__main__':
    analyze(acquire())
