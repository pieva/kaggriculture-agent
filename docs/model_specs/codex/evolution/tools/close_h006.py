"""Summarize the frozen H006 diagnostic without changing its predictions."""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'docs/model_specs/codex/evolution'
OUT = BASE / 'reports/H006'


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = read(OUT / 'RESULT.json')
previous = read(BASE / 'reports/H005/RESULT.json')
checks = read(OUT / 'CHECKS.json')
assert checks['witnesses_reproduced'] == 420 and checks['forecasts_reproduced'] == 84
assert all(value is True for key, value in checks.items() if key not in ['witnesses_reproduced', 'forecasts_reproduced'])
old = read(BASE / 'reports/H005/PREDICTIONS.json')
new = read(OUT / 'PREDICTIONS.json')
transitions = Counter()
fixed = 0
for before, after in zip(old, new):
    assert (before['source'], before['seat']) == (after['source'], after['seat'])
    for a, b in zip(before['evidence'], after['evidence']):
        transitions[(a['status'], b['status'])] += 1
        fixed += any(d.get('fixed_floor_revenue') for d in b.get('items', []))
comparison = dict(
    status_transitions=[dict(before=a, after=b, count=n) for (a, b), n in sorted(transitions.items())],
    witnesses_with_reported_fixed_floor=fixed,
    forecast_transitions=dict(Counter(a['forecast'] + ' -> ' + b['forecast'] for a, b in zip(old, new))),
    forecast_labels=dict(Counter(p['forecast'] for p in new)),
    previous_predictions_unchanged=sha(BASE / 'reports/H005/PREDICTIONS.json') == previous['predictions_sha256'])
assert comparison['previous_predictions_unchanged']
(OUT / 'COMPARISON.json').write_text(json.dumps(comparison, indent=2) + '\n')
decision = 'NOT_OPERATIONALLY_USEFUL' if not result['applied'] else 'DIAGNOSTIC_ONLY_REQUIRES_FULL_CONTINUATIONS'
summary = f'''H006 recupera le vendite proprie di prodotti non acquistabili gia al prezzo minimo come ricavi certi, senza stimare il volume concorrente. Soglie e campione invariati rispetto a H005.

Ricostruzioni identificate: {previous['historical_identified']} -> {result['historical_identified']}/420; previsioni: {previous['forecast_covered']} -> {result['forecast_covered']}/84. Errori storici {result['historical_errors']}, errori forecast {result['forecast_errors']}, riordini selezionati {result['applied']}, riordini negativi {result['applied_losses']}, delta cassa one-step totale {result['total_delta_cash']}. Decisione: **{decision}**, non adottato.

Passati 120 casi sintetici sul motore, inclusi casi di astensione per fragole e grano al minimo. Riprodotte 420 testimonianze e 84 previsioni senza D20/seguito e senza azioni o stato privato avversari; input e predizioni invariati. Le predizioni H005 restano identiche. Nessuna nuova partita completa, nessuna modifica ai tre modelli, nessun accesso ai seed riservati.

Gli errori sono misurati solo nei casi coperti del campione diagnostico gia esposto (sette seed, ruoli accoppiati). Le astensioni non sono successi. I prodotti che raggiungono il minimo durante il batch restano un limite del modello inverso; il presente esperimento non ne ricostruisce la saturazione.

I quattro riordini selezionati riguardano esclusivamente E19 contro E18: seed 180910204 e 180910206, entrambi i ruoli. Sono due seed, non quattro repliche indipendenti. Il vantaggio immediato per ruolo e rispettivamente +17 e +20 di cassa (+32 e +37 di margine). E20.1 non riceve interventi. Il seguito concreto richiede quattro prosecuzioni modificate e quattro controlli esatti fino a D30, con memoria originale ricostruita, avversario libero di reagire e audit dei 22 KPI; questi risultati terminali non sono ancora disponibili.
'''
report = OUT / 'REPORT.md'
text = report.read_text(encoding='utf-8').split('## Interpretazione finale H006')[0]
report.write_text(text.rstrip() + '\n\n## Interpretazione finale H006\n\n' + summary + '\n[Confronto H005](COMPARISON.json) · [Controlli](CHECKS.json) · [Test sintetici](SYNTHETIC_CHECKS.json).\n', encoding='utf-8')
registry_path = BASE / 'REGISTRY.json'
registry = read(registry_path)
registry['experiments'] = [e for e in registry['experiments'] if e['id'] != 'H006']
registry['experiments'].append(dict(id='H006', status='complete', adopted=False, decision=decision,
    protocol_sha256=sha(BASE / 'H006_PROTOCOL.md'), prediction_sha256=sha(OUT / 'PREDICTIONS.json'),
    historical_identified=result['historical_identified'], forecast_covered=result['forecast_covered'],
    forecast_errors=result['forecast_errors'], applied_reorders=result['applied'],
    result_path='docs/model_specs/codex/evolution/reports/H006/RESULT.json'))
registry_path.write_text(json.dumps(registry, indent=2) + '\n')
heading = '## 2026-09-10 — H006: ricavi certi al prezzo minimo'
checkpoint = heading + '\n\n' + summary + '\n[Report H006](model_specs/codex/evolution/reports/H006/REPORT.md).\n'
for name in ['PROJECT_STATE.md', 'NEW_SESSION.md', 'EXPERIMENT_LOG.md']:
    path = ROOT / 'docs' / name
    text = path.read_text(encoding='utf-8')
    if heading not in text:
        path.write_text(text.rstrip() + '\n\n' + checkpoint if name == 'EXPERIMENT_LOG.md' else checkpoint + '\n---\n\n' + text, encoding='utf-8')
path = BASE / 'README.md'
text = path.read_text(encoding='utf-8')
if '## H006: ricavi certi' not in text:
    path.write_text(text.rstrip() + '\n\n## H006: ricavi certi al prezzo minimo\n\n[Protocollo](H006_PROTOCOL.md) · [Report](reports/H006/REPORT.md). Dalla radice eseguire con `.venv/Scripts/python.exe`, in sequenza, gli script in `docs/model_specs/codex/evolution/tools/`: `test_h006_accounting.py`, `run_h006.py`, `check_h006.py`, `close_h006.py`. Nessuna promozione sul campione diagnostico.\n', encoding='utf-8')
paths = [p for p in OUT.glob('*.json') if p.name != 'MANIFEST.json'] + [report, BASE / 'H006_PROTOCOL.md', registry_path]
paths += [BASE / 'tools' / name for name in ['infer_market_order_floor.py', 'run_h006.py', 'check_h006.py', 'test_h006_accounting.py', 'close_h006.py']]
(OUT / 'MANIFEST.json').write_text(json.dumps(dict(status='complete', sha256={p.relative_to(ROOT).as_posix(): sha(p) for p in paths}), indent=2) + '\n')
print(summary)
print(json.dumps(comparison, indent=2))
