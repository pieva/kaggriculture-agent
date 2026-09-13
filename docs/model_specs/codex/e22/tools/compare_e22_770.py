"""Direct, serial E22 versus frozen E19 770 V51C comparison."""
import copy,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
OUT=ROOT/'docs/model_specs/codex/e22/reports/e22_vs_770v51c';OUT.mkdir(exist_ok=True)
ART=ROOT/'docs/model_specs/codex/e22/artifacts/e22_vs_770v51c';ART.mkdir(parents=True,exist_ok=True)
def main():
 files=[ROOT/'submission/submission_codex_e22_s56165462_observed_v1.py',ROOT/'submission/submission_codex_e19_770_v51_candidate.py']
 protocol=dict(models=['E22Replica','E19 770 V51C'],seeds=[180911301,180911303],roles=[0,1],method='Direct paired matches, serial execution, exposed seeds, shared endogenous market; no policy modifications.',hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
 (OUT/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2),encoding='utf-8')
 from kaggle_environments import make
 from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
 rows=[]
 for seed in protocol['seeds']:
  for seat in [0,1]:
   path=ART/f'E22Replica_{seed}_{seat}.json'
   if path.exists():rows.append(json.loads(path.read_text()));continue
   agents=[None,None]
   for p,s in zip(files,[seat,1-seat]):
    ns={};exec(p.read_text(encoding='utf-8'),ns);agents[s]=ns['create_agent']({'player_position':s})
   env=make('kaggriculture',configuration=dict(seed=seed,episodeSteps=720,turnsPerDay=24),debug=False);env.run(agents);r=env.toJSON()
   assert len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1])
   ls=[audit(r,i) for i in [0,1]]
   row=dict(model='E22Replica',seed=seed,seat=seat,rewards=r['rewards'],margin=r['rewards'][seat]-r['rewards'][1-seat],ledgers=ls,terminal=[end_state(r,i) for i in [0,1]])
   with gzip.open(path.with_suffix('.replay.json.gz'),'wt',encoding='utf-8') as f:json.dump(r,f,separators=(',',':'))
   path.write_text(json.dumps(row,separators=(',',':')),encoding='utf-8');rows.append(row);print('RESULT',seed,seat,row['rewards'],row['margin'],flush=True)
 (OUT/'RESULTS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 # Render the direct comparison using the shared daily chart primitive.
 from e209_s56165462_charts import chart
 from statistics import mean
 summary=dict(n=len(rows),wins=sum(r['margin']>0 for r in rows),mean_margin=mean(r['margin'] for r in rows),min_margin=min(r['margin'] for r in rows),max_margin=max(r['margin'] for r in rows))
 (OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
 intro=f"Confronto diretto: E22 contro E19 770 V51C (submission 56124996, bundle storico verificato con hash). {summary['wins']}/4 vittorie E22; margine medio {summary['mean_margin']:,.1f} monete. Due seed esposti, entrambi i ruoli; nessuna modifica ai candidati."
 body='<h1>E22 vs E19 770 V51C · confronto diretto</h1><p>'+intro+'</p><p>Blu: E19 770 V51C · Arancio: E22. Valori sui punti. <a href="PROTOCOL.json">Protocollo</a> · <a href="RESULTS.json">Dati verificati</a></p><label>Partita <select id="match">'+''.join(f'<option value="{i}">Seed {r["seed"]} · E22 ruolo {r["seat"]}</option>' for i,r in enumerate(rows))+'</select></label>'
 for i,r in enumerate(rows):
  seat=r['seat'];ls=[r['ledgers'][1-seat],r['ledgers'][seat]];g=json.load(gzip.open(ART/f'E22Replica_{r["seed"]}_{seat}.replay.json.gz','rt',encoding='utf-8'))
  def series(fn):return [[fn(d) for d in l['daily']] for l in ls]
  def plot(title,s,u):return chart(title,s,u).replace('E20.9','E19 770 V51C').replace('s56165462','E22')
  body+=f'<section data-i="{i}"'+(' hidden' if i else '')+f'><h2>Seed {r["seed"]} · ruolo {seat}</h2><p>Cassa E22 {r["rewards"][seat]:,.0f}; E19 770 V51C {r["rewards"][1-seat]:,.0f}; margine {r["margin"]:,.0f}.</p><div class="plots">'
  body+=plot('Cassa giornaliera',[[g['steps'][d*24-1][s]['observation']['farms'][s]['money'] for d in range(1,31)] for s in [1-seat,seat]],'monete')
  body+=plot('Costo lavoro',series(lambda d:d['hire_cash']),'monete/giorno')
  def tiles(s,d):return [t for row in g['steps'][d*24-1][s]['observation']['farms'][s]['tiles'] for t in row if isinstance(t,dict)]
  body+=plot('Strutture animali',[[sum(t.get('kind') in ['PASTURE','COOP'] for t in tiles(s,d)) for d in range(1,31)] for s in [1-seat,seat]],'caselle')
  body+=plot('Assunzioni',series(lambda d:d['hires']),'lavoratori/giorno')
  for item in ['MELON','STRAWBERRY','WOOL','MILK','EGG','WHEAT','CARROT','TOMATO','FERTILIZER']:
   species={'WOOL':'SHEEP','MILK':'COW','EGG':'GOOSE'}.get(item,item)
   if item!='FERTILIZER':
    body+=plot(item+' · raccolto',series(lambda d:d['harvested'].get(item,0)),'unità/giorno')
    body+=plot(item+' · caselle produttive',[[sum((t.get('animal') or t.get('crop'))==species for t in tiles(s,d)) for d in range(1,31)] for s in [1-seat,seat]],'caselle')
   body+=plot(item+' · quantità venduta',series(lambda d:d['sold_units'].get(item,0)),'unità/giorno')
   body+=plot(item+' · prezzo realizzato',series(lambda d:d['sales_cash'].get(item,0)/d['sold_units'][item] if d['sold_units'].get(item,0) else None),'monete/unità')
   body+=plot(item+' · ricavi',series(lambda d:d['sales_cash'].get(item,0)),'monete/giorno')
  body+='</div></section>'
 body+='<p>Audit della cassa sulle 719 transizioni di entrambi. Quattro partite su due seed esposti non sono una stima del rating né una conferma su seed riservati.</p><script>document.getElementById("match").addEventListener("change",e=>document.querySelectorAll("section[data-i]").forEach(x=>x.hidden=x.dataset.i!==e.target.value));</script>'
 (OUT/'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>E22 vs E19 770 V51C</title><style>body{font:16px system-ui;max-width:1400px;margin:30px auto;padding:0 24px;background:#f3f5f0;color:#24332d}section{background:white;padding:24px;border-radius:12px;margin:20px 0}p{line-height:1.6}.plots{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.plot{border:1px solid #ddd;padding:12px;border-radius:8px;min-width:0}svg{width:100%}select{padding:10px;font:inherit}@media(max-width:850px){.plots{grid-template-columns:1fr}}</style>'+body+'</html>',encoding='utf-8')
 (OUT/'REPORT.md').write_text('# E22 vs E19 770 V51C\n\n'+intro+'\n\n| Seed | Ruolo E22 | Cassa E22 | Cassa V51C | Margine E22 |\n|---|---|---:|---:|---:|\n'+'\n'.join(f"| {r['seed']} | {r['seat']} | {r['rewards'][r['seat']]} | {r['rewards'][1-r['seat']]} | {r['margin']} |" for r in rows)+'\n\n[Grafici D1–D30](REPORT.html). Risultati sui soli seed esposti; nessuna pubblicazione.\n',encoding='utf-8')
 print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
