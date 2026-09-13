import gzip,json,sys
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'docs/model_specs/codex/e22/tools'))
from e209_s56165462_charts import chart
def main():
    summary=[];allrows={}
    for version in ['v52a','v52b','v52c','v52d']:
        path=HERE/'reports'/version/'RESULTS.json'
        if not path.exists():continue
        rows=json.loads(path.read_text(encoding='utf-8'));allrows[version]=rows
        summary.append(dict(version=version,n=len(rows),mean_margin=mean(r['margin'] for r in rows),wins=sum(r['margin']>0 for r in rows),escapes=sum(len(r['ledger'][r['seat']]['animal_escapes']) for r in rows),candidate_labor=mean(sum(d['hire_cash'] for d in r['ledger'][r['seat']]['daily']) for r in rows),control_labor=mean(sum(d['hire_cash'] for d in r['ledger'][1-r['seat']]['daily']) for r in rows)))
    (HERE/'SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    intro='E22 pubblicata: submission 56206528, Complete. E19.2 riparte da E19 770 V51C. Il costo del lavoro spiega circa il 10% del precedente distacco: serve preservare e monetizzare la produzione mentre si riducono i costi.'
    descriptions='V52A estende i percorsi speciali D29 a D12–D29, ma penalizza crescita e fertilizzazione: respinta. V52B include fertilizzazione e protezione della crescita, ma presenta perdite animali in un seed: respinta. V52C mantiene esecutore e colture V51C; a D12–D29 il massimo ordinario scende da 12 a 11 e torna a 12 se animali non alimentati o colture stressate richiedono recupero. Il controllo originale decide comunque quante persone assumere sotto quel massimo. D1–D11 e D30 conservano il comportamento precedente.'
    descriptions+=' V52C perde tutti i quattro confronti: respinta. V52D conserva il limite originale e valuta le cure animali da D12: omette CARE se il bonus è saturo o non può più generare produzione. Tiene conto del consumo del bonus al prossimo aggiornamento, prima della registrazione della cura odierna. V52D respinta sul primo seed, in entrambi i ruoli: margine −1.699 e una fuga animale per partita; il secondo seed è stato annullato. Nessuna delle quattro varianti è promossa.'
    md='# E19.2 — sviluppo della 770 reattiva\n\n'+intro+'\n\n'+descriptions+'\n\n| Variante | Partite | Vittorie | Margine medio | Lavoro candidato / controllo | Fughe candidato |\n|---|---:|---:|---:|---:|---:|\n'+'\n'.join(f"|{s['version']}|{s['n']}|{s['wins']}|{s['mean_margin']:.1f}|{s['candidate_labor']:.1f} / {s['control_labor']:.1f}|{s['escapes']}|" for s in summary)
    md+='\n\n## Valutazione\n\nConfronti diretti contro V51C, due seed esposti, simulazioni seriali, registri economici verificati. Le varianti respinte rimangono documentate e non sono proposte per la pubblicazione. Il risparmio di lavoro deve essere valutato insieme a produzione venduta, sopravvivenza e cassa finale. V52C non introduce nuove rotazioni: conserva quelle di V51C; l’estensione colturale resta una prova separata, dopo il lavoro. Non trasferire automaticamente i due pomodori programmati di E20.9: non erano una selezione dinamica sui prezzi.\n\n[Grafici D1–D30](REPORT.html) · [Dati sintetici](SUMMARY.json). Nessuna E19.2 pubblicata.\n'
    (HERE/'REPORT.md').write_text(md,encoding='utf-8')
    body='<h1>E19.2 · 770 reattiva</h1><p>'+intro+'</p><p>'+descriptions+'</p><p><a href="https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56206528">E22 pubblicata</a> · <a href="REPORT.md">Metodo e limiti</a></p><section><h2>Esiti delle varianti</h2><ul>'+''.join(f"<li>{s['version']}: {s['wins']}/{s['n']} vittorie; margine medio {s['mean_margin']:,.1f}; lavoro {s['candidate_labor']:,.1f} contro {s['control_labor']:,.1f}; fughe {s['escapes']}.</li>" for s in summary)+'</ul></section>'
    rows=[r for version in ['v52c','v52d'] for r in allrows.get(version,[])]
    body+='<label>Variante e partita <select id="match">'+''.join(f'<option value="{i}">{r["candidate"].upper()} · Seed {r["seed"]}, ruolo {r["seat"]}</option>' for i,r in enumerate(rows))+'</select></label>'
    for i,r in enumerate(rows):
        seat=r['seat'];version=r['candidate'];ls=[r['ledger'][1-seat],r['ledger'][seat]];g=json.load(gzip.open(HERE/f'artifacts/{version}/{r["seed"]}_{seat}.replay.json.gz','rt',encoding='utf-8'))
        def series(fn):return [[fn(d) for d in l['daily']] for l in ls]
        def plot(t,s,u):return chart(t,s,u).replace('E20.9','E19 V51C').replace('s56165462','E19.2 '+version.upper())
        body+=f'<section data-i="{i}"'+(' hidden' if i else '')+f'><h2>{version.upper()} · Seed {r["seed"]} · ruolo {seat}</h2><p>Blu: V51C. Arancio: {version.upper()}. Margine candidato {r["margin"]:,.0f}.</p><div class="plots">'
        body+=plot('Cassa giornaliera',[[g['steps'][d*24-1][s]['observation']['farms'][s]['money'] for d in range(1,31)] for s in [1-seat,seat]],'monete')
        body+=plot('Costo lavoro',series(lambda d:d['hire_cash']),'monete/giorno')+plot('Assunzioni',series(lambda d:d['hires']),'persone/giorno')
        for item in ['STRAWBERRY','MELON','WOOL','MILK','WHEAT','CARROT','TOMATO']:
            body+=plot(item+' · venduto',series(lambda d:d['sold_units'].get(item,0)),'unità')
            body+=plot(item+' · prezzo realizzato',series(lambda d:d['sales_cash'].get(item,0)/d['sold_units'][item] if d['sold_units'].get(item,0) else None),'monete/unità')
            body+=plot(item+' · ricavi',series(lambda d:d['sales_cash'].get(item,0)),'monete')
        body+='</div></section>'
    body+='<script>document.getElementById("match").addEventListener("change",e=>document.querySelectorAll("section[data-i]").forEach(x=>x.hidden=x.dataset.i!==e.target.value));</script>'
    (HERE/'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>E19.2 770 reattiva</title><style>body{font:16px system-ui;max-width:1400px;margin:30px auto;padding:0 24px;background:#f3f5f0;color:#24332d}section{background:white;padding:24px;border-radius:12px;margin:20px 0}p{line-height:1.6}.plots{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.plot{border:1px solid #ddd;padding:12px;border-radius:8px;min-width:0}svg{width:100%}select{padding:10px;font:inherit}@media(max-width:850px){.plots{grid-template-columns:1fr}}</style>'+body+'</html>',encoding='utf-8');print(summary)
if __name__=='__main__':main()
