"""Screen cached public opponents and audit direct V51C–770 trajectories."""
import csv,hashlib,json,sys
from pathlib import Path
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from markdown_it import MarkdownIt
ROOT=Path(__file__).resolve().parents[5]
WORK=Path('C:/Users/pietr/.codex/worktrees/dd62/kaggriculture-agent')
OUT=ROOT/'docs/model_specs/codex/e19/reports/restart770_20260912'
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.analyze_first_external import profile
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def screen():
    rows=[];excluded=[];seen=set()
    for base in [ROOT,WORK]:
        for p in sorted((base/'data/replays/json').rglob('*.json')):
            r=read(p);eid=r.get('info',{}).get('EpisodeId');names=r.get('info',{}).get('TeamNames',[])
            if not eid or eid in seen or names.count('Pietro Valocchi')!=1:continue
            seen.add(eid);seat=1-names.index('Pietro Valocchi')
            if len(r.get('steps',[]))!=720 or r.get('statuses')!=['DONE','DONE']:
                excluded.append({'episode':eid,'reason':'incomplete'});continue
            daily=[]
            for day in range(1,31):
                f=r['steps'][min(day*24-1,719)][seat]['observation']['farms'][seat];counts=[0]*4
                for y,line in enumerate(f['tiles']):
                    for x,t in enumerate(line):
                        if isinstance(t,dict) and t.get('kind')=='PASTURE':counts[int(x>=5)+2*int(y>=5)]+=1
                daily.append(counts)
            rows.append(dict(episode=eid,opponent=names[seat],opponent_seat=seat,raw_path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),daily_topology=daily,production770=all(t==[7,7,0,0] for t in daily[14:25]),final770=daily[-1]==[7,7,0,0],rewards=r['rewards']))
            print('SCREEN',eid,flush=True)
    save(OUT/'SCREEN.json',dict(scope='All unique complete cached public replays with exactly one Pietro Valocchi in main and V51 worktree data/replays/json; not all historical submissions downloaded.',criterion='770 production: all daily D15-D25 checkpoints exactly 7,7,0,0; final D30 separately; no outcome filtering.',rows=rows,excluded=excluded))
