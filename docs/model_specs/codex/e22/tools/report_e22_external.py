"""Numeric-identity E22 replay report: outcomes, daily KPI and Q0 variant."""
import json,sys,statistics,html
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(Path(__file__).parent))
import e209_s56165462_charts as charts
OUT=ROOT/'docs/model_specs/codex/e22/reports/external_e22_20260913'
TARGET={(4,1),(3,2),(2,3)}
def mix(s,d=30):return dict(Counter(c['animal'] for c in s['daily'][d-1]['cells'] if c.get('animal')))
def signature(s):return {(c['x'],c['y']):c['kind'] for c in s['daily'][-1]['cells'] if c['kind'] in ('PASTURE','COOP')}
def totals(s):
 ds=s['ledger']['daily'];out={k:dict(sum((Counter(d[k]) for d in ds),Counter())) for k in ['sales_cash','sold_units','purchase_cash','harvested']};out['hire_cash']=sum(d['hire_cash'] for d in ds);out['land_cash']=sum(d['land_cash'] for d in ds);out['unit_cash_delta']=sum(d['unit_cash_delta'] for d in ds);return out
def map_svg(s):
 cells={(c['x'],c['y']):c for c in s['daily'][-1]['cells']};out='<svg viewBox="0 0 340 345" aria-label="Geometria D30">'
 for y in range(10):
  for x in range(10):
   c=cells.get((x,y),{});k=c.get('kind');color={'PASTURE':'#bbdf9a','COOP':'#f9cf78','PLANT':'#b4d6bf'}.get(k,'#e7ded1');label={'COW':'C','SHEEP':'S','GOOSE':'G'}.get(c.get('animal'),'');border='#c4353e' if (x,y) in TARGET else '#fff'
   out+=f'<rect x="{x*32+10}" y="{y*32+10}" width="31" height="31" fill="{color}" stroke="{border}" stroke-width="2"/><text x="{x*32+26}" y="{y*32+31}" text-anchor="middle" font-size="14">{label}</text>'
 out+='<path d="M170 10V330 M10 170H330" stroke="#354944" stroke-width="2"/></svg>';return out

