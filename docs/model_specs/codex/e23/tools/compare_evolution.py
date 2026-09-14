"""Descriptive coordinate and calendar deltas; no simulations or policy changes."""
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
OTHER=Path('C:/Users/pietr/.codex/worktrees/756c/kaggriculture-agent')
OUT=ROOT/'docs/model_specs/codex/e23/reports/evolution_delta_20260914'


def profile(path,seat):
    r=json.loads(path.read_text());obs=[s[seat]['observation'] for s in r['steps']]
    placements=[];starts=[];services=Counter();hires=Counter()
    for i in range(1,720):
        b,a=obs[i-1:i+1];action=r['steps'][i][seat]['action'];day=b['day']+1
        f=b['farms'][seat]
        for pos,cmd in zip([f['farmer']]+f['hands'],[action['farmer']]+action['hands']):
            x,y=pos;t=f['tiles'][y][x]
            if isinstance(t,dict) and t.get('animal') and cmd and cmd[0] in ['FEED','CARE','HARVEST','COLLECT_FERTILIZER']:
                services[t['animal']+' '+cmd[0]]+=1
        for y,row in enumerate(a['farms'][seat]['tiles']):
            for x,t in enumerate(row):
                old=b['farms'][seat]['tiles'][y][x];old=old if isinstance(old,dict) else {}
                if not isinstance(t,dict):continue
                if t.get('animal') and t['animal']!=old.get('animal'):
                    placements.append([x,y,t['animal'],day,b['hour']+1])
                if t.get('crop') and (t['crop'],t.get('planted_day'))!=(old.get('crop'),old.get('planted_day')) and t.get('planted_day')==b['day']:
                    starts.append([x,y,t['crop'],day,b['hour']+1])
    daily=[]
    for day in range(1,31):
        f=obs[day*24-1]['farms'][seat]
        crops=[[x,y,t['crop']] for y,row in enumerate(f['tiles']) for x,t in enumerate(row) if isinstance(t,dict) and t.get('crop')]
        daily.append(dict(day=day,hands=len(f['hands']),crops=crops))
    return dict(episode=r['info']['EpisodeId'],placements=placements,starts=starts,services=dict(services),daily=daily)


def main():
    OUT.mkdir(parents=True,exist_ok=True);profiles={}
    for label,tag in [('E22.1','external_e22_1_q2_grano_20260914'),('E22.2_parent','external_e22_2_fix_20260914')]:
        g=json.loads((OTHER/'docs/model_specs/codex/e23/reports'/tag/'COHORT.json').read_text())[0]
        profiles[label]=profile(OTHER/g['path'],g['seat'])
    cohort=json.loads((ROOT/'docs/model_specs/codex/e23/reports/near3000_20260914/COHORT.json').read_text(encoding='utf-8'))
    for label,eid in [('E23_geese8',108922213),('E23_geese9',108922490),('E23_sheep',108915255),('E23_sheep_D8',108921530)]:
        g=next(x for x in cohort if x['episode']==eid and x['submission'] in [56222223,56223630])
        profiles[label]=profile(ROOT/f'data/replays/json/e23_near3000_20260914/{eid}.json',g['seat'])
    (OUT/'PROFILES.json').write_text(json.dumps(profiles,indent=2),encoding='utf-8')
    lines=['# E23 — delta evolutivi rispetto alle due E22','',
        'Confronto descrittivo di replay rappresentativi. E23 indica ricette candidate osservate nelle submission 56222223 e 56223630, non bundle implementati. Coordinate zero-based; giorni e ore one-based. Nessuna stima causale di guadagno.', '',
        'E22.1 usa la versione Q2 Grano 56228842. La traiettoria E22.2 proviene dal parent fix 56228129: la versione corrente 56231638 coincide fino a D27 e aggiunge la successione Q2 Grano a D28–30. I delta tardivi del parent riportati sotto vanno interpretati tenendo conto di questa modifica già acquisita.', '']
    for base,target in [('E22.1','E23_geese8'),('E22.1','E23_geese9'),('E22.2_parent','E23_sheep'),('E22.2_parent','E23_sheep_D8')]:
        a,b=profiles[base],profiles[target]
        lines += [f'## {base} → {target}', '',f'Replay: {a["episode"]} → {b["episode"]}.', '',
                  '| Casella | Animale E22, collocamento | Animale candidato, collocamento |','|---|---|---|']
        aa={(p[0],p[1]):p for p in a['placements']};bb={(p[0],p[1]):p for p in b['placements']}
        for xy in sorted(aa.keys()|bb.keys()):
            x,y=aa.get(xy),bb.get(xy)
            if x!=y:
                def fmt(v):return f'{v[2]} D{v[3]} H{v[4]}' if v else 'assente'
                lines.append(f'| {xy} | {fmt(x)} | {fmt(y)} |')
        lines+=['','### Colture ai checkpoint','','| Giorno | Caselle differenti | Conteggi E22 | Conteggi candidato |','|---|---:|---|---|']
        for day in [12,20,22,25,28,29,30]:
            x={(c[0],c[1]):c[2] for c in a['daily'][day-1]['crops']};y={(c[0],c[1]):c[2] for c in b['daily'][day-1]['crops']}
            lines.append(f'| {day} | {sum(x.get(k)!=y.get(k) for k in x.keys()|y.keys())} | {dict(Counter(x.values()))} | {dict(Counter(y.values()))} |')
        lines+=['','### Comandi richiesti sulle caselle animali','','Sono richieste, non conteggi di servizi riusciti.','', '| Specie/servizio | E22 | Candidato |','|---|---:|---:|']
        for k in sorted(a['services'].keys()|b['services'].keys()):
            lines.append(f'| {k} | {a["services"].get(k,0)} | {b["services"].get(k,0)} |')
        handdiff=[(d+1,a['daily'][d]['hands'],b['daily'][d]['hands']) for d in range(30) if a['daily'][d]['hands']!=b['daily'][d]['hands']]
        lines+=['',f'Organico ai checkpoint differente (giorno, E22, candidato): {handdiff}.','']
    (OUT/'DETAILS.md').write_text('\n'.join(lines),encoding='utf-8')
    print('Wrote',OUT/'DETAILS.md')


if __name__=='__main__':main()
