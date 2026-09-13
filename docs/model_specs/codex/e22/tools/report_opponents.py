"""Build comparison tables and a self-contained visual replay dossier."""
import csv
import html
import json
from collections import Counter,defaultdict
from pathlib import Path
from statistics import mean,median

ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e22/reports/opponent_strategy_20260913'
PRODUCTS=['MELON','STRAWBERRY','TOMATO','WHEAT','CARROT','MILK','WOOL','EGG','FERTILIZER']


def geometry(p,day=20):
    cells=p['topology'][day-1]
    return '/'.join(str(sum(t['kind']=='PASTURE' and int(t['x']>=5)+2*int(t['y']>=5)==q for t in cells)) for q in range(4))


def net(d):return sum(d['sales_cash'].values())-sum(d['purchase_cash'].values())-d['hire_cash']-d['land_cash']+d['unit_cash_delta']


def compact(p):
    return dict(daily=p['daily'],kpi=p['kpi'],maps=p['maps'],ledger=p['ledger']['daily'],totals=p['totals'],terminal=p['terminal'],
                land_days=p['land_days'],losses=p['crop_starvation'])


def main():
    cohort=json.loads((OUT/'COHORT.json').read_text(encoding='utf-8'))
    games=[json.loads((OUT/'profiles'/f"{g['episode']}.json").read_text(encoding='utf-8')) for g in cohort['games']]
    assert len(games)==len(cohort['games'])
    losses=[g for g in games if g['outcome']=='loss']
    rows=[]
    for g in games:
        p=g['opponent'];d=p['daily'][19]
        rows.append(dict(episode=g['episode'],opponent=g['name'],opponent_rating=g['rating'],outcome=g['outcome'],
                         own_cash=g['own_cash'],opponent_cash=g['opponent_cash'],margin=g['margin'],pastures_D20=geometry(p),
                         coops_D20=sum(t['kind']=='COOP' for t in p['topology'][19]),
                         **{k:d['animals'][k] for k in ['COW','SHEEP','GOOSE']},
                         crop_tiles_D20=d['crop_tiles'],strawberry_D20=d['crops']['STRAWBERRY'],wheat_D20=d['crops']['WHEAT'],
                         people_D20=d['people'],land_days=','.join(map(str,p['land_days'])),crop_losses=len(p['crop_starvation']),
                         hire_cash=p['totals']['hire_cash'],land_cash=p['totals']['land_cash']))
    with (OUT/'OPPONENTS.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    groups=defaultdict(list)
    for g in games:groups[geometry(g['opponent'])].append(g)
    group_summary=[]
    for key,gs in groups.items():
        group_summary.append(dict(topology=key,n=len(gs),own_losses=sum(g['outcome']=='loss' for g in gs),
                                  mean_rating=mean(g['rating'] for g in gs),mean_margin=mean(g['margin'] for g in gs),
                                  names=[g['name'] for g in gs]))
    phase_rows=[]
    for label,lo,hi in [('D1-6',0,6),('D7-11',6,11),('D12-19',11,19),('D20-29',19,29),('D30',29,30)]:
        values={}
        for side in ['own','opponent']:
            values[side]={key:mean(sum(fn(d) for d in g[side]['ledger']['daily'][lo:hi]) for g in losses)
                          for key,fn in [('net',net),('sales',lambda d:sum(d['sales_cash'].values())),
                            ('purchases',lambda d:sum(d['purchase_cash'].values())),('hire',lambda d:d['hire_cash'])]}
        phase_rows.append(dict(phase=label,**values,gap=values['opponent']['net']-values['own']['net']))
    product_rows=[]
    for product in PRODUCTS:
        row=dict(product=product)
        for side in ['own','opponent']:
            units=sum(g[side]['totals']['sold_units'].get(product,0) for g in losses)
            revenue=sum(g[side]['totals']['sales_cash'].get(product,0) for g in losses)
            row[side]=dict(units=units/len(losses),revenue=revenue/len(losses),price=revenue/units if units else None)
        product_rows.append(row)
    pairs=[]
    for i,a in enumerate(losses):
        for b in losses[i+1:]:
            ca=a['opponent']['commands'];cb=b['opponent']['commands']
            eq=sum(x==y for x,y in zip(ca,cb))
            pairs.append(dict(a=a['name'],b=b['name'],episode_a=a['episode'],episode_b=b['episode'],
                              worker_frame_equal=eq,share=eq/719,opening_equal=sum(x==y for x,y in zip(ca[:144],cb[:144]))))
    summary=dict(n=len(games),wins=len(games)-len(losses),losses=len(losses),
                 rating_current=games[-1]['own_rating_after'],peak=max(g['own_rating_after'] for g in games),
                 loss_opponent_rating_range=[min(g['rating'] for g in losses),max(g['rating'] for g in losses)],
                 mean_loss=mean(-g['margin'] for g in losses),median_loss=median(-g['margin'] for g in losses),
                 groups=group_summary,phases=phase_rows,products=product_rows,pairs=sorted(pairs,key=lambda x:-x['share']),
                 loss_details=[r for r in rows if r['outcome']=='loss'])
    (OUT/'SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    payload=[dict(episode=g['episode'],name=g['name'],rating=g['rating'],outcome=g['outcome'],margin=g['margin'],
                  own=compact(g['own']),opponent=compact(g['opponent'])) for g in sorted(games,key=lambda g:(g['outcome']!='loss',g['margin']))]
    data=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    table=''.join('<tr>'+''.join(f'<td>{html.escape(str(round(r[k],1) if k=='opponent_rating' else r[k]))}</td>' for k in ['opponent','episode','opponent_rating','margin','pastures_D20','coops_D20','COW','SHEEP','GOOSE','people_D20','land_days'])+'</tr>' for r in summary['loss_details'])
    variability=json.loads((OUT/'VARIABILITY.json').read_text(encoding='utf-8'))
    vrows=[]
    for group in variability['groups']:
        rates=[p['identical_worker_frames']/719*100 for p in group['pairs']]
        compositions=[' / '.join(str(sum(a[2]==species for a in d['animals'])) for species in ['COW','SHEEP','GOOSE']) for d in group['d20']]
        vrows.append('<tr><td>'+html.escape(group['name'])+'</td><td>'+str(group['submission'])+'</td><td>'+f'{min(rates):.1f}–{max(rates):.1f}%'+'</td><td>'+'; '.join(compositions)+'</td></tr>')
    page=TEMPLATE.replace('__TABLE__',table).replace('__DATA__',data).replace('__VARIABILITY__',''.join(vrows))
    (OUT/'REPORT.html').write_text(page,encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ['pairs','loss_details']},ensure_ascii=True,indent=2))


