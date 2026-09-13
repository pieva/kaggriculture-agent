"""Occupied species tiles and empty structures across same-submission replays."""
import csv
import json
from collections import Counter
from pathlib import Path

OUT=Path(__file__).resolve().parents[1]/'reports/opponent_strategy_20260913'
SPECIES=['COW','SHEEP','GOOSE','MELON','STRAWBERRY','TOMATO','WHEAT','CARROT']


def main():
    v=json.loads((OUT/'VARIABILITY.json').read_text(encoding='utf-8'));rows=[];summaries=[]
    for g in v['groups']:
        for member,days in zip(g['members'],g['daily']):
            for d in days:
                counts=Counter(t[2] for t in d['animals']+d['crops'])
                occupied={(t[0],t[1]) for t in d['animals']}
                counts['ANIMALS_TOTAL']=len(d['animals']);counts['CROPS_TOTAL']=len(d['crops'])
                counts['PASTURE']=sum(t[2]=='PASTURE' for t in d['topology'])
                counts['COOP']=sum(t[2]=='COOP' for t in d['topology'])
                counts['EMPTY_PASTURE']=sum(t[2]=='PASTURE' and (t[0],t[1]) not in occupied for t in d['topology'])
                counts['EMPTY_COOP']=sum(t[2]=='COOP' and (t[0],t[1]) not in occupied for t in d['topology'])
                d['counts']=dict(counts)
                for species in [*SPECIES,'ANIMALS_TOTAL','CROPS_TOTAL','PASTURE','COOP','EMPTY_PASTURE','EMPTY_COOP']:
                    positions=[t for t in d['animals']+d['crops'] if t[2]==species]
                    if species=='ANIMALS_TOTAL':positions=d['animals']
                    elif species=='CROPS_TOTAL':positions=d['crops']
                    elif species in ('PASTURE','COOP'):positions=[t for t in d['topology'] if t[2]==species]
                    elif species.startswith('EMPTY_'):positions=[t for t in d['topology'] if t[2]==species[6:] and (t[0],t[1]) not in occupied]
                    quadrants={f'Q{q}':sum(int(t[0]>=5)+2*int(t[1]>=5)==q for t in positions) for q in range(4)}
                    rows.append(dict(name=g['name'],submission=g['submission'],episode=member['episode'],day=d['day'],
                                     species=species,tiles=counts[species],**quadrants))
        summaries.append(dict(name=g['name'],d20={s:[d[19]['counts'].get(s,0) for d in g['daily']] for s in [*SPECIES,'ANIMALS_TOTAL','PASTURE','COOP']}))
    with (OUT/'SPECIES_TILES.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (OUT/'SPECIES_SUMMARY.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    payload=json.dumps(v['groups'],ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    (OUT/'SPECIES_VARIABILITY.html').write_text(TEMPLATE.replace('__DATA__',payload),encoding='utf-8')


TEMPLATE='''<!doctype html><html lang="it"><meta charset="utf-8"><title>E22 · Variabilità per specie</title><style>body{font:16px system-ui;max-width:1280px;margin:30px auto;padding:0 24px;background:#f4f5f0;color:#223329}section{padding:22px;background:white;border-radius:12px;margin:20px 0}select{font:inherit;padding:10px}table{border-collapse:collapse;width:100%}td,th{padding:9px;text-align:left;border-bottom:1px solid #d9dfd9}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.plot{background:white;border:1px solid #d9dfd9;padding:14px;border-radius:8px}svg{width:100%;height:auto}.maps svg{max-width:260px}.muted{color:#58685e}a{color:#197b67}@media(max-width:850px){.grid{grid-template-columns:1fr}}input{width:300px}</style>
<h1>E22 · Mix e numero di caselle per specie</h1><p><a href="REPORT.html">Confronto E20.9 e sconfitte</a> · <a href="SPECIES_TILES.csv">Serie complete CSV</a></p><p>Tre replay della stessa submission per cinque avversari. Le linee distinguono le partite, non modelli diversi. Ogni punto misura le caselle occupate a fine giornata: animali vivi, colture presenti e strutture vuote sono separati.</p>
<select id="model"></select><div id="content"></div><script>const groups=__DATA__,species=['COW','SHEEP','GOOSE','MELON','STRAWBERRY','TOMATO','WHEAT','CARROT'],colors=['#197b67','#b24c34','#5b64ae'];const sc={COW:'#577bac',SHEEP:'#ad85bb',GOOSE:'#8ccac3',MELON:'#dfa820',STRAWBERRY:'#e35d73',TOMATO:'#bc3c2a',WHEAT:'#c6a96b',CARROT:'#ef8d34',PASTURE:'#bad0ac',COOP:'#978069'};const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function plot(g,s){const values=g.daily.map(ds=>ds.map(d=>d.counts[s]||0)),max=Math.max(1,...values.flat());return `<div class="plot"><b>${s}</b><svg viewBox="0 0 330 150"><text x="3" y="15" font-size="11">${max} tile</text><path d="M12 125H320" stroke="#ccd6ce"/>${values.map((v,k)=>`<polyline points="${v.map((x,i)=>`${12+i*308/29},${125-x/max*100}`).join(' ')}" stroke="${colors[k]}" stroke-width="2" fill="none"/>`).join('')}<text x="12" y="145" font-size="11">D1</text><text x="298" y="145" font-size="11">D30</text></svg></div>`}
function map(d){let cells=new Map();for(const t of [...d.topology,...d.crops,...d.animals])cells.set(`${t[0]},${t[1]}`,t);return `<svg viewBox="0 0 200 200">${Array.from({length:100},(_,i)=>{const x=i%10,y=Math.floor(i/10),t=cells.get(`${x},${y}`);return `<rect x="${x*20}" y="${y*20}" width="19" height="19" fill="${t?sc[t[2]]:'#eee9de'}"><title>${x},${y}: ${t?t[2]:'altro'}</title></rect>`}).join('')}</svg>`}
function updateDay(){const g=groups[document.getElementById('model').value],day=Number(document.getElementById('day').value);document.getElementById('daylabel').textContent=`D${day}`;const names=[...species,'ANIMALS_TOTAL','CROPS_TOTAL','PASTURE','COOP','EMPTY_PASTURE','EMPTY_COOP'];document.getElementById('snapshot').innerHTML=`<div class="grid maps">${g.members.map((m,k)=>`<div><b style="color:${colors[k]}">Replay ${m.episode}</b><p>${esc(m.teams.join(' / '))}</p>${map(g.daily[k][day-1])}</div>`).join('')}</div><table><tr><th>Specie / struttura</th>${g.members.map((m,k)=>`<th style="color:${colors[k]}">${m.episode}</th>`).join('')}<th>Intervallo</th></tr>${names.map(s=>{const a=g.daily.map(ds=>ds[day-1].counts[s]||0);return `<tr><td>${s}</td>${a.map(n=>`<td>${n}</td>`).join('')}<td>${Math.min(...a)}–${Math.max(...a)}</td></tr>`}).join('')}</table>`}
function show(){const g=groups[document.getElementById('model').value];document.getElementById('content').innerHTML=`<section><h2>${esc(g.name)} · submission ${g.submission}</h2><p>${g.members.map((m,k)=>`<span style="color:${colors[k]}">■</span> <a href="https://www.kaggle.com/competitions/episodes/${m.episode}/replay.json">${m.episode}</a>${m.focal?' contro E20.9':''}`).join(' · ')}</p><p class="muted">Le curve sovrapposte possono coprirsi: la tabella riporta tutti i conteggi esatti. Lo sfondo chiaro delle mappe rappresenta le altre caselle senza distinguere terreno bloccato e vuoto.</p><h3>Animali: occupazione per specie e capacità costruita</h3><div class="grid">${['COW','SHEEP','GOOSE','ANIMALS_TOTAL','PASTURE','COOP'].map(s=>plot(g,s)).join('')}</div><h3>Colture: numero di caselle per specie</h3><div class="grid">${['MELON','STRAWBERRY','TOMATO','WHEAT','CARROT','CROPS_TOTAL'].map(s=>plot(g,s)).join('')}</div><h3>Confronto spaziale e conteggi del giorno</h3><label id="daylabel">D20</label> <input id="day" type="range" min="1" max="30" value="20"><p>${Object.entries(sc).map(([s,c])=>`<span style="color:${c}">■</span> ${s}`).join(' · ')}</p><div id="snapshot"></div></section><p class="muted">Tre partite per modello: differenze osservate, non prova della causa della scelta. Numero di animali, mortalità/fughe, mancati collocamenti e caselle colturali perse richiedono verifica degli eventi. Queste serie non stimano la produzione venduta: i volumi e prezzi sono nel dossier economico delle partite E20.9.</p>`;document.getElementById('day').addEventListener('input',updateDay);updateDay()}
document.getElementById('model').innerHTML=groups.map((g,i)=>`<option value="${i}">${esc(g.name)}</option>`).join('');document.getElementById('model').addEventListener('change',show);show();</script></html>'''


if __name__=='__main__':main()
