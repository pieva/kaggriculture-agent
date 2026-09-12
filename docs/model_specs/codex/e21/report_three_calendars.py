"""22 KPIs and product diversification: Goose2, common native, frozen775."""
from pathlib import Path
import sys,json,gzip,csv,hashlib,html
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3];sys.path.insert(0,str(ROOT))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS
OUT=BASE/'reports/three_calendars_goose2';OUT.mkdir(exist_ok=True)
PRODUCTS=['MELON','STRAWBERRY','WHEAT','CARROT','TOMATO','MILK','WOOL','EGG']
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def table(headers,rows):return '<table><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</table>'
all_kpi=[];all_market=[];summary=[];sources={};images=[];checks=[]
for seed in [180911301,180911303]:
 stems=[BASE/f'artifacts/operational772_goose2_v2/Goose2_E18_{seed}',BASE/f'artifacts/operational772_recorded_control/OpRecorded_E18_{seed}']
 games=[]
 for stem in stems:
  for suffix in ['.json','.kpi.json','.replay.json.gz']:
   p=stem.with_suffix(suffix);sources[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
  m=read(stem.with_suffix('.json'));k=read(stem.with_suffix('.kpi.json'));r=json.load(gzip.open(stem.with_suffix('.replay.json.gz'),'rt',encoding='utf-8'))
  assert len(r['steps'])==720
  games.append((m,k,r))
 profiles=[('Nuova 772 · 8C/6S/2G',games[0][1]['sides'][0],0,0),('Comune · 8C/6S/3G',games[1][1]['sides'][0],1,0),('775 · avversaria nuova 772',games[0][1]['sides'][1],0,1)]
 colors=['#007c91','#d97512','#7562aa'];styles=['-','--',':']
 for label,p,g,seat in profiles:
  assert len(p['kpi'])==30 and all(all(key in d for key,_,_ in FIELDS) for d in p['kpi'])
  checks.append({'seed':seed,'version':label,'calls':games[g][0]['runtime'][seat]['calls'],'cash_parity_errors':p['ledger']['cash_parity_errors'],'days':30,'kpi_count':22})
  last=p['kpi'][-1];summary.append([seed,label,int(p['reward']),int(games[g][0]['rewards'][1-seat]),'/'.join(str(last[x]) for x in ['COW','SHEEP','GOOSE']),len(p['crop_starvation'])])
  for d in p['kpi']:all_kpi.append(dict(seed=seed,version=label,game=g,seat=seat,day=d['day'],**{key:d[key] for key,_,_ in FIELDS}))
 fig,axes=plt.subplots(11,2,figsize=(16,33))
 for ax,(key,title,unit) in zip(axes.flat,FIELDS):
  for (label,p,_,_),color,style in zip(profiles,colors,styles):ax.plot(range(1,31),[d[key] for d in p['kpi']],label=label,color=color,ls=style,lw=2)
  ax.set_title('Caselle coltivate' if key=='crop_tiles' else title);ax.set_ylabel(unit);ax.set_xlabel('Giorno');ax.grid(alpha=.2);ax.set_xlim(1,30)
  if key=='MELON':ax.text(.04,.15,'Nuova 772 e comune coincidono:\n12 caselle, raccolta a D11',transform=ax.transAxes,fontsize=9)
 h,l=axes.flat[0].get_legend_handles_labels();fig.legend(h,l,loc='upper center',ncol=3);fig.tight_layout(rect=(0,0,1,.98));fig.savefig(OUT/f'KPI22_{seed}.png',dpi=110);plt.close(fig)
 # Product sales show timing and diversification without mixing unlike units.
 fig,axes=plt.subplots(3,1,figsize=(16,13),sharex=True);palette=plt.get_cmap('tab10').colors
 for ax,(label,p,g,seat) in zip(axes,profiles):
  bottom=[0]*30
  for prod,c in zip(PRODUCTS,palette):
   values=[d['sales_cash'].get(prod,0) for d in p['ledger']['daily']]
   ax.bar(range(1,31),values,bottom=bottom,label=prod,color=c);bottom=[a+b for a,b in zip(bottom,values)]
  ax.set_title(label);ax.set_ylabel('Incassi giornalieri');ax.grid(axis='y',alpha=.2)
 h,l=axes[0].get_legend_handles_labels();fig.legend(h,l,loc='upper center',ncol=8);axes[-1].set_xlabel('Giorno');fig.tight_layout(rect=(0,0,1,.96));fig.savefig(OUT/f'SALES_{seed}.png',dpi=110);plt.close(fig)
 fig,axes=plt.subplots(4,2,figsize=(16,15))
 for g,(_,k,r) in enumerate(games):
  for day in range(1,31):
   d=k['sides'][0]['kpi'][day-1];o=r['steps'][d['step_index']][0]['observation']
   for prod in PRODUCTS:
    row={'seed':seed,'game':g,'market':'nuova772 vs775' if g==0 else 'comune vs775','day':day,'product':prod,'end_price':o['market']['prices'][prod],'market_inventory':o['market']['inventory'][prod]}
    for seat in [0,1]:
     led=k['sides'][seat]['ledger']['daily'][day-1]
     row[f'sold_units_seat{seat}']=led['sold_units'].get(prod,0);row[f'sales_cash_seat{seat}']=led['sales_cash'].get(prod,0)
    all_market.append(row)
  for ax,prod in zip(axes.flat,PRODUCTS):
   ds=[d for d in all_market if d['seed']==seed and d['game']==g and d['product']==prod]
   ax.plot(range(1,31),[d['end_price'] for d in ds],label='Nuova 772 vs 775' if g==0 else 'Comune vs 775',color=colors[g],ls=styles[g],lw=2)
   ax.set_title(prod);ax.set_ylabel('Prezzo a fine giornata');ax.set_xlabel('Giorno');ax.grid(alpha=.2)
 h,l=axes.flat[0].get_legend_handles_labels();fig.legend(h,l,loc='upper center',ncol=2);fig.tight_layout(rect=(0,0,1,.97));fig.savefig(OUT/f'PRICES_{seed}.png',dpi=110);plt.close(fig)
 images.append(seed)
for name,rows in [('KPI22',all_kpi),('MARKET',all_market)]:
 with (OUT/f'{name}.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'VERIFICATION.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
(OUT/'MANIFEST.json').write_text(json.dumps(sources,indent=2),encoding='utf-8')
body='''<h1>Nuova 772, calendario comune e 775</h1><p>Confronto dei 22 KPI per 30 giorni, sui due seed 180911301 e 180911303. La nuova 772 è la variante con <strong>8 mucche, 6 pecore e 2 oche</strong>; “comune” è l’esecuzione della sequenza nativa del rappresentante 107083439, con <strong>8 mucche, 6 pecore e 3 oche</strong>. La 775 è il bundle E18.2 congelato.</p><p>Ogni seed comprende due partite: nuova 772 contro 775 e comune contro 775. Nei grafici dei 22 KPI la linea 775 viene dalla partita contro la nuova 772; la comune viene dall’altra partita. Stesso seed, ma mercato diverso: non è una partita a tre. I prezzi sono mostrati separatamente per i due mercati.</p>'''
body+=table(['Seed','Versione','Cassa finale','Cassa avversaria','Mucche/pecore/oche','Perdite colture'],summary)
body+='''<h2>Diversificazione e prezzi</h2><p>L’ipotesi da verificare è che distribuire le vendite fra prodotti e giorni riduca la pressione sul singolo mercato. Qui separiamo tre grandezze: caselle/specie presenti nei 22 KPI; incassi giornalieri per prodotto; prezzi osservati nei due mercati. Una coltura presente non implica una vendita nello stesso giorno.</p><p>I grafici delle vendite mostrano incassi, non quantità, ed escludono il fertilizzante; il CSV MARKET contiene anche le quantità vendute da entrambi i giocatori e la disponibilità del mercato. I ricavi dipendono sia dai volumi sia dai prezzi. Questi replay permettono di osservare le associazioni, ma non isolano causalmente l’effetto della diversificazione: cambiano anche i volumi, le specie, l’esecuzione e le vendite avversarie.</p><p>I 12 meloni della nuova 772 e della comune coincidono fino alla raccolta a D11: il conteggio a fine D11 è zero. Le linee hanno stili distinti e il pannello segnala esplicitamente la sovrapposizione. MOVE/PASS sono comandi richiesti; WATER/FEED/CARE sono azioni riuscite. I KPI riguardano tutta la fattoria.</p>'''
for seed in images:
 body+=f'<section id="seed{seed}"><h2>Seed {seed} · 22 KPI</h2><img src="KPI22_{seed}.png" alt="22 KPI seed {seed}"><h2>Seed {seed} · calendario degli incassi</h2><img src="SALES_{seed}.png" alt="Vendite per prodotto"><h2>Seed {seed} · prezzi nei due mercati</h2><img src="PRICES_{seed}.png" alt="Prezzi per prodotto"></section>'
body+='<p><a href="KPI22.csv">22 KPI CSV</a> · <a href="MARKET.csv">Vendite, prezzi e scorte mercato CSV</a> · <a href="VERIFICATION.json">Verifiche</a> · <a href="MANIFEST.json">Provenienza e hash replay</a></p>'
(OUT/'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>22 KPI — nuova 772, comune, 775</title><style>body{font:17px/1.5 system-ui;color:#243746;max-width:1250px;margin:40px auto;padding:20px}img{width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:9px;border-bottom:1px solid #ccd6df;text-align:left}th{background:#edf4f7}h1,h2{color:#006582}</style>'+body+'</html>',encoding='utf-8')
print(json.dumps(summary,indent=2))