TEMPLATE='''<!doctype html><html lang="it"><meta charset="utf-8"><title>E22 Â· Avversari E20.9</title>
<style>body{font:15px system-ui;background:#f2f4f0;color:#202e29;margin:28px auto;max-width:1320px;padding:0 20px}h1{font-size:32px}h2{margin-top:30px}table{border-collapse:collapse;width:100%;font-size:13px}td,th{border-bottom:1px solid #ccd6ce;padding:8px;text-align:left}section,.card{background:white;padding:20px;border-radius:10px;margin:18px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}.charts{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.muted{color:#53645c}select{padding:10px;max-width:100%;font:inherit}svg{max-width:100%;height:auto}label{font-weight:600}.map{width:220px}.legend{font-size:12px;margin:8px 0}small{display:block;color:#53645c}a{color:#186b50}@media(max-width:900px){.charts,.grid{grid-template-columns:1fr}}.overflow{overflow:auto}</style>
<h1>E22 Â· Come ci battono gli avversari</h1><p>Submission E20.9 / 56202079 Â· storico congelato il 13 settembre 2026 Â· 33 partite, 15 sconfitte, 18 vittorie.</p>
<p class="muted">Nessuna topologia o pianificazione imposta. Confronto descrittivo: rating prima della partita e cassa sono misure distinte. Gli avversari delle sconfitte sono sotto 1700: questo campione non dimostra un percorso sufficiente a 2000.</p>
<p><a href="REPORT.md">Conclusioni e ipotesi</a> · <a href="SPECIES_VARIABILITY.html">Mix e caselle per specie</a> Â· <a href="OPPONENTS.csv">Tabella CSV</a> Â· <a href="SUMMARY.json">Dati aggregati</a></p>
<section><h2>Cosa emerge</h2><p>14 avversari su 15 espandono a D7 e D12; 13 usano a D20 pascoli 10/7 oppure 7/7 nei quadranti settentrionali. Tre avversari diversi emettono gli stessi 719 gruppi di comandi dei lavoratori. La flessibilità non è una spiegazione unica delle sconfitte.</p><p>Nelle sconfitte il divario netto medio nasce soprattutto a D7–D11 (+5716 per l'avversario) e D20–D29 (+5354). Fragole vendute: 255 contro 216; prezzo medio ponderato 147,2 contro 146,3. Sono differenze descrittive, non effetti causali isolati.</p></section>
<section><h2>Variabilità della stessa submission</h2><p>Tre replay per ciascuno di cinque rappresentanti esplorativi: sconfitta contro E20.9 e due precedenti partite pubbliche. Coincidenza dei gruppi di comandi dei lavoratori fra le tre coppie di replay; composizione animale C/S/G a D20. Una differenza può derivare da scelta, mercato, infestanti o fallimento operativo.</p><table><tr><th>Avversario</th><th>Submission</th><th>Comandi identici</th><th>Animali nei tre replay</th></tr>__VARIABILITY__</table><p>s56165462: geometria e colture identiche per tutti i giorni. Denis: geometria stabile, mix animale variabile. Sam-wiz: configurazioni animali alternative, colture molto simili. Rheinmetall: variabilità estesa. EnricRovira: differenze anche da perdite di animali precoci.</p><a href="VARIABILITY.json">Fonti e confronti delle tre repliche</a></section>
<section><h2>Le 15 sconfitte</h2><p>Pascoli per quadrante Q0/Q1/Q2/Q3 a D20; pollai separati. C/S/G = mucche/pecore/oche. Lavoratori inclusivo dell'agricoltore. Espansioni: giorni d'acquisto dei terreni.</p><div class="overflow"><table><thead><tr><th>Avversario</th><th>Episodio</th><th>Rating</th><th>Margine nostro</th><th>Pascoli</th><th>Pollai</th><th>C</th><th>S</th><th>G</th><th>Lavoratori</th><th>Espansioni</th></tr></thead><tbody>__TABLE__</tbody></table></div></section>
<section><h2>Dossier della partita</h2><select id="game"></select><div id="detail"></div></section>
<script>const games=__DATA__;
const colors={MELON:'#dfa820',STRAWBERRY:'#e35d73',TOMATO:'#bc3c2a',WHEAT:'#c6a96b',CARROT:'#ef8d34',COW:'#577bac',SHEEP:'#ad85bb',GOOSE:'#8ccac3',WEED:'#b3c3a1',PASTURE:'#8bb36f',COOP:'#978069'};
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=x=>x==null?'â€”':Number(x).toLocaleString('it-IT',{maximumFractionDigits:1});
function chart(a,b,title){const vals=[...a,...b].filter(x=>x!=null),max=Math.max(1,...vals),min=Math.min(0,...vals),W=360,H=75;function line(v,c){let pts=v.map((x,i)=>x==null?null:`${8+i*344/29},${H-8-(x-min)/(max-min)*56}`).filter(x=>x!=null).join(' ');return `<polyline points="${pts}" fill="none" stroke="${c}" stroke-width="2"/>`};return `<small>${title} Â· max ${fmt(max)}</small><svg viewBox="0 0 ${W} ${H+16}"><path d="M8 67H352" stroke="#ccd6ce"/>${line(a,'#197b67')}${line(b,'#b24c34')}<text x="8" y="87" font-size="10">D1</text><text x="330" y="87" font-size="10">D30</text></svg>`}
function map(p,d){const cells=p.maps[d-1];return `<svg class="map" viewBox="0 0 210 225"><text x="0" y="12" font-size="12">D${d}</text>${Array.from({length:100},(_,i)=>`<rect x="${i%10*20}" y="${20+Math.floor(i/10)*20}" width="19" height="19" fill="#eee9de"/>`).join('')}${cells.map(c=>`<rect x="${c.x*20}" y="${20+c.y*20}" width="19" height="19" fill="${colors[c.animal||c.crop||c.kind]||'#ddd'}"><title>${c.x},${c.y}: ${esc(c.animal||c.crop||c.kind)}</title></rect>`).join('')}<rect x="80" y="100" width="40" height="40" fill="none" stroke="#222" stroke-width="2"/></svg>`}
function show(){const g=games[document.getElementById('game').value],o=g.own,p=g.opponent;document.getElementById('detail').innerHTML=`<h2>${esc(g.name)} Â· rating ${fmt(g.rating)}</h2><p><a href="https://www.kaggle.com/competitions/episodes/${g.episode}/replay.json">Replay ${g.episode}</a> Â· cassa nostra ${fmt(o.terminal.cash)}, avversaria ${fmt(p.terminal.cash)} Â· margine ${fmt(g.margin)}</p><p class="legend">Linee: <b style="color:#197b67">E20.9</b> / <b style="color:#b24c34">avversario</b>. Fotografie giornaliere a H24; vendite aggregate per giorno di azione.</p><div class="grid"><div>${chart(o.daily.map(x=>x.money),p.daily.map(x=>x.money),'Cassa')}${chart(o.daily.map(x=>x.people),p.daily.map(x=>x.people),'Lavoratori')}</div><div><h3>Economia del mese</h3><table><tr><th></th><th>E20.9</th><th>Avversario</th></tr>${[['Vendite','sales_cash'],['Acquisti','purchase_cash'],['Lavoro','hire_cash'],['Terreni','land_cash']].map(([l,k])=>`<tr><td>${l}</td>${[o,p].map(s=>`<td>${fmt(typeof s.totals[k]==='object'?Object.values(s.totals[k]).reduce((a,b)=>a+b,0):s.totals[k])}</td>`).join('')}</tr>`).join('')}</table><p>Espansioni: E20.9 D${o.land_days.join(', D')}; avversario D${p.land_days.join(', D')}.</p><p>Perdite colturali verificate: ${o.losses.length} / ${p.losses.length}.</p></div></div><h3>Geometria e colture durante la partita</h3><p class="legend">${Object.entries(colors).map(([k,c])=>`<span style="color:${c}">â– </span> ${k}`).join(' Â· ')}. Bordo nero: accessi al deposito; sfondo chiaro: altre caselle, senza distinguere terreno bloccato e vuoto.</p><div class="grid"><div><b>E20.9</b><div>${[10,20,29].map(d=>map(o,d)).join('')}</div></div><div><b>Avversario</b><div>${[10,20,29].map(d=>map(p,d)).join('')}</div></div><h3>Portafoglio, volumi venduti e prezzi realizzati</h3><div class="charts">${['MELON','STRAWBERRY','TOMATO','WHEAT','CARROT','MILK','WOOL','EGG'].map(item=>{const species={MILK:'COW',WOOL:'SHEEP',EGG:'GOOSE'}[item];const stock=s=>s.daily.map(d=>species?d.animals[species]:d.crops[item]);const sales=s=>s.ledger.map(d=>d.sold_units[item]||0);const price=s=>s.ledger.map(d=>d.sold_units[item]?d.sales_cash[item]/d.sold_units[item]:null);return `<div class="card"><b>${item}</b>${chart(stock(o),stock(p),species?'Animali':'Caselle colturali')}${chart(sales(o),sales(p),'UnitÃ  vendute')}${chart(price(o),price(p),'Prezzo medio delle vendite Â· lacune senza vendite')}</div>`}).join('')}</div><p class="muted">Il prezzo medio non Ã¨ una quotazione costante; Ã¨ ricavo diviso unitÃ  effettivamente vendute. Il collegamento fra punti non implica vendite nei giorni senza osservazioni.</p>`}
document.getElementById('game').innerHTML=games.map((g,i)=>`<option value="${i}">${g.outcome==='loss'?'Sconfitta':'Vittoria'} Â· ${esc(g.name)} Â· ${fmt(g.margin)}</option>`).join('');document.getElementById('game').addEventListener('change',show);show();</script></html>'''


if __name__=='__main__':main()
