"""Daily comparison charts, generated directly from the audited profiles."""
import html

COLORS=['#2563eb','#c05e12']
NAMES=['E20.9','s56165462']
def chart(title,series,unit='unità'):
 values=[v for seq in series for v in seq if v is not None]
 lo=min([0,*values]);hi=max([1,*values]);span=hi-lo
 def y(v):return 205-170*(v-lo)/span
 def x(i):return 65+i*25
 svg=f'<svg viewBox="0 0 830 245" role="img" aria-label="{html.escape(title)}">'
 for j in range(5):
  v=lo+span*j/4;yy=y(v)
  svg+=f'<line x1="65" x2="790" y1="{yy}" y2="{yy}" stroke="#e2e7e1"/><text x="57" y="{yy+4}" text-anchor="end" font-size="11">{v:,.0f}</text>'
 for i in [0,4,9,14,19,24,29]:svg+=f'<text x="{x(i)}" y="227" text-anchor="middle" font-size="12">D{i+1}</text>'
 for k,seq in enumerate(series):
  segments=[];part=[]
  for i,v in enumerate(seq):
   if v is None:
    if part:segments.append(part);part=[]
   else:part.append(f'{x(i)},{y(v)}')
  if part:segments.append(part)
  for seg in segments:svg+=f'<polyline points="{" ".join(seg)}" fill="none" stroke="{COLORS[k]}" stroke-width="2.5"/>'
  for i,v in enumerate(seq):
   if v is not None:svg+=f'<circle cx="{x(i)}" cy="{y(v)}" r="3" fill="{COLORS[k]}"><title>{NAMES[k]} · D{i+1}: {v:,.2f} {unit}</title></circle>'
 svg+='</svg>'
 return f'<article class="plot"><h3>{html.escape(title)}</h3><span class="muted">{unit} · D1–D30</span>{svg}</article>'