def main():
    OUT.mkdir(exist_ok=True)
    if '--screen' in sys.argv:screen()
    data=read(OUT/'SCREEN.json');rows=data['rows']
    cohort=read(WORK/'docs/model_specs/codex/e19/reports/v51_external_20260909/cohort.json')
    v51={g['episode'] for g in cohort['games']}
    metadata={}
    for p in (ROOT/'docs/model_specs/codex/e21/reports/external_770_772_774_775').glob('history_*.json'):
        for e in read(p)['episodes']:metadata[e['id']]=e
    candidates=[r for r in rows if r['production770'] or r['final770']]
    for r in candidates:
        r['direct_v51']=r['episode'] in v51
        e=metadata.get(r['episode'],{})
        a=next((a for a in e.get('agents',[]) if a.get('index',0)==r['opponent_seat']),{})
        r['opponent_submission_id']=a.get('submissionId')
        r['opponent_rating_before']=a.get('initialScore')
    save(OUT/'CANDIDATES.json',candidates)
    profiles=[];errors=[]
    for g in candidates:
        if not g['direct_v51'] or not g['production770']:continue
        try:
            dest=OUT/f"profile_{g['episode']}.json"
            if dest.exists():s=read(dest)
            else:
                raw=Path(g['raw_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==g['sha256']
                r=json.loads(raw);seat=g['opponent_seat']
                s=dict(episode=g['episode'],opponent=g['opponent'],sha256=g['sha256'],candidate=profile(r,1-seat),external=profile(r,seat))
                for side in ('candidate','external'):
                    p=s[side];assert len(p['kpi'])==30 and p['ledger']['cash_parity_errors']==0
                    assert p['terminal']['cash']==p['reward']
                save(dest,s)
            profiles.append(s);print('PROFILE',g['episode'],flush=True)
        except Exception as exc:errors.append(dict(episode=g['episode'],error=repr(exc)));print('ERROR',errors[-1],flush=True)
    save(OUT/'AUDIT_ERRORS.json',errors)
    if profiles:
        with (OUT/'DAILY_KPI.csv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=['episode','opponent','side','day']+[k for k,_,_ in FIELDS]);writer.writeheader()
            for p in profiles:
                for side in ('candidate','external'):
                    for d,kpi in enumerate(p[side]['kpi'],1):writer.writerow(dict(episode=p['episode'],opponent=p['opponent'],side=side,day=d,**{k:kpi[k] for k,_,_ in FIELDS}))
        fig,axes=plt.subplots(6,4,figsize=(17,22),layout='constrained')
        fig.suptitle(f'V51C contro avversari 770 nella stessa partita · n={len(profiles)}\nMediana e intervallo interquartile · D15–D25 sempre 7-7-0',fontsize=16)
        for ax,(key,label,unit) in zip(axes.flat,FIELDS):
            for side,color,title in [('candidate','#216ec0','V51C'),('external','#c46222','Avversari 770')]:
                arr=np.array([[d[key] for d in p[side]['kpi']] for p in profiles]);ax.plot(range(1,31),np.median(arr,axis=0),label=title,color=color);ax.fill_between(range(1,31),np.quantile(arr,.25,axis=0),np.quantile(arr,.75,axis=0),color=color,alpha=.15)
            ax.set_title(label,fontsize=10);ax.set_ylabel(unit);ax.set_xlabel('Giorno');ax.grid(alpha=.2)
        for ax in list(axes.flat)[22:]:ax.axis('off')
        axes.flat[22].legend(*axes.flat[0].get_legend_handles_labels(),loc='center');fig.savefig(OUT/'DIRECT_V51_770_KPI22.png',dpi=110);plt.close(fig)
    counts=Counter(r['opponent'] for r in candidates if r['production770'])
    text=f'''# Base 770 e avversari esterni disponibili

**Base di riavvio: CODEX 770 V51C, submission 56124996.** Bundle recuperato dal commit 977d5e064f2ef9808b4cd03d41c1276ba94348af, SHA256 `43d5c6c3b70cf2940afaa83f3a243cba75e52f89db459d31ecb96187c4f13fda`. Copia identica in `submission/submission_codex_e19_770_v51_candidate.py`; provenienza completa in BASELINE.json.

V49F corregge l'assunzione improduttiva D2; V51C impegna percorsi completi e adegua le assunzioni residue a D29. Sviluppo: 6 casi, +345 cassa media contro V49F; validazione: 4 casi su due seed, +64,50, servizi invariati. Un seed peggiora: non è superiorità uniforme. V50 respinta. V48 submission 56101593 resta controllo storico. La scelta recupera miglioramenti verificati, non deriva dal confronto fra rating di coorti diverse.

## Screening

Esaminati **{len(rows)} replay unici completi** già scaricati con un nostro lato identificato, in questo checkout e nel worktree V51. Esclusi tecnici: {len(data['excluded'])}. Non è il censimento di tutte le partite di tutte le submission; nessuna nuova partita o simulazione. Deduplicazione per EpisodeId. I replay di leader contro altri leader sono esclusi dal presente screening.

**{sum(r['production770'] for r in rows)} replay di {len(counts)} nomi avversari** mantengono 7-7-0-0 a tutti i checkpoint D15–D25. **{sum(r['final770'] for r in rows)}** terminano 770; **{sum(r['final770'] and not r['production770'] for r in rows)}** sono 770 soltanto secondo il criterio finale. Il nome del team non identifica necessariamente una policy unica: submission distinte restano distinte quando i metadati sono disponibili. Non sono automaticamente agenti top o adattativi.

| Avversario | Episodio | 770 D15–25 | 770 D30 | Diretto V51C |
|---|---:|---|---|---|
'''
    for r in sorted(candidates,key=lambda r:(r['opponent'],r['episode'])):
        text+=f"| {r['opponent']} | [{r['episode']}](https://www.kaggle.com/competitions/episodes/{r['episode']}) | {'sì' if r['production770'] else 'no'} | {'sì' if r['final770'] else 'no'} | {'sì' if r['direct_v51'] else 'no'} |\n"
    text+=f'\n## Confronto diretto disponibile\n\n{len(profiles)} replay V51C contro 770 produttiva con 22 KPI e ledger verificati su entrambi i lati; {len(errors)} errori di audit, elencati in AUDIT_ERRORS.json. Tutti gli esiti inclusi, nessuna selezione per vittoria. Confronto descrittivo dentro la stessa partita, non effetto causale della topologia; ruoli, mix produttivo e strategie differiscono.\n'
    if profiles:
        text+='\n![22 KPI](DIRECT_V51_770_KPI22.png)\n\nCheckpoint D1–D29 prima dell’ultimo batch, D30 terminale; flussi conteggiati sull’intero giorno. CSV con traiettorie individuali in DAILY_KPI.csv.\n'
        text+='\n| Avversario | Episodio | Cassa V51C | Cassa esterno | Margine V51C |\n|---|---:|---:|---:|---:|\n'
        for p in profiles:text+=f"| {p['opponent']} | {p['episode']} | {p['candidate']['reward']:.0f} | {p['external']['reward']:.0f} | {p['candidate']['reward']-p['external']['reward']:+.0f} |\n"
    text+='\nLe topologie giornaliere D1–D30 e gli hash raw sono in SCREEN.json; il catalogo selezionato è CANDIDATES.json. I confronti di leader precedenti sono già disponibili nel worktree V51, cartella reports/top_v51_20260909, e restano distinti dagli avversari delle nostre submission.\n'
    (OUT/'REPORT.md').write_text(text,encoding='utf-8')
    (OUT/'REPORT.html').write_text('<meta charset="utf-8"><title>Riavvio 770 V51C</title><style>body{font:17px/1.5 system-ui;max-width:1200px;margin:32px auto;padding:20px;color:#24354a}img{max-width:100%}td,th{padding:7px;border-bottom:1px solid #ddd}table{border-collapse:collapse}code{overflow-wrap:anywhere}</style>'+MarkdownIt().enable('table').render(text),encoding='utf-8')
    save(OUT/'MANIFEST.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file() and p.name!='MANIFEST.json'})
    print('DONE',len(rows),len(candidates),len(profiles),errors,flush=True)
if __name__=='__main__':main()
