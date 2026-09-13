"""Daily dashboard plus paired v2-v1 comparison against the frozen E22 control."""
import json
from statistics import mean, median
import report_q0_pastures as shared
from compare_q0_pastures import ROOT
from e209_s56165462_charts import chart

OUT = ROOT / 'docs/model_specs/codex/e22/reports/q0_8c9s_calendar_v2'
ART = ROOT / 'docs/model_specs/codex/e22/artifacts/q0_8c9s_calendar_v2'
V1 = ART.parent / 'q0_8c9s_v1'

def main():
    shared.OUT, shared.ART = OUT, ART
    shared.main()
    rows = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(ART.glob('*.json'))]
    pairs = []
    for r in rows:
        old = json.loads((V1 / f"{r['seed']}_{r['seat']}.json").read_text(encoding='utf-8'))
        assert old['hashes']['baseline'] == r['hashes']['baseline']
        s = r['seat']
        pairs.append(dict(seed=r['seed'],seat=s,v1_margin=old['margin'],v2_margin=r['margin'],
                          margin_delta=r['margin']-old['margin'],
                          own_cash_delta=r['rewards'][s]-old['rewards'][s],
                          opponent_cash_delta=r['rewards'][1-s]-old['rewards'][1-s],
                          v1=old,v2=r))
    compact = [{k:v for k,v in p.items() if k not in ('v1','v2')} for p in pairs]
    comparison = dict(n=len(pairs),better_than_v1=sum(p['margin_delta']>0 for p in pairs),
                      mean_margin_delta=mean(p['margin_delta'] for p in pairs),
                      median_margin_delta=median(p['margin_delta'] for p in pairs),
                      mean_own_cash_delta=mean(p['own_cash_delta'] for p in pairs),pairs=compact,
                      method='Difference between two matches against identical E22 policy on the same seed/role; not a direct v1-v2 match. Market response is included.')
    (OUT/'VS_V1.json').write_text(json.dumps(comparison,indent=2),encoding='utf-8')
    explanation = ('Calendario esterno applicato alle tre pecore: (3,2) D11 H20, (4,1) D11 H21, (2,3) D12 H7. '
        'Raccolte delle prime due a D17/20/23/26/29; della terza a D18/21/24/27/30. '
        'Le ore di raccolta sfruttano i nostri percorsi e non copiano un intero piano avversario. '
        'Le raccolte con resa presente hanno precedenza sugli altri servizi nei giorni previsti; alimentazione e cure continuano negli slot disponibili. '
        'La v1 ritardava le prime due ultime raccolte a D30. Il collocamento anticipato nella stessa giornata non cambia da solo l’età produttiva nel motore. '
        'A D12 l’acquisto della pecora passa da H2 a H1, l’operaio 1 la colloca a H7 e consegna il latte a H11; '
        'l’operaio 6 conserva il percorso di alimentazione. Nessuna assunzione aggiuntiva. Due slot di raccolta fertilizzante D12 sono rimossi per far spazio al tragitto. '
        'La logica di vendita lana v1, inclusa quella precedente a D11, rimane invariata.')
    comparison_text = (f"Rispetto alla v1, il margine contro E22 migliora in {comparison['better_than_v1']}/{len(pairs)} partite; "
        f"differenza media {comparison['mean_margin_delta']:+.1f}, mediana {comparison['median_margin_delta']:+.1f}. "
        f"Differenza media della sola cassa del candidato {comparison['mean_own_cash_delta']:+.1f}. "
        'Sono confronti su seed e ruoli accoppiati contro E22, non partite dirette v1-v2. '
        'La differenza dei margini comprende anche la variazione degli incassi del controllo nel mercato condiviso.')
    md = '\n## Calendario adottato e confronto con v1\n\n' + explanation + '\n\n' + comparison_text + '\n\n'
    md += '| Seed | Ruolo | Margine v1 | Margine v2 | Delta |\n|---|---:|---:|---:|---:|\n'
    for p in pairs: md += f"| {p['seed']} | {p['seat']} | {p['v1_margin']:+.0f} | {p['v2_margin']:+.0f} | {p['margin_delta']:+.0f} |\n"
    md += '\n[Confronto v1 JSON](VS_V1.json). I controlli per casella, compresi ore e quantità, sono nei risultati di ogni partita.\n'
    report = (OUT/'REPORT.md').read_text(encoding='utf-8').replace('8C9S v1','8C9S calendario v2')
    (OUT/'REPORT.md').write_text(report + md,encoding='utf-8')
    decision = json.loads((OUT/'DECISION.json').read_text(encoding='utf-8'))
    decision['decision'] = decision['decision'].replace('8C9S v1','8C9S calendario v2')
    decision['comparison_to_v1'] = comparison_text
    (OUT/'DECISION.json').write_text(json.dumps(decision,indent=2),encoding='utf-8')
    extra = '<section><h2>Calendario esterno adottato</h2><p>' + explanation + '</p><p>' + comparison_text + '</p>'
    extra += '<p><a href="VS_V1.json">Confronto accoppiato completo</a></p><div class="plots">'
    for label, fn in [('Cassa media H24 nei rispettivi incontri',lambda p,d:p['daily'][p['seat']][d]['cash']),
                      ('Lana raccolta media giornaliera',lambda p,d:p['ledgers'][p['seat']]['daily'][d]['harvested'].get('WOOL',0))]:
        series = [[mean(fn(p[v],d) for p in pairs) for d in range(30)] for v in ('v1','v2')]
        extra += chart(label,series,'monete' if label.startswith('Cassa') else 'unità').replace('E20.9','8C9S v1').replace('s56165462','Calendario v2')
    extra += '</div><p>In questi due grafici blu = v1, arancio = calendario v2. I grafici delle singole partite sotto confrontano v2 con E22.</p></section>'
    page = (OUT/'REPORT.html').read_text(encoding='utf-8').replace('8C9S v1','8C9S calendario v2')
    page = page.replace('<h1>E22 · tre pascoli Q0 · 8C9S</h1>','<h1>E22 · 8C9S · calendario esterno v2</h1>')
    page = page.replace('<title>E22 Q0 8C9S</title>','<title>E22 Q0 calendario v2</title>')
    page = page.replace('<label>Partita', extra + '<label>Partita',1)
    (OUT/'REPORT.html').write_text(page,encoding='utf-8')
    print(json.dumps({k:v for k,v in comparison.items() if k!='pairs'}),flush=True)

if __name__ == '__main__': main()
