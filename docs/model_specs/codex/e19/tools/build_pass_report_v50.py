"""Publish local evidence, including failed development prototypes."""
import html,json,sys
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.analyze_pass_reduction_v50 import analyze,OUT,OLD


def table(headers,rows):
    return '<table><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</table>'


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    selected=sys.argv[1]
    variants=sorted({p.name.split('_')[1] for p in OUT.glob('development_v50*.json') if not p.name.endswith('_obligations.json')})
    summaries={v:analyze(v) for v in variants}
    selected_summary=summaries[selected]
    plots=OUT/'figures';plots.mkdir(exist_ok=True)
    qa=ROOT/'scratch/v50/figures';qa.mkdir(exist_ok=True)
    body='''<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V50 · PASS, risorse e organico</title><style>body{font:16px/1.5 system-ui;max-width:1280px;margin:auto;padding:30px;color:#20313a;background:#f5f7f8}h2{margin-top:38px}table{width:100%;border-collapse:collapse;background:white;margin:20px 0;font-size:14px}th,td{padding:9px;border-bottom:1px solid #d8e2e6;text-align:left}th{background:#dcebed}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}figure{margin:0;background:white;padding:10px}img{width:100%}.note{background:white;padding:18px;border-left:5px solid #007e80}code{overflow-wrap:anywhere}@media(max-width:750px){.grid{grid-template-columns:1fr}table{display:block;overflow:auto}}</style><h1>V50 · PASS, risorse e organico</h1>'''
    body+='<p>Confronto con V49F locale congelata. V48 pubblicata invariata. Nessuna nuova submission.</p>'
    body+='<div class="note">Variante in evidenza: '+html.escape(selected.upper())+'. Stato: '+html.escape(selected_summary['status'])+'. Lo sviluppo usa seed esposti; i prototipi respinti rimangono nel report. I gate economici, biologici e sui PASS restano distinti dal runtime standard e dalla validazione esterna.</div>'
    diagnostic=json.loads((OUT/'route_causality.json').read_text())
    body+='<h2>Diagnosi della prenotazione</h2><p>Replay esposto 106843637: 719/719 azioni V48 riprodotte anche con sonde offline. Le sonde provano la preparazione senza il solo filtro del percorso, nello stato dopo le assegnazioni reali. Non sono prove di redditività o di miglioramento della partita.</p>'
    body+=table(['Giorno','Visite sondate','Fattibili senza filtro','Slot PASS con almeno una visita fattibile'],[[d['day'],d['probes'],d['feasible'],d['pass_slots_with_feasible']] for d in diagnostic['days']])
    body+='<p>D12–D15 restano aperti. D29 richiede di distinguere risorse nel deposito, prelievi già impegnati e grano trasportato dai singoli lavoratori. Più manovali non rendono accessibile il grano già assegnato ad altri.</p>'
    rows=[]
    for v,s in summaries.items():
        d=s['partitions']['development'];m=d['mean_delta']
        rows.append([v,d['n'],round(m['cash'],3),round(m['pass_count'],3),round(m['share'],4),round(m['move'],3),', '.join(k for k,ok in d['gates'].items() if not ok) or 'superati sul campione'])
    body+='<h2>Tutti i prototipi di sviluppo</h2>'+table(['Variante','Coppie','Δ cassa','Δ PASS','Δ quota pp','Δ MOVE','Gate non superati'],rows)
    body+='<p>A–D e G esplorano certificati conservativi; E modifica il packing dei percorsi con scorte condivise; F combina E e D. H certifica servizi biologici e raccolte, escludendo lavoro facoltativo sul fertilizzante e usando il vincolo di rientro ereditato. I combina H con la rimozione della raccolta facoltativa; J combina H ed E; K combina H, E e I. Il certificato indica una distribuzione possibile e non obbliga il dispatcher a eseguirla: i replay verificano l’esito reale.</p>'
    for split,section in selected_summary['partitions'].items():
        body+='<h2>'+html.escape(split)+' · '+str(section['n'])+' coppie</h2>'
        body+=table(['Seed','Posto','Δ cassa','Δ PASS','Δ MOVE'],[[c['seed'],c['seat'],c['delta']['cash'],c['delta']['pass_count'],c['delta']['move']] for c in section['cases']])
        body+=table(['Gate','Esito'],[[k,'SUPERATO' if ok else 'NON SUPERATO'] for k,ok in section['gates'].items()])
        body+='<div class="grid">'
        for key,title in [('pass_count','PASS per giorno'),('share','PASS / slot (%)'),('move','MOVE per giorno'),('cash','Cassa H24'),('slots','Slot disponibili'),('hire_cash','Spesa assunzioni'),('FEED','FEED riusciti'),('CARE','CARE riusciti'),('WATER','WATER riusciti'),('HARVEST','HARVEST riusciti'),('crops','Colture H24'),('animals','Animali H24')]:
            fig,ax=plt.subplots(figsize=(6.2,3.2),layout='constrained')
            for v,color in [('v49f','#566573'),(selected,'#007e80')]:
                runs=[json.loads(((OLD if v=='v49f' and split=='development' else OUT)/f'{split}_{v}_{c["seed"]}_{c["seat"]}.json').read_text()) for c in section['cases']]
                series=[[d['pass_count']/d['slots']*100 if key=='share' else d['executed'].get(key,0) if key in {'FEED','CARE','WATER','HARVEST'} else d[key] for d in r['daily']] for r in runs]
                ax.plot(range(1,31),[mean(s[i] for s in series) for i in range(30)],label=v.upper(),color=color)
                ax.fill_between(range(1,31),[min(s[i] for s in series) for i in range(30)],[max(s[i] for s in series) for i in range(30)],color=color,alpha=.1)
            ax.set(title=title,xlabel='Giorno',xlim=(1,30));ax.legend(frameon=False);ax.grid(alpha=.2)
            name=f'{selected}_{split}_{key}'
            fig.savefig(plots/(name+'.svg'));fig.savefig(qa/(name+'.png'),dpi=120);plt.close(fig)
            body+=f'<figure><img src="figures/{name}.svg" alt="{title}"><figcaption>Media e min–max, stessi seed e posti.</figcaption></figure>'
        body+='</div>'
    runtimes=[json.loads(p.read_text()) for p in sorted(OUT.glob('runtime_*.json'))]
    body+='<h2>Runtime standard locale</h2>'+table(['Variante','Seed','Posto','Chiamate','Esito','Massimo s','Overage s'],[[r['variant'],r['seed'],r['seat'],r['calls'],r['passed'],round(r['max_seconds'],3),round(r['overage'],3)] for r in runtimes])
    body+='<p>Le matrici comportamentali usano actTimeout=120. Le prove runtime sono seriali, con actTimeout=1 e overage standard del motore. Nessuna equivalenza garantita con l’hardware Kaggle. I posti non sono repliche indipendenti. <a href="PROTOCOL_IT.md">Protocollo</a> · <a href="route_causality.json">Diagnosi</a> · <a href="summary_'+selected+'.json">Dati e deficit biologici per caso</a>.</p></html>'
    (OUT/'REPORT_V50_IT.html').write_text(body,encoding='utf-8')


if __name__=='__main__':main()
