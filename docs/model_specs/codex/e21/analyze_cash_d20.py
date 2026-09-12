"""Cash explanation from existing ledgers only; no new simulations."""
import gzip,hashlib,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent/'reports/trajectory_774_772_775'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def aggregate(s):
    ds=s['ledger']['daily'][19:];out={}
    for k in ['sales_cash','sold_units','harvested','purchase_cash','bought_units']:
        c=Counter()
        for d in ds:c.update(d[k])
        out[k]=dict(c)
    out['hire_cash']=sum(d['hire_cash'] for d in ds)
    out['net_cash']=sum(sum(d['sales_cash'].values())-sum(d['purchase_cash'].values())-d['hire_cash']-d['land_cash']+d['unit_cash_delta'] for d in ds)
    return out
def main():
    profiles=read(OUT/'ANALYSIS.json')['profiles'];rows=[];sources={}
    for p in profiles:
        path=ROOT/p['source'];k=read(path.with_suffix('.kpi.json'))
        raw=gzip.decompress(path.with_suffix('.replay.json.gz').read_bytes());assert hashlib.sha256(raw).hexdigest()==k['replay_sha256']
        r=json.loads(raw);a=aggregate(k['sides'][0]);a.update(label=p['label'],source=p['source'],cash_start_d20=r['steps'][456][0]['observation']['farms'][0]['money'],cash_final=p['reward'])
        assert a['cash_start_d20']+a['net_cash']==a['cash_final']
        a['wool_price_checkpoints']={d:r['steps'][24*d-1][0]['observation']['market']['prices']['WOOL'] for d in [20,21,24,25,27,30]}
        a['town_checkpoints']={d:r['steps'][24*d-1][0]['observation']['town']['unlocked_shops'] for d in [13,16,19,22,25]}
        rows.append(a);sources[p['source']]=hashlib.sha256(path.read_bytes()).hexdigest()
        if p['label']=='774 ricostruita':
            other=aggregate(k['sides'][1]);other.update(label='775 E18 nella partita della 774',cash_final=k['sides'][1]['reward'])
    payload=dict(window='All action flows D20-D30, exact state 456 to terminal; not D19 pre-last-batch checkpoint',rows=rows,same_match_e18=other,sources=sources,new_simulations=0)
    (OUT/'CASH_D20_ANALYSIS.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    text='''# Cosa sostiene il distacco di cassa da D20

La voce principale è la lana, ma i due confronti hanno spiegazioni differenti. Flussi completi D20–D30, riconciliati dal vero inizio D20 (stato 456), non dal checkpoint grafico D19 prima dell'ultimo batch.

| Traiettoria | Lana raccolta | Lana venduta | Ricavi lana | Prezzo medio realizzato |
|---|---:|---:|---:|---:|
| 775 E18 del grafico, contro 772 | 140 | 140 | 22.307 | 159,34 |
| 772 E20.2, contro 775 | 77 | 90 | 14.091 | 156,57 |
| 774 ricostruita, contro 775 | 139 | 145 | 9.936 | 68,52 |
| 775 E18 nella partita della 774 | 140 | 140 | 8.326 | 59,47 |

## 775 contro 772

Prezzi medi della lana simili, ma 775 ha dieci pecore contro sei e raccoglie/vende più lana. Il contributo lana è +8.216 di ricavi. Nel complesso D20–D30: +13.295 vendite, −5.975 maggiori acquisti, −139 assunzioni = +7.181 di cassa aggiuntiva rispetto a 772. Il vantaggio di cassa già all'inizio D20 è 9.014; finale 16.195. Nessun terreno acquistato nella finestra. I maggiori ricavi grano (+5.342) sono quasi compensati dai maggiori acquisti di grano (+5.320): non rappresentano un grande guadagno agricolo netto.

## 775 del grafico contro 774: soprattutto mercato della lana

Produzione quasi identica (140 contro 139), ma ricavi lana differenti di 12.371. Questo spiega circa il 71% del divario di crescita di cassa D20–D30: +17.325 vendite e +215 minori acquisti = +17.540. Il divario finale è 21.559, di cui 4.019 già all'inizio D20.

Le due curve provengono da mercati diversi. Contro 772, la lana venduta complessivamente dai due giocatori D20–D30 è 230 unità; contro 774 è 285. In entrambe le partite c'è un solo YARN_STORE, aperto da D7, con la stessa domanda di lana: due unità ogni quattro turni più una ogni 24 dal centro città. Gli altri negozi differiscono, ma non consumano lana. È quindi la maggiore offerta congiunta, a domanda di lana uguale, a saturare quel mercato. Anche calendario delle vendite e competizione nello stesso batch influenzano il prezzo realizzato.

Prezzo pubblico lana al checkpoint D24: 193 nella partita 775/772, 24 nella partita 774/775; D25: 154 contro 5. La produzione della 775 è la stessa (140 unità nella finestra), ma nella partita della 774 incassa appena 8.326 dalla lana. La sua cassa finale lì è 75.765 contro 72.473 della 774: margine diretto 3.292, non i 21.559 fra le curve di partite diverse.

Il risultato sostiene un vantaggio di capacità produttiva animale contro 772 e un forte effetto di saturazione commerciale contro un altro allevamento denso. Non dimostra che la 775 possieda una regola speciale che anticipa D20, né misura il rendimento marginale delle CARE. Un solo seed esposto; nessuna nuova simulazione.
'''
    (OUT/'CASH_D20_ANALYSIS.md').write_text(text,encoding='utf-8')
    section='''<section id="cassa-d20"><h2>Perché la cassa 775 si distacca da D20?</h2><p><strong>Soprattutto lana.</strong> Contro 772, 775 vende 140 unità a 159,34 medi; 772 ne vende 90 a 156,57. La differenza è principalmente il volume: dieci pecore contro sei.</p><p>Contro la curva 774, invece, la produzione è quasi uguale (140 contro 139), ma i mercati sono diversi. Nella partita 774/775 i due allevamenti vendono insieme 285 unità di lana D20–D30, contro 230 nella partita 775/772, con la stessa domanda di lana. Il prezzo pubblico D24 è 24 contro 193. La stessa E18, nella partita della 774, ricava dalla lana solo 8.326 e chiude a 75.765: vantaggio diretto 3.292, non 21.559.</p><p><a href="CASH_D20_ANALYSIS.md">Analisi completa e riconciliazione della cassa</a> · <a href="CASH_D20_ANALYSIS.json">Dati D20–D30</a></p></section>'''
    p=OUT/'REPORT.html';h=p.read_text(encoding='utf-8')
    if 'id="cassa-d20"' not in h:h=h.replace('<section id="interpretazione">',section+'<section id="interpretazione">')
    p.write_text(h,encoding='utf-8')
    manifest=read(OUT/'MANIFEST.json');manifest['sources'][str(Path(__file__).relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    for p in [OUT/'REPORT.html',OUT/'CASH_D20_ANALYSIS.md',OUT/'CASH_D20_ANALYSIS.json']:manifest['outputs'][p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    (OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Cash explanation saved; all three D20-D30 cash flows reconcile exactly.')
if __name__=='__main__':main()