def main():
 c=json.loads((OUT/'COHORT.json').read_text());gs=c['games'];ps=[json.loads(p.read_text()) for p in (OUT/'profiles').glob('*.json')];ps.sort(key=lambda p:p['time']);assert len(ps)==len(c['selected'])
 summary=dict(games=len(gs),wins=sum(g['margin']>0 for g in gs),draws=sum(g['margin']==0 for g in gs),losses=sum(g['margin']<0 for g in gs),mean_margin=statistics.mean(g['margin'] for g in gs),median_margin=statistics.median(g['margin'] for g in gs),latest_rating=gs[-1]['rating_after'],latest_episode=gs[-1]['episode'],peak_rating=max(g['rating_after'] for g in gs),audited=len(ps),parity_errors=sum(s['ledger']['cash_parity_errors'] for p in ps for s in p['sides']))
 family=[]
 for p in ps:
  a,b=p['sides'];sa,sb=signature(a),signature(b)
  row=dict(episode=p['episode'],opponent_submission=p['opponent_submission'],margin=p['margin'],own_mix=mix(a),opponent_mix=mix(b),q0_three_pastures=all(sb.get(x)=='PASTURE' for x in TARGET),q2_coop=sb.get((3,7))=='COOP',own_plan_matches=a['full_matches'],opponent_worker_matches=b['worker_matches'],own_escapes=len(a['ledger']['animal_escapes']),opponent_escapes=len(b['ledger']['animal_escapes']))
  family.append(row)
 target=next(p for p in ps if p['episode']==108561064);a,b=target['sides'];ta,tb=totals(a),totals(b)
 delta={k:tb['sales_cash'].get(k,0)-ta['sales_cash'].get(k,0) for k in set(ta['sales_cash'])|set(tb['sales_cash'])}
 cash_effect=dict(sales=delta,purchases=sum(ta['purchase_cash'].values())-sum(tb['purchase_cash'].values()),labor=ta['hire_cash']-tb['hire_cash'],land=ta['land_cash']-tb['land_cash'],unit_cash=tb['unit_cash_delta']-ta['unit_cash_delta'])
 assert sum(delta.values())+sum(cash_effect[k] for k in ['purchases','labor','land','unit_cash'])==target['opponent_cash']-target['cash']
 summary.update(variant_sample=[r for r in family if r['q0_three_pastures'] and r['q2_coop']],target=dict(episode=108561064,own_mix=mix(a),opponent_mix=mix(b),own_totals=ta,opponent_totals=tb,cash_effect=cash_effect,opponent_events=b['events'],opponent_escapes=b['ledger']['animal_escapes']))
 (OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');(OUT/'FAMILIES.json').write_text(json.dumps(family,indent=2)+'\n')
 intro=f"Storico congelato: {len(gs)} partite pubbliche concluse, {summary['wins']} vittorie, {summary['losses']} sconfitte, {summary['draws']} pareggi. Rating dopo l’ultimo episodio {summary['latest_episode']}: {summary['latest_rating']:.1f}; massimo osservato {summary['peak_rating']:.1f}. Il rating varia nel tempo e non coincide con la cassa di una partita."
 method=f"Audit dettagliato di {len(ps)} replay: 16 posizioni equidistanti nello storico, tre episodi segnalati e i margini estremi, senza duplicati. Campione diagnostico selezionato, non stima imparziale della frequenza delle strategie. Cassa verificata a ogni transizione per entrambi i giocatori: zero discrepanze. I KPI monetari seguono il giorno dell’azione; le mappe e la cassa sono osservazioni H24, prima dell’ultima azione del giorno quando presente."
 findings=f"Nell’episodio 108561064, la submission 56165125 sostituisce effettivamente con pascoli le coordinate (4,1), (3,2), (2,3), e mantiene il pollaio vuoto (3,7) in Q2. Coordinate zero-based: Q0 = x<5,y<5; Q2 = x<5,y>=5. E22 termina con {mix(a)}, l’avversario con {mix(b)}. Cassa 121.069 contro 130.059, differenza 8.990. Il confronto comprende anche altre differenze del mix e del calendario: non isola l’effetto dei soli tre pascoli."
 parts=['<!doctype html><html lang="it"><meta charset="utf-8"><title>E22 · Replay e variante Q0</title><style>body{font:16px system-ui;margin:30px auto;max-width:1450px;padding:0 24px;background:#f1f5f2;color:#24372f}p{line-height:1.6}section{background:white;padding:22px;border-radius:12px;margin:20px 0}.plots,.maps{display:grid;grid-template-columns:1fr 1fr;gap:18px}.plot{border:1px solid #dfe6e0;padding:12px;border-radius:9px;min-width:0}svg{width:100%}.maps svg{max-height:350px}select{padding:12px;font:inherit;max-width:100%}.muted{font-size:13px;color:#566c60}a{color:#155d8b}nav{position:sticky;top:0;background:#f1f5f2;padding:12px;z-index:3}@media(max-width:800px){.plots,.maps{grid-template-columns:1fr}}</style>',f'<h1>E22 · Replay e variante con pascoli in Q0</h1><p>{intro}</p><p>{method}</p><section><h2>La variante da sviluppare</h2><p>{findings}</p><p>Verde: pascolo; giallo: pollaio; C: mucca, S: pecora, G: oca. Le tre coordinate Q0 sono bordate in rosso. Una struttura vuota non equivale a un animale produttivo.</p><div class="maps"><div><h3>E22 · 56206528</h3>{map_svg(a)}</div><div><h3>Variante · 56165125</h3>{map_svg(b)}</div></div><p><a href="SUMMARY.json">Risultati e scomposizione contabile</a> · <a href="FAMILIES.json">Classificazione del campione</a> · <a href="COHORT.json">Protocollo e storico numerico</a></p></section>']
 # Entire cohort as a compact SVG, without compressing 78 games onto the 30-day chart axis.
 vals=[g['rating_after'] for g in gs];lo=min(vals)-30;hi=max(vals)+30;pts=' '.join(f'{45+i*1080/max(1,len(vals)-1):.1f},{230-(v-lo)/(hi-lo)*190:.1f}' for i,v in enumerate(vals));parts.append(f'<section><h2>Rating · tutte le {len(gs)} partite</h2><svg viewBox="0 0 1160 260"><polyline points="{pts}" fill="none" stroke="#2563eb" stroke-width="3"/><text x="5" y="30">{hi:.0f}</text><text x="5" y="245">{lo:.0f}</text><text x="45" y="255">Prima partita</text><text x="1000" y="255">Ultima congelata</text></svg></section>')
 parts.append('<section><h2>Pattern comune e origine del vantaggio</h2><p>Nel campione diagnostico, '+str(len(summary['variant_sample']))+' avversari hanno i tre pascoli Q0 e il pollaio Q2; E22 perde in tutti questi casi. Il campione include episodi segnalati e il margine peggiore: questa frequenza non misura la superiorità della variante nella popolazione.</p><p>Nel caso 108561064, lana +16.393 monete; uova −4.366; latte −1.303; altri ricavi −2.509. Acquisti complessivi inferiori di 2.118, lavoro superiore di 1.343: totale +8.990 per l’avversario. I soli acquisti di grano costano 3.621 contro 5.269 di E22; questo dato non misura da solo il risparmio da autoconsumo.</p><p>Il pascolo (4,1) resta vuoto: nessuna fuga nel caso guida. Le pecore aggiuntive entrano in (3,2) a D11 H20 e in (2,3) a D12 H7. Il pollaio Q2 (3,7) compare soltanto a D29 H5 e resta senza animale. La configurazione finale nasconde dunque tempi diversi e capacità non utilizzata.</p><p><b>Primo esperimento:</b> isolare tre pascoli Q0 con 8 mucche e fino a 9 pecore, contro E22 congelata. La replica 6 mucche/10 pecore è un secondo braccio distinto; non confonderne l’effetto con la sola conversione.</p></section>')
 parts.append('<nav><label>Replay <select id="match">'+''.join(f'<option value="{i}"'+(' selected' if p['episode']==108561064 else '')+f'>{p["episode"]} · S{p["opponent_submission"]} · margine E22 {p["margin"]:+,}</option>' for i,p in enumerate(ps))+'</select></label><p>Blu: E22 · Arancio: avversario. Passa sui punti per i valori.</p></nav>')
 for i,p in enumerate(ps):
  charts.NAMES=['E22',str(p['opponent_submission'])];ss=p['sides']
  def led(fn):return [[fn(d) for d in s['ledger']['daily']] for s in ss]
  def daily(fn):return [[fn(d) for d in s['daily']] for s in ss]
  parts.append(f'<section class="match" data-i="{i}"'+(' hidden' if p['episode']!=108561064 else '')+f'><h2>Episodio {p["episode"]}</h2><p>Cassa E22 {p["cash"]:,}; avversario {p["opponent_cash"]:,}. <a href="https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56206528&episodeId={p["episode"]}">Apri replay Kaggle</a>. Azioni E22 conformi: {ss[0]["full_matches"]}/719; gruppi lavoratori avversari uguali: {ss[1]["worker_matches"]}/719.</p><div class="plots">')
  parts.append(charts.chart('Cassa a H24',daily(lambda d:d['money']),'monete'))
  parts.append(charts.chart('Ricavi giornalieri',led(lambda d:sum(d['sales_cash'].values())),'monete'))
  parts.append(charts.chart('Costo lavoro',led(lambda d:d['hire_cash']),'monete'))
  parts.append(charts.chart('Acquisti di mercato',led(lambda d:sum(d['purchase_cash'].values())),'monete'))
  for animal in ['COW','SHEEP','GOOSE']:
   parts.append(charts.chart('Animali '+animal,daily(lambda d,a=animal:sum(c.get('animal')==a for c in d['cells']))))
  for kind in ['PASTURE','COOP']:
   parts.append(charts.chart('Caselle '+kind,daily(lambda d,k=kind:sum(c['kind']==k for c in d['cells'])),'caselle'))
  parts.append(charts.chart('Alimentazioni eseguite',led(lambda d:d['executed_actions'].get('FEED',0)),'azioni'))
  parts.append(charts.chart('Grano comprato · costo',led(lambda d:d['purchase_cash'].get('BUY_PRODUCT:WHEAT',0)),'monete'))
  parts.append(charts.chart('Grano comprato · quantità',led(lambda d:d['bought_units'].get('BUY_PRODUCT:WHEAT',0)),'unità'))
  for item in ['MILK','WOOL','EGG','MELON','STRAWBERRY','WHEAT']:
   parts.append(charts.chart(item+' · ricavi',led(lambda d,k=item:d['sales_cash'].get(k,0)),'monete'))
   parts.append(charts.chart(item+' · prezzo realizzato',led(lambda d,k=item:d['sales_cash'].get(k,0)/d['sold_units'][k] if d['sold_units'].get(k,0) else None),'monete/unità'))
  parts.append('</div></section>')
 parts.append('<section><h2>Esperimento successivo</h2><p>Conservare E22 congelata. Prima variante: sostituire i tre pollai Q0 con pascoli e pianificarne animali, alimentazione e raccolta, mantenendo il pollaio Q2. Separare questa ipotesi dalla replica dell’intero mix avversario. Confrontare entrambe le posizioni su seed accoppiati, misurando margine, lavoro, acquisti di grano, produzione, prezzi realizzati, fughe e rimanenze. Nessuna superiorità causale dei pascoli dimostrata dai soli replay.</p></section><script>document.getElementById("match").addEventListener("change",e=>document.querySelectorAll(".match").forEach(x=>x.hidden=x.dataset.i!==e.target.value));</script></html>')
 (OUT/'REPORT.html').write_text(''.join(parts),encoding='utf-8')
 (OUT/'REPORT.md').write_text('# E22 — replay e variante Q0\n\n'+intro+'\n\n'+method+'\n\n'+findings+'\n\n## Scomposizione del margine avversario nel caso 108561064\n\n'+ '\n'.join(f'- Ricavi {k}: {v:+,} monete.' for k,v in sorted(delta.items(),key=lambda x:-abs(x[1])))+'\n'+ '\n'.join(f'- Effetto {k}: {cash_effect[k]:+,} monete.' for k in ['purchases','labor','land','unit_cash'])+'\n\nLa somma è esattamente +8.990, ma è una scomposizione contabile, non l’effetto causale dei soli pascoli.\n\n[Grafici sui 30 giorni e selettore replay](REPORT.html). [Dati sintetici](SUMMARY.json).\n',encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