def dashboard(ps):
 def ledger(fn):return [[fn(d) for d in p['ledger']['daily']] for p in ps]
 def snapshots(fn):return [[fn(d) for d in p['daily']] for p in ps]
 def net(d):return sum(d['sales_cash'].values())-sum(d['purchase_cash'].values())-d['hire_cash']-d['land_cash']+d['unit_cash_delta']
 styles='<style>.plots{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.plot{border:1px solid #dde4db;border-radius:10px;padding:14px;min-width:0}.plot h3{margin:0 0 5px;font-size:17px}.plot svg{display:block;width:100%;max-height:none}.muted{color:#627166;font-size:13px}.legend{position:sticky;top:0;background:#f3f5f0;padding:12px;z-index:2}.legend b{margin-right:20px}summary{cursor:pointer;padding:15px;font-weight:600}@media(max-width:850px){.plots{grid-template-columns:1fr}}</style>'
 out=styles+'<h1>E20.9 vs s56165462 · 30 giorni</h1><p>Scontro diretto 108480607 · Cassa finale 70.898 vs 81.844 · Distacco 10.946 monete. Stesso mercato, un solo confronto: non una stima generale di forza.</p><p>Submission: <a href="https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56202079">E20.9 · 56202079</a> · <a href="https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56166543">s56165462 · 56166543</a> · <a href="KPI.json">Dati</a></p><div class="legend"><b style="color:#2563eb">● E20.9</b><b style="color:#c05e12">● s56165462</b>Passa sui punti per giorno e valore.</div>'
 out+='<section><h2>D11: stessa raccolta e stessi ordini, consegne diverse</h2><p>Entrambi raccolgono 72 meloni. A D11 E20.9 vende 30 unità, s56165462 60; a D12 ne vendono 36 e 12. E20.9 lascia 42 meloni trasportati al cambio giornata: soltanto 36 entrano nel deposito pieno, 6 vengono scartati. Gli ordini di vendita a D11 sono identici, ma il prodotto deve essere nel deposito per essere venduto.</p><p>Il delta totale non resta costante: +6.132 a D11, +4.710 a D12, +10.946 a D30. Il contributo cumulativo dei meloni si ferma invece dopo D12.</p><p>Submission del nuovo link, <b>56165462</b>: 20/20 replay controllati con comandi dei lavoratori e ordini di mercato esattamente identici; 19/20 anche con le stesse traiettorie colturali. Campione di 20 su 289 disponibili, distinto dalla submission 56166543 dello scontro diretto.</p><a href="D11_AND_CONSISTENCY.md">Diagnosi, campionamento e limiti</a></section>'
 out+='<section><h2>Risultato e flussi monetari</h2><div class="plots">'
 out+=chart('Cassa a fine giornata',snapshots(lambda d:d['money']),'monete')
 out+=chart('Flusso netto giornaliero',ledger(net),'monete/giorno')
 out+=chart('Ricavi giornalieri',ledger(lambda d:sum(d['sales_cash'].values())),'monete/giorno')
 out+=chart('Costi giornalieri: acquisti, lavoro e terreni',ledger(lambda d:sum(d['purchase_cash'].values())+d['hire_cash']+d['land_cash']),'monete/giorno')
 out+='</div><p>6.115 monete del distacco si formano tra D7 e D11. Flussi calcolati dal registro delle transazioni, cassa dai rilevamenti giornalieri.</p></section>'
 out+='<section><h2>Lavoro e capacità produttiva</h2><div class="plots">'
 out+=chart('Assunzioni giornaliere',ledger(lambda d:d['hires']),'lavoratori')+chart('Costo delle assunzioni',ledger(lambda d:d['hire_cash']),'monete/giorno')
 out+=chart('Caselle con colture',snapshots(lambda d:d['crop_tiles']),'caselle')+chart('Strutture animali',snapshots(lambda d:d['livestock_structures']),'caselle')
 out+=chart('Comandi di movimento richiesti',ledger(lambda d:d['requested_actions'].get('MOVE',0)),'comandi')+chart('Comandi PASS richiesti',ledger(lambda d:d['requested_actions'].get('PASS',0)),'comandi')
 out+='</div><p>MOVE e PASS non misurano automaticamente lo spreco. L’aumento dei costi dipende anche dalla concentrazione delle assunzioni nello stesso giorno.</p></section>'
 products=['MELON','STRAWBERRY','WOOL','MILK','EGG','CARROT','TOMATO','WHEAT','FERTILIZER']
 labels=['Meloni','Fragole','Lana','Latte','Uova','Carote','Pomodori','Grano','Fertilizzante']
 out+='<section><h2>Produzione e monetizzazione per prodotto</h2><label for="chart-product">Prodotto </label><select id="chart-product">'+''.join(f'<option value="{p}">{l}</option>' for p,l in zip(products,labels))+'</select><p>Prezzo realizzato = ricavi / quantità venduta quel giorno. Giorni senza vendite lasciati vuoti. Quantità vendute e prezzi sono riportati sotto i grafici di produzione.</p>'
 for j,item in enumerate(products):
  out+=f'<div class="product-charts" data-product="{item}"'+(' hidden' if j else '')+'><div class="plots">'
  if item!='FERTILIZER':out+=chart('Quantità raccolta',ledger(lambda d:d['harvested'].get(item,0)),'unità/giorno')
  else:out+='<article class="plot"><h3>Raccolta fertilizzante</h3><p>La quantità raccolta tramite COLLECT_FERTILIZER non è ricostruita dal contatore HARVEST. Non viene rappresentata come zero.</p></article>'
  crop=item if item in ['MELON','STRAWBERRY','CARROT','TOMATO','WHEAT'] else None
  animal={'WOOL':'SHEEP','MILK':'COW','EGG':'GOOSE'}.get(item)
  if crop:out+=chart('Caselle della coltura a fine giornata',snapshots(lambda d:d['crops'].get(crop,0)),'caselle')
  elif animal:out+=chart('Animali della specie a fine giornata',snapshots(lambda d:d['animals'].get(animal,0)),'animali')
  else:out+=chart('Fertilizzante acquistato',ledger(lambda d:d['bought_units'].get('BUY_PRODUCT:FERTILIZER',0)),'unità/giorno')
  out+=chart('Quantità venduta',ledger(lambda d:d['sold_units'].get(item,0)),'unità/giorno')
  out+=chart('Prezzo medio realizzato',ledger(lambda d:d['sales_cash'].get(item,0)/d['sold_units'][item] if d['sold_units'].get(item,0) else None),'monete/unità')
  out+=chart('Ricavi del prodotto',ledger(lambda d:d['sales_cash'].get(item,0)),'monete/giorno')+'</div></div>'
 out+='</section><section><h2>Grano e nutrimento animale</h2><div class="plots">'
 out+=chart('Grano acquistato',ledger(lambda d:d['bought_units'].get('BUY_PRODUCT:WHEAT',0)),'unità/giorno')
 out+=chart('FEED eseguiti',ledger(lambda d:d['executed_actions'].get('FEED',0)),'razioni/giorno')
 out+=chart('Spesa per acquisti di grano',ledger(lambda d:d['purchase_cash'].get('BUY_PRODUCT:WHEAT',0)),'monete/giorno')
 out+=chart('Prezzo medio di acquisto del grano',ledger(lambda d:d['purchase_cash'].get('BUY_PRODUCT:WHEAT',0)/d['bought_units']['BUY_PRODUCT:WHEAT'] if d['bought_units'].get('BUY_PRODUCT:WHEAT',0) else None),'monete/unità')
 out+='</div><p>Le serie distinguono acquisti e nutrimento; non attribuiscono automaticamente il grano consumato al raccolto proprio. Prezzi medi giornalieri, non prova di arbitraggio.</p></section><script>document.getElementById("chart-product").addEventListener("change",e=>document.querySelectorAll(".product-charts").forEach(p=>p.hidden=p.dataset.product!==e.target.value));</script>'
 return out
