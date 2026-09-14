"""Audited descriptive report: published E22.1 versus an observed E23 recipe."""
import contextlib,csv,hashlib,html,io,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
SOURCE=Path('C:/Users/pietr/.codex/worktrees/756c/kaggriculture-agent')
OUT=ROOT/'docs/model_specs/codex/e23/reports/geese_vs_e221_20260914'
sys.path.insert(0,str(SOURCE))


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from docs.model_specs.codex.e22.tools.analyze_external_20260914 import enrich
        from docs.model_specs.codex.e22.tools.report_external_20260914 import page,METRICS,aggregate,rowdata
    cohort=json.loads((ROOT/'docs/model_specs/codex/e23/reports/near3000_20260914/COHORT.json').read_text(encoding='utf-8'))
    g=next(x for x in cohort if x['submission']==56222223 and x['episode']==108922490)
    path=ROOT/f'data/replays/json/e23_near3000_20260914/{g["episode"]}.json'
    raw=path.read_bytes();r=json.loads(raw)
    for i,s in enumerate(r['steps']):s[0]['observation']['step']=i
    cache=OUT/'CANDIDATE_AUDIT.json'
    if cache.exists():candidate=json.loads(cache.read_text())
    else:
        candidate={}
        for label,seat in [('own',g['seat']),('opponent',1-g['seat'])]:
            candidate[label]=enrich(r,seat)
            print('AUDITED',label,'cash_errors',candidate[label]['ledger']['cash_parity_errors'],flush=True)
        cache.write_text(json.dumps(candidate),encoding='utf-8')
    basepath=SOURCE/'docs/model_specs/codex/e23/reports/external_e22_1_q2_grano_20260914/profiles/108891785.json'
    baseline=json.loads(basepath.read_text())
    a,b=baseline['own'],candidate['own']
    assert all(p['ledger']['cash_parity_errors']==0 for p in [a,b,baseline['opponent'],candidate['opponent']])
    summary={}
    for label,p in [('E22.1',a),('E23_recipe',b)]:
        t=p['totals']
        summary[label]=dict(cash=p['reward'],revenue=sum(t['sales_cash'].values()),purchases=sum(t['purchase_cash'].values()),labor=t['hire_cash'],land=t['land_cash'],unit_cash=t['unit_cash_delta'],sold=t['sold_units'],sales=t['sales_cash'],harvested=t['harvested'],terminal=p['terminal'],escapes=len(p['ledger']['animal_escapes']),unfed=len(p['unfed']))
    delta=b['reward']-a['reward']
    sa,sb=summary.values()
    assert abs(delta-((sb['revenue']-sa['revenue'])-(sb['purchases']-sa['purchases'])-(sb['labor']-sa['labor'])-(sb['land']-sa['land'])+(sb['unit_cash']-sa['unit_cash'])))<.01
    data=dict(metrics=METRICS,views=[
        dict(title='E22.1 vs ricetta E23 · mercati differenti',labels=['E22.1 · 8C6S3G','Ricetta E23 · 9C5S3G'],note='Confronto descrittivo di due partite diverse: non misura il guadagno della trasformazione. Le bande coincidono con la linea perché ogni serie contiene un replay.',series=[aggregate([a]),aggregate([b])]),
        dict(title='E22.1 · confronto con il proprio avversario',labels=['E22.1','Avversario del replay 108891785'],note='Due lati dello stesso replay 108891785.',series=[aggregate([a]),aggregate([baseline['opponent']])]),
        dict(title='Ricetta E23 · confronto con il proprio avversario',labels=['Thomas · 9C5S3G','Avversario del replay 108922490'],note='Due lati dello stesso replay 108922490; Thomas non è una nostra submission E23.',series=[aggregate([b]),aggregate([candidate['opponent']])])])
    def fmt(v):return f'{v:,.1f}'.replace(',','X').replace('.',',').replace('X','.')
    body='<p>E22.1 Q2 Grano <b>56228842</b> · ricetta candidata osservata in Thomas Tschinkel <b>56222223</b> · 14 settembre 2026.</p>'
    body+='<p class="note"><b>E23 non è ancora implementata.</b> Questo report confronta la ricetta 9 mucche / 5 pecore / 3 oche osservata nel replay 108922490 con E22.1 nel replay 108891785. Semi, mercati e avversari sono diversi: il delta di cassa non è una stima del miglioramento di E23.</p>'
    body+='<section><h2>Trasformazione proposta</h2><p><b>8C6S3G → 9C5S3G:</b> stesse 17 coordinate animali, 14 pascoli e 3 pollai. In (6,2) una mucca prende il posto della pecora al primo collocamento, D10 H14. Nessuna rimozione animale necessaria.</p><p>Il nucleo 33 fragole / 25 grani e le successioni D22–25 sono condivisi. Nel replay candidato il pollaio vuoto Q2 viene costruito tardi: <b>conservare invece il nostro Q2 Grano</b> nella futura variante. I checkpoint colturali differiscono a D8, D28 e D29; le altre 27 mappe coincidono.</p><p>Organico cumulato ai checkpoint: <b>260 → 268 giornate-manovale</b>. I servizi e le vendite cambiano oltre alla specie: il replay candidato non è un esperimento isolato del solo mix.</p></section>'
    body+='<h2>Contabilità dei due replay</h2><div class="tablewrap"><table><tr><th>Indicatore</th><th>E22.1</th><th>Ricetta E23</th><th>Delta osservato</th></tr>'
    for label,k in [('Cassa finale','cash'),('Ricavi lordi','revenue'),('Acquisti','purchases'),('Manodopera','labor'),('Terreni','land'),('Fughe','escapes'),('Eventi animale/giorno senza pasto','unfed')]:
        body+=f'<tr><td>{label}</td><td>{fmt(sa[k])}</td><td>{fmt(sb[k])}</td><td>{fmt(sb[k]-sa[k])}</td></tr>'
    body+='</table></div><h2>Produzioni e prezzi realizzati</h2><div class="tablewrap"><table><tr><th>Prodotto</th><th>Raccolto E22 / E23</th><th>Venduto E22 / E23</th><th>Prezzo ponderato E22 / E23</th><th>Delta ricavi</th></tr>'
    for item in ['MILK','WOOL','EGG','STRAWBERRY','MELON','WHEAT','CARROT','TOMATO','FERTILIZER']:
        nums=[s['sold'].get(item,0) for s in [sa,sb]];prices=[fmt(s['sales'].get(item,0)/n) if n else 'n/d' for s,n in zip([sa,sb],nums)]
        harvested='n/a (raccolta separata)' if item=='FERTILIZER' else f'{sa["harvested"].get(item,0)} / {sb["harvested"].get(item,0)}'
        body+=f'<tr><td>{item}</td><td>{harvested}</td><td>{nums[0]} / {nums[1]}</td><td>{prices[0]} / {prices[1]}</td><td>{fmt(sb["sales"].get(item,0)-sa["sales"].get(item,0))}</td></tr>'
    body+='</table></div><h2>Mappe D1–D30</h2><section><label>Giorno <input id="mapday" type="range" min="1" max="30" value="20"><b id="daylabel">20</b></label><p class="meta">Coordinate (x,y) zero-based. C mucca · S pecora · G oca · F fragola · W grano · M melone · R carota · T pomodoro · P pascolo vuoto · O pollaio vuoto. Il bordo rosso indica una differenza fra i due replay.</p><div id="maps" class="grid"></div></section>'
    body+='<h2>Come leggere il report</h2><p>22 KPI standard e 18 grafici di volumi e prezzi: 40 pannelli, tre viste. Cassa e consistenze ai checkpoint 24D−1, D30 terminale; flussi su tutte le azioni. Prezzi realizzati = ricavi / unità vendute, n/d senza vendite. Comandi falliti e servizi mancanti non sono automaticamente perdite recuperabili.</p><p><a href="REPORT.md">Sintesi e limiti</a> · <a href="DAILY.csv">CSV giornaliero</a> · <a href="VERIFICATION.json">Verifica contabile</a></p>'
    maps=json.dumps([a['maps'],b['maps']])
    js="""const mapsData=MAPDATA;function mapDraw(){let d=+document.getElementById('mapday').value;document.getElementById('daylabel').textContent=d;let root=document.getElementById('maps');root.replaceChildren();let lookup=mapsData.map(m=>Object.fromEntries(m[d-1].map(t=>[t.x+','+t.y,t])));const token=t=>t?(t.animal||t.crop||t.kind):'';const chars={COW:'C',SHEEP:'S',GOOSE:'G',STRAWBERRY:'F',WHEAT:'W',MELON:'M',CARROT:'R',TOMATO:'T',PASTURE:'P',COOP:'O',WEED:'×'};lookup.forEach((m,s)=>{let box=document.createElement('div');let title=document.createElement('h3');title.textContent=s?'Ricetta E23 · Thomas':'E22.1 Q2 Grano';box.append(title);let svg=elem('svg',{viewBox:'0 0 420 420',role:'img','aria-label':title.textContent+' giorno '+d});for(let y=0;y<10;y++)for(let x=0;x<10;x++){let t=m[x+','+y],v=token(t),diff=v!==token(lookup[1-s][x+','+y]);svg.append(elem('rect',{x:20+x*38,y:20+y*38,width:36,height:36,fill:t?(t.animal?'#dcebf7':t.crop?'#e4efd9':'#f0eadb'):'#f4f5f6',stroke:diff?'#bd3c30':'#ccd3d9','stroke-width':diff?2:1}));svg.append(elem('text',{x:38+x*38,y:43+y*38,'text-anchor':'middle'},chars[v]||''));}for(let i=0;i<10;i++){svg.append(elem('text',{x:38+i*38,y:12,'text-anchor':'middle'},i));svg.append(elem('text',{x:10,y:43+i*38,'text-anchor':'middle'},i));}box.append(svg);root.append(box);});}document.getElementById('mapday').addEventListener('input',mapDraw);mapDraw();""".replace('MAPDATA',maps)
    output=page('E23 con oche / E22.1 · confronto della ricetta',body,data).replace('</html>','<script>'+js+'</script></html>')
    (OUT/'REPORT.html').write_text(output,encoding='utf-8')
    with (OUT/'DAILY.csv').open('w',newline='',encoding='utf-8') as f:
        rows=[dict(row,series=label,day=i+1) for label,p in [('E22.1',a),('E23_recipe',b)] for i,row in enumerate(rowdata(p))]
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    verification=dict(ledger_profiles=4,cash_parity_errors=0,kpi=22,panels=40,views=3,new_simulations=0,e23_implemented=False,candidate_replay_sha256=hashlib.sha256(raw).hexdigest(),baseline_profile=str(basepath),cash_delta_reconciled=delta)
    (OUT/'VERIFICATION.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
    md=f'''# E23 con oche / E22.1

Report descrittivo: E22.1 Q2 Grano 56228842, replay 108891785, contro ricetta candidata 9C5S3G osservata nella submission Thomas 56222223, replay 108922490. E23 non è implementata. Mercati e avversari differenti: nessuna conclusione causale dal delta di cassa.

- Mix: 8C6S3G → 9C5S3G; stessa struttura, specie diversa in (6,2), collocamento D10 H14.
- Mappe colturali identiche in 27/30 checkpoint; differenze a D8, D28, D29. Q2 Grano della nostra E22.1 va conservato nell'evoluzione.
- Organico cumulato ai checkpoint: 260 → 268 giornate-manovale; non è costo monetario né fabbisogno minimo stimato.
- Cassa osservata: {fmt(sa['cash'])} → {fmt(sb['cash'])}; delta {fmt(delta)} in mercati diversi.
- Quattro ledger verificati, zero discrepanze; delta di cassa riconciliato con ricavi e costi. Nessuna nuova simulazione.

[Report interattivo: 22 KPI, volumi/prezzi e mappe](REPORT.html) · [CSV giornaliero](DAILY.csv) · [Dati sintetici](SUMMARY.json) · [Verifica](VERIFICATION.json)

Il prossimo confronto causale richiede una candidata implementata, stessa controparte e semi accoppiati. Cambiare soltanto la specie non riproduce automaticamente il calendario e i servizi del top.
'''
    (OUT/'REPORT.md').write_text(md,encoding='utf-8')
    print(json.dumps(verification),flush=True)


if __name__=='__main__':main()
