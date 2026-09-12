"""Summarize technical checks and cash ledgers; render 22 daily KPI paths."""
import csv,hashlib,html,json,sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from markdown_it import MarkdownIt
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[3];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.build_assisted_complete_kpi import FIELDS

def main():
    out=BASE/'reports/repair774_v2'
    checks=json.loads((out/'VERIFICATION.json').read_text())
    old=json.loads((BASE/'artifacts/fixed774/Fixed774_E18_180911301.kpi.json').read_text())['sides'][0]
    match=json.loads((BASE/'artifacts/repair774_v2/Repair774_E18_180911301.kpi.json').read_text())
    new,control=match['sides']
    profiles=[('774 prima',old),('774 corretta R2',new),('775 nello stesso match R2',control)]
    fig,axes=plt.subplots(6,4,figsize=(18,22),layout='constrained')
    fig.suptitle('774 prima e dopo le correzioni · 22 KPI · seed esposto 180911301\n775: avversaria della corretta; la prima 774 proviene dal match precedente',fontsize=17)
    for ax,(key,label,unit) in zip(axes.flat,FIELDS):
        for (name,p),color in zip(profiles,['#999999','#2465b0','#c17a24']):
            ax.plot(range(1,31),[d[key] for d in p['kpi']],label=name,color=color,lw=1.8)
        ax.set_title('Caselle coltivate' if key=='crop_tiles' else label,fontsize=10);ax.grid(alpha=.2);ax.set_xlim(1,30)
        ax.set_xlabel('Giorno');ax.set_ylabel(unit)
    axes.flat[22].axis('off');axes.flat[23].axis('off')
    handles,labels=axes.flat[0].get_legend_handles_labels()
    axes.flat[22].legend(handles,labels,loc='center',fontsize=9,frameon=False)
    fig.savefig(out/'KPI22.png',dpi=110);plt.close(fig)
    with (out/'KPI22.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['model','day']+[k for k,_,_ in FIELDS]);w.writeheader()
        for name,p in profiles:
            for d in p['kpi']:w.writerow({'model':name,'day':d['day'],**{k:d[k] for k,_,_ in FIELDS}})
    rows=[]
    for r in checks:
        rows.append(f"| {r['source'].split('_')[-1][:-5]} | {r['seat']} | {r['reward']:,.0f} | {r['opponent_reward']:,.0f} | {r['margin']:+,.0f} | {'PASS' if all(r['checks'].values()) else 'FAIL'} |")
    def total(p,key):return sum(sum(d[key].values()) for d in p['ledger']['daily'])
    def product(p,key,item):return sum(d[key].get(item,0) for d in p['ledger']['daily'])
    cash={'delta_cash':new['reward']-old['reward'],
          'delta_sales':total(new,'sales_cash')-total(old,'sales_cash'),
          'delta_purchases':total(new,'purchase_cash')-total(old,'purchase_cash')}
    cash['other_net']=cash['delta_cash']-cash['delta_sales']+cash['delta_purchases']
    cash['by_product']={item:{'sales_delta':product(new,'sales_cash',item)-product(old,'sales_cash',item),
                                    'old_harvest':product(old,'harvested',item),'new_harvest':product(new,'harvested',item)}
                        for item in ['WHEAT','MELON','STRAWBERRY','MILK','WOOL','EGG','FERTILIZER']}
    (out/'CASH_COMPARISON.json').write_text(json.dumps(cash,indent=2)+'\n')
    all_ok=all(all(r['checks'].values()) for r in checks)
    report=f'''# Correzioni 774 e verifica successiva

Versione: **CODEX-E21-774-REPAIR2**. Esito tecnico: **{'PASS' if all_ok else 'FAIL'}** su {len(checks)} partite seriali, seed esposti 180911301 e 180911303, entrambi i ruoli. Nessuna pubblicazione effettuata. Nessun seed riservato consumato.

## Correzioni effettive

1. **Acquisti e collocamenti:** cap di 17 bovini/ovini, obiettivo 8 mucche + 9 pecore, oltre a un'oca. Il pascolo Q1 (6,3) resta vuoto; la missione di completamento può riempire Q2. Verificati portafoglio finale esatto e zero animali inutilizzati in tutti i casi.
2. **Routine:** le escursioni prive di lavoro agricolo sul target (4,7) vengono saltate e sostituite da una tratta verso la successiva tappa originaria. Il suo orario resta un vincolo verificato. Il tempo disponibile può servire colture sul posto; non viene aperta un'altra tratta. Gli altri segmenti del piano possono comunque reagire alla fattoria modificata: non è una misura isolata del valore di una pecora.
3. **Identificazione:** modello E21-774-REPAIR2 e topologia 7-7-4 nei metadati; bundle e protocolli distinti dalla 774 ricostruita del report precedente.

## Altri difetti trovati e risolti durante il controllo

La prima correzione R1 comprava il numero giusto di pecore ma ne lasciava una nel deposito e il pascolo (3,6) vuoto. È conservata come tentativo fallito. R2 ripristina una missione di collocamento limitata, escludendo il pascolo Q1 che deve rimanere vuoto.

R1 ha inoltre evidenziato una risemina sul target senza acqua successiva, già presente nel comportamento ereditato. R2 ammette la semina quando un lavoratore presente ha uno slot compatibile nel turno seguente; il filtro agricolo usa quello slot per WATER. Nei replay verificati tutte le semine riuscite sul target sono seguite da acqua e non si osservano morti per sete su quella casella. Questa regola prudente può rinunciare a semine: non è ancora un pianificatore ottimale del ciclo completo.

Nel finale la gestione E18 di trasporto/consegna resta autorevole: il filtro non può sostituirla con compiti agricoli. Restano le protezioni contro costruzioni/collocamenti animali sul target. Normalizzato anche il campo opzionale `step` dai dati giorno/ora.

## Verifiche

719 chiamate per partita, riproduzione esatta dall'ingresso pubblico, reset episodio, nessun errore/fallback rilevato anche nei controller annidati, prefisso D1–D11 identico alla versione congelata, topologia massima e finale 774, massimo 18 animali, portafoglio finale 8/9/1, zero scorte animali, zero comandi animali sul target, rientri di tutte le tratte completati, contabilità di cassa riconciliata e zero fughe. Dettagli in VERIFICATION.json.

| Seed | Ruolo 774 | Cassa 774 R2 | Cassa E18 | Margine | Verifiche |
|---|---:|---:|---:|---:|---|
{chr(10).join(rows)}

Questi sono controlli diagnostici su seed già esposti. I ruoli non sono repliche indipendenti. Non dimostrano una superiorità competitiva.

## Effetti economici e limiti rimasti

Sul seed 301, ruolo 0, la vecchia ricostruzione faceva {old['reward']:,.0f}; R2 fa {new['reward']:,.0f}, variazione {cash['delta_cash']:+,.0f}. La variazione deriva da vendite {cash['delta_sales']:+,.0f}, acquisti {cash['delta_purchases']:+,.0f} (una riduzione è un risparmio) e altri flussi netti {cash['other_net']:+,.0f}. La 775 avversaria cambia anch'essa risultato tra i due match. Il motore accoppia infestanti e calendario dei negozi tramite RNG condiviso: non attribuire tutta la differenza al minor allevamento. Quantità e ricavi per prodotto sono in CASH_COMPARISON.json.

La copertura delle altre colture resta un limite della routine ereditata: nei due ruoli del seed 301 non è stato introdotto un pianificatore biologico generale. Nel ruolo 0 si rilevano {len(new['crop_starvation'])} eventi di perdita per sete, contro {len(old['crop_starvation'])} della precedente 774 e {len(control['crop_starvation'])} della 775 nello stesso nuovo match. Le correzioni tecniche non garantiscono un aumento della cassa.

**Conclusione operativa:** le correzioni richieste sono verificate come baseline diagnostica; pubblicazione non eseguita e nessuna promozione competitiva automatica. Non avviare ulteriori varianti economiche soltanto per recuperare il risultato sul campione.

## Traiettorie dei 22 KPI

![22 KPI](KPI22.png)

Dati giornalieri in KPI22.csv. L'originale e R2 provengono da match distinti; la curva 775 è l'avversaria di R2. Il precedente report 774/772/775 e il suo bundle non sono stati sovrascritti.
'''
    (out/'REPORT.md').write_text(report,encoding='utf-8')
    document='<!doctype html><meta charset="utf-8"><title>774 corretta — verifica</title><style>body{max-width:1100px;margin:40px auto;font:17px/1.5 system-ui;padding:0 20px;color:#223}h1,h2{color:#17456e}td,th{padding:8px 16px;border-bottom:1px solid #ddd;text-align:right}th:first-child,td:first-child{text-align:left}img{width:100%}code{font-size:.88em}a{color:#2465b0}</style>'+MarkdownIt().enable('table').render(report)
    (out/'REPORT.html').write_text(document,encoding='utf-8')
    paths=[BASE/'artifacts/repaired774_v2.py',BASE/'REPAIR774_V2_PROTOCOL.json',BASE/'REPAIR774_V2_180911303_PROTOCOL.json',out/'VERIFICATION.json',out/'REPORT.md',out/'REPORT.html',out/'KPI22.csv',out/'KPI22.png']
    (out/'MANIFEST.json').write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n')
    print(out/'REPORT.md')

if __name__=='__main__':main()
