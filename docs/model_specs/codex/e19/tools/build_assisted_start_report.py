"""Evidence report for the bounded assisted-opening experiment."""
import base64
import hashlib
import json
import os
from pathlib import Path
from statistics import mean

ROOT=Path(__file__).resolve().parents[5]
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'scratch/matplotlib_kpi'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from markdown_it import MarkdownIt

BASE=ROOT/'docs/model_specs/codex/e19'
DATA=BASE/'artifacts/derived/assisted_start_20260907'
OUT=BASE/'reports/assisted_start_20260907'


def net(row):
    return sum(row['sales_cash'].values())-sum(row['purchase_cash'].values())-row['hire_cash']-row['land_cash']+row['unit_cash_delta']


def fmt(n):return f'{n:,.1f}'.replace(',','X').replace('.',',').replace('X','.')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    datasets={t:[json.loads((DATA/f'{t}_{s}_{p}.json').read_text()) for s in range(180903001,180903008) for p in (0,1)] for t in ('770','662')}
    old={t:[json.loads((BASE/'artifacts/derived/paired_kpi_v4d_20260907'/f'{t}_{s}_{p}.json').read_text()) for s in range(180903001,180903008) for p in (0,1)] for t in datasets}
    summary={}
    for t,cases in datasets.items():
        assert all(c['source_bundle_action_parity']==265 and not c['capacity_violations'] and c['handover_interface_pass'] for c in cases)
        summary[t]={}
        for label in ('assisted','v4d'):
            sides=[c['sides'][label] for c in cases]
            summary[t][label]=dict(
                cases=len(cases),d11_cash=mean(s['prefix_cash'] for s in sides),
                d11_net=mean(net(s['ledger']['daily'][10]) for s in sides),
                d11_melon_harvest=mean(s['ledger']['daily'][10]['harvested'].get('MELON',0) for s in sides),
                d11_melon_sold=mean(s['ledger']['daily'][10]['sold_units'].get('MELON',0) for s in sides),
                d11_melon_revenue=mean(s['ledger']['daily'][10]['sales_cash'].get('MELON',0) for s in sides),
                d10_strawberry=mean(s['daily'][9]['crops']['STRAWBERRY'] for s in sides),
                animal_escapes=sum(len(s['ledger']['animal_escapes']) for s in sides),
                min_melon_harvest=min(s['ledger']['daily'][10]['harvested'].get('MELON',0) for s in sides),
                max_melon_harvest=max(s['ledger']['daily'][10]['harvested'].get('MELON',0) for s in sides),
                d11_topologies=sorted(set(str(s['daily'][10]['pasture_topology']) for s in sides)))
        a=summary[t]['assisted'];b=summary[t]['v4d']
        summary[t]['paired_net_ratio']=a['d11_net']/b['d11_net']
        summary[t]['old_v2_net']=mean(net(c['sides']['parametric']['ledger']['daily'][10]) for c in old[t])
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    for col,t in enumerate(datasets):
        for label,name,color,style in [('assisted','Avvio assistito','#176b9b','-'),('v4d','V4D nella stessa partita','#d66a36','--')]:
            cases=datasets[t]
            axes[0,col].plot(range(1,12),[mean(c['sides'][label]['daily'][d]['settled_cash'] for c in cases) for d in range(11)],label=name,color=color,ls=style,lw=2.5)
            axes[1,col].plot(range(1,12),[mean(net(c['sides'][label]['ledger']['daily'][d]) for c in cases) for d in range(11)],label=name,color=color,ls=style,lw=2.5)
        for ax in axes[:,col]:
            ax.axvline(11,color='#999',alpha=.4);ax.grid(alpha=.2);ax.set_xlabel('Giorno');ax.set_xticks(range(1,12));ax.legend(fontsize=8)
        axes[0,col].set_title(f'{t} · cassa dopo tutti i batch del giorno')
        axes[1,col].set_title(f'{t} · variazione netta di cassa giornaliera')
    fig.savefig(OUT/'trend_d11.png',dpi=150);fig.savefig(OUT/'trend_d11.svg');plt.close(fig)
    text='''# Avvio assistito comune · E18 770 ed E19 662

## Obiettivo e natura della prova

Recuperare il raccolto e il salto di cassa di D11. La prima versione usa **V4D come guida esecutiva fino alla fine di D11**, con un filtro delle costruzioni basato sulle capacità del profilo. Da D12 subentra il core parametrico V2 comune, senza riavviare il bootstrap grano/carote. È una variante ibrida esplicita: il risultato non dimostra ancora che l’allocatore autonomo abbia imparato questa apertura.

Il riferimento operativo è la V4D campione; il precedente confronto V4C/Top770 ha fornito la lettura dell’apertura. Non viene eseguito il piano storico oltre D11.

## Risultati locali

14 partite per target: semi di sviluppo 180903001–180903007, entrambe le posizioni, contro V4D. Ogni partita conserva l’orizzonte del motore a 720 step e termina la misura dopo 264 batch, con tutti i flussi di D11 regolati. Non sono punteggi finali né benchmark esterni.

| KPI medio | 770 assistita | V4D contro 770 | 662 assistita | V4D contro 662 |
|---|---:|---:|---:|---:|
'''
    for key,title in [('d11_cash','Cassa a chiusura D11'),('d11_net','Delta netto di cassa D11'),('d11_melon_harvest','Meloni raccolti a D11, unità'),('d11_melon_sold','Meloni venduti a D11, unità'),('d11_melon_revenue','Ricavo meloni D11'),('d10_strawberry','Piante di fragola a D10')]:
        text+='| '+title+' | '+' | '.join(fmt(summary[t][label][key]) for t,label in [('770','assisted'),('770','v4d'),('662','assisted'),('662','v4d')])+' |\n'
    text+='\n![Cassa e delta di cassa D1–D11](trend_d11.png)\n\n'
    text+=f'''Il rapporto fra delta netto assistito e V4D **nella stessa partita** è {fmt(100*summary['770']['paired_net_ratio'])}% per 770 e {fmt(100*summary['662']['paired_net_ratio'])}% per 662. Nei precedenti test il delta D11 dei core V2 era rispettivamente {fmt(summary['770']['old_v2_net'])} e {fmt(summary['662']['old_v2_net'])}: quei numeri descrivono il vecchio avvio, ma provengono da mercati diversi.

Il ricavo storico di circa 14.797 sui meloni non è un importo invariabile da imporre: con due aperture produttive cambia il mercato. Qui ciascun lato vende 54 delle 72 unità raccolte entro D11, contro le 60 vendute dalla V4D nei precedenti confronti; cambiano quindi sia quantità monetizzata sia prezzi. Il criterio pertinente è conservare produzione e monetizzazione e confrontare il delta con V4D nello stesso mercato.

## Come funziona l’assistenza

- D1: portafoglio iniziale storico di 12 meloni e 7 grani, con 2 mucche e 2 pecore; la guida coordina acquisti, assunzioni e percorsi.
- D2–D10: servizi al ciclo iniziale, crescita degli animali e progressiva introduzione delle fragole secondo la guida, con limiti di pascolo osservati.
- D11: raccolta e vendita; il filtro impedisce i pascoli eccedenti e i pollai, estranei ai profili 770/662.
- D12: subentro del core comune su risorse e inventari realmente osservati. È verificata solo la prima chiamata dell’interfaccia, non la bontà economica della continuazione.

Il filtro riserva anche le costruzioni simultanee dello stesso batch. A 662 evita il settimo pascolo di Q1 e quello di Q0; a 770 questi rientrano nel budget. Non sono richiesti il completamento di 770/662 o l’espansione del terzo quadrante entro D11.

## Verifiche e limiti

- Banco di prova riconciliato con quattro prefissi già consolidati: entrambi i target e le posizioni, tutti i KPI e i flussi di entrambe le fattorie.
- 28 partite, 264 batch ciascuna: riconciliazione della cassa, vincoli di pascolo a ogni stato, parità di 265 azioni fra sorgente e file candidato, inclusa la prima chiamata D12.
- Tre test unitari: prenotazioni simultanee, capacità parametrica e confine del passaggio D11/D12.
- Sono semi di sviluppo già utilizzati. Il governatore resta dipendente dalla guida storica; robustezza fuori campione e prosecuzione oltre D11 non sono valutate.
- Le candidate sono locali e non pubblicate. La V4D competitiva rimane invariata.

## Indicazione per il prossimo sviluppo

Conservare questa apertura assistita come controllo positivo. Per rendere autonoma la governance, sostituire progressivamente le decisioni della guida mantenendo i traguardi osservati: completamento dei 12 meloni entro D1, servizi sufficienti alla resa di 72 unità a D11, grano di servizio e passaggio alle fragole. Il rilascio della guida va verificato separatamente: un buon avvio, da solo, non certifica la capacità del core di sfruttare il capitale dopo D11.
'''
    for t in datasets:
        text+=f"\nTopologia dei pascoli osservata a D11 nella candidata {t}: `{'; '.join(summary[t]['assisted']['d11_topologies'])}`. Fughe di animali nel prefisso: {summary[t]['assisted']['animal_escapes']}.\n"
    name='REPORT_AVVIO_ASSISTITO_D11_IT'
    (OUT/f'{name}.md').write_text(text,encoding='utf-8')
    body=MarkdownIt().enable('table').render(text).replace('src="trend_d11.png"','src="data:image/png;base64,'+base64.b64encode((OUT/'trend_d11.png').read_bytes()).decode()+'"')
    html='<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Avvio assistito D11 · 770 e 662</title><style>body{max-width:1120px;margin:40px auto;padding:0 24px;font:17px/1.6 system-ui;color:#183045}h1,h2{line-height:1.25}h2{margin-top:36px}table{border-collapse:collapse;width:100%;font-size:15px}td,th{padding:9px;border-bottom:1px solid #dce4ed;text-align:right}td:first-child,th:first-child{text-align:left}th{background:#edf3f8}img{width:100%}code{overflow-wrap:anywhere}</style><body>'+body+'</body></html>'
    (OUT/f'{name}.html').write_text(html,encoding='utf-8')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    paths=list(DATA.glob('*.json'))+list(OUT.glob('*'))
    (OUT/'manifest.json').write_text(json.dumps(dict(scope='D1-D11',sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.name!='manifest.json'}),indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
