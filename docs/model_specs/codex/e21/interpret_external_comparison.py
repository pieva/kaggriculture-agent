"""Summarize observed rating history and cash decomposition, not causal effects."""
import json,csv
from pathlib import Path
from statistics import mean
from collections import Counter
BASE=Path(__file__).resolve().parent;OUT=BASE/'reports/external_770_772_774_775'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def num(x):return f'{x:,.1f}'.replace(',','_').replace('.',',').replace('_','.')

def main():
    summary=read(OUT/'SUMMARY.json');rows=[read(p) for p in (OUT/'profiles_1700').glob('*.json')]
    assert len(rows)==80 and all(s['n']==20 for s in summary.values()) and not read(OUT/'AUDIT_ERRORS.json')
    history=read(OUT/'history_56185961.json')
    es=sorted([e for e in history['episodes'] if e.get('state')=='COMPLETED' and e.get('type')=='EPISODE_TYPE_PUBLIC' and len({a['teamId'] for a in e['agents']})==2],key=lambda e:(e['createTime'],e['id']))
    own=lambda e:next(a for a in e['agents'] if a['submissionId']==56185961)
    win=lambda e:own(e)['reward']>next(a['reward'] for a in e['agents'] if a['submissionId']!=56185961)
    rating={'complete_public_games':len(es),'wins':sum(win(e) for e in es),'first8_wins':sum(win(e) for e in es[:8]),
            'peak':max(own(e)['updatedScore'] for e in es),'latest':own(es[-1])['updatedScore'],
            'episodes':[{'id':e['id'],'end':e['endTime'],'won':win(e),'rating':own(e)['updatedScore']} for e in es]}
    context={};terminal={};exclusions={}
    for model in summary:
        group=[r for r in rows if r['model']==model]
        context[model]={}
        for day in [12,20,25]:
            counts=Counter()
            for r in group:
                valid=[t for t in r['town_changes'] if t['day']<=day]
                if valid:counts.update(valid[-1]['town'].get('unlocked_shops',[]))
            context[model][str(day)]={k:v/len(group) for k,v in counts.items()}
        terminal[model]={'games_with_shed_stock':sum(any(r['profile']['terminal']['shed'].values()) for r in group),
                         'games_with_carried_stock':sum(any(r['profile']['terminal']['carried'].values()) for r in group)}
        h=read(OUT/f"history_{group[0]['submission_id']}.json")
        exclusions[model]={'history_total':len(h['episodes']),'states':dict(Counter(e.get('state') for e in h['episodes'])),
                           'types':dict(Counter(e.get('type') for e in h['episodes'])),
                           'self_play_same_team':sum(len({a['teamId'] for a in e['agents']})<2 for e in h['episodes']),
                           'eligible_completed_public':len([e for e in h['episodes'] if e.get('state')=='COMPLETED' and e.get('type')=='EPISODE_TYPE_PUBLIC' and len({a['teamId'] for a in e['agents']})==2]),'selected':20}
    with (OUT/'PRODUCTS.csv').open(encoding='utf-8',newline='') as f:products=list(csv.DictReader(f))
    decomp=[]
    for item in ['MILK','WOOL','STRAWBERRY']:
        a=next(p for p in products if p['model']=='774' and p['product']==item);b=next(p for p in products if p['model']=='775' and p['product']==item)
        qa,qb=float(a['mean_sold']),float(b['mean_sold']);pa,pb=float(a['realized_price_weighted']),float(b['realized_price_weighted'])
        decomp.append({'product':item,'delta_revenue':float(a['mean_sales_cash'])-float(b['mean_sales_cash']),
                       'quantity_component':(qa-qb)*(pa+pb)/2,'price_component':(pa-pb)*(qa+qb)/2})
    save(OUT/'MARKET_AND_RATING_CONTEXT.json',{'rating774':rating,'shop_counts_mean':context,'terminal':terminal,'history_accounting':exclusions,'revenue_decomposition_774_minus775':decomp})
    interp=f'''### L'avvio era forte, ma al cutoff il segnale si è ridimensionato

La cronologia conferma **8 vittorie nelle prime 8 partite** e un picco provvisorio di rating **{num(rating['peak'])}**. Alle 17:00 sono disponibili **29 partite pubbliche complete**, con **15 vittorie complessive**. Nel campione preregistrato delle **ultime 20**, la 774 fa **7 vittorie e 13 sconfitte**, rating dell'ultimo episodio **{num(rating['latest'])}**. La prima impressione positiva era reale, ma non descrive tutta l'evoluzione successiva. I primi nove episodi non entrano nei 22 KPI della coorte recente; la loro cronologia è conservata nei metadati.

La 774 ha **cassa media 66.252,8**, contro **82.260,8** della 775: circa **16.008 in meno**. Ha però un margine medio sull'avversario meno negativo (−4.890,7 contro −6.850,9) e 7 vittorie contro 6. Questi ordinamenti diversi mostrano perché cassa assoluta, rating e vittorie non sono intercambiabili. Gli avversari della 774 e della 775 hanno rating iniziale medio rispettivamente {num(summary['774']['opponent_rating_mean'])} e {num(summary['775']['opponent_rating_mean'])}; quelli di 770/772 {num(summary['770']['opponent_rating_mean'])}/{num(summary['772']['opponent_rating_mean'])}. Non sono partite appaiate.

### La differenza di cassa nasce soprattutto dopo D12

Rispetto alla 775, la 774 guadagna **821,4** di flusso netto medio in D1–11, poi perde **5.833,8** in D12–19, **9.166,5** in D20–29 e **1.829,1** a D30. Nel bilancio complessivo: ricavi **−16.561,0**, acquisti **−557,9** (risparmio), manodopera **+4,8** (maggior costo), terra invariata. È una riconciliazione contabile delle due coorti, non un effetto causale stimato della rimozione del pascolo.

I ricavi mancanti principali sono **latte −7.414**, **lana −5.224** e **fragole −4.681**; altri prodotti compensano in parte. Il latte raccolto è quasi uguale, **237,95 contro 239,80**, ma il prezzo realizzato scende da **89,15 a 58,69**. La differenza sul latte è quindi soprattutto di monetizzazione nel mercato incontrato, non di quantità raccolta. La lana risente sia della quantità (venduto 210,3 contro 234,0) sia del prezzo (103,57 contro 115,41). Non attribuire questi prezzi alla sola topologia.

### Correzioni tecniche confermate, servizio agricolo ancora debole

La 774 mantiene **7-7-4 in 20/20 replay**, sempre **8 mucche, 9 pecore e un'oca**, senza fughe. Le perdite crop per sete restano **24,9 per partita**, contro **21,9** della 775 e **4,5/3,25** circa di 770/772: un limite della routine agricola che il confronto esterno rende visibile. I conteggi riguardano eventi di perdita, non il numero di giorni senza WATER.

La 775 conserva nel campione l'episodio **108072534**, con finale **5-7-5** e una fuga: escluderlo migliorerebbe artificialmente il suo risultato. In quel replay e in un replay 770 compaiono comandi MOVE/PASS per lavoratori non presenti. Restano contati come richieste globali, ma non attribuiti a un quadrante inventato; quantità e giorni sono nel CSV sotto NON_ATTRIBUIBILE.

**Esito:** pubblicare ha prodotto informazione utile e confermato le correzioni tecniche. Questo primo confronto non dimostra ancora che la 774 sia competitivamente superiore. Nessuna modifica o nuova pubblicazione è stata eseguita a seguito dei risultati.
'''
    (OUT/'INTERPRETATION.md').write_text(interp,encoding='utf-8')
    p=OUT/'REPORT.md';p.write_text(p.read_text(encoding='utf-8').replace('Vedi INTERPRETATION.md per la lettura dei risultati.', '\n'+interp),encoding='utf-8')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(11,4),layout='constrained');ax.plot(range(1,len(es)+1),[own(e)['updatedScore'] for e in es],marker='o',color='#216ec0')
    ax.axvline(9.5,color='#888',ls='--',label='Inizio delle ultime 20 partite');ax.set_xlabel('Partita pubblica completata, ordine temporale');ax.set_ylabel('Rating dopo la partita');ax.set_title('774 · avvio e successivo ridimensionamento · 29 episodi al cutoff');ax.grid(alpha=.2);ax.legend()
    fig.savefig(OUT/'RATING_774.png',dpi=130);plt.close(fig)
    p.write_text(p.read_text(encoding='utf-8').replace('### La differenza di cassa nasce soprattutto dopo D12','![Rating 774 sulle 29 partite](RATING_774.png)\n\n### La differenza di cassa nasce soprattutto dopo D12'),encoding='utf-8')
    print(json.dumps({'rating':rating['latest'],'n':len(rows),'context':context,'terminal':terminal},indent=2))
if __name__=='__main__':main()
