"""Record H005 interpretation and hash its diagnostic evidence."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'docs/model_specs/codex/evolution'
OUT = BASE / 'reports/H005'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


note = '''## Interpretazione finale H005

Rispetto a H004, le ricostruzioni storiche identificate aumentano da 64 a 83 su 420 e le previsioni da 18 a 31 su 84. Tutte le 31 previsioni sono `not_first`: 24 per E18, 7 per E19, nessuna per E20.1. Nessuna attiva il riordino H003. Decisione: **NOT_OPERATIONALLY_USEFUL**, non adottato. Zero errori nei casi coperti non dimostra generalizzazione: il campione contiene sette seed diagnostici gia esposti, con ruoli accoppiati.

I 24 test sintetici sul motore coprono vendite e acquisti propri e concorrenti, acquisti di semi e assunzioni: tutti conservano la posizione vera. Il controllo temporale riproduce 420 testimonianze e 84 previsioni rimuovendo D20 e seguito, oscurando anche la fattoria pubblica avversaria; input e hash delle predizioni restano invariati.

La diagnosi successiva, separata dalle predizioni congelate, localizza i 116 residui incompatibili su MILK (75) e WOOL (41). In 50 casi il prezzo iniziale e gia 1; negli altri 66 parte sopra il minimo. Il motore non incrementa lo stock pubblico per le vendite quotate a 1: il residuo negativo non prova acquisti avversari. La diagnosi localizza il limite, senza ricostruire ancora tutte le transazioni dei 66 casi restanti.

Prossimo esperimento da preregistrare: trattare come ricavo certo le vendite dei prodotti non acquistabili gia al minimo, mantenendo non identificato il volume concorrente. Per i prodotti che raggiungono il minimo durante il batch serve invece una ricostruzione compatibile con la saturazione dello stock. Non modificare retroattivamente H005 e non abbassare la soglia delle due testimonianze concordi. I seed riservati 180911301-307 restano inutilizzati.

[Controlli temporali](CHECKS.json) · [Test sul motore](SYNTHETIC_CHECKS.json) · [Diagnosi delle astensioni](ABSTENTION_DIAGNOSIS.json).
'''
report = OUT / 'REPORT.md'
original = report.read_text(encoding='utf-8').split('## Interpretazione finale H005')[0]
report.write_text(original.rstrip() + '\n\n' + note, encoding='utf-8')
registry_path = BASE / 'REGISTRY.json'
registry = json.loads(registry_path.read_text())
registry['experiments'] = [e for e in registry['experiments'] if e['id'] != 'H005']
registry['experiments'].append(dict(
    id='H005', status='complete', adopted=False,
    protocol_sha256=sha(BASE / 'H005_PROTOCOL.md'),
    result_path='docs/model_specs/codex/evolution/reports/H005/RESULT.json',
    historical_identified=83, forecast_covered=31, forecast_errors=0,
    applied_reorders=0, decision='NOT_OPERATIONALLY_USEFUL',
    prediction_sha256=sha(OUT / 'PREDICTIONS.json')))
registry_path.write_text(json.dumps(registry, indent=2) + '\n', encoding='utf-8')
checkpoint = '''## 2026-09-10 — H005: transazioni miste, copertura maggiore ma zero riordini

Completato il seguito preregistrato di H004, con SELL/BUY_PRODUCT/BUY_SEED/HIRE e soglia invariata. Sui medesimi 42 replay diagnostici: 83/420 ricostruzioni identificate (H004: 64), 31/84 previsioni (H004: 18), zero errori nei casi coperti. Tutte le previsioni sono not_first: E18 24, E19 7, E20.1 zero. Nessun riordino selezionato, nessun guadagno dimostrato: NON ADOTTATO.

Passati 24 test sintetici sul motore e riproduzione di 420 testimonianze/84 previsioni senza D20 o seguito, senza azioni/privato avversari, con input e hash predizioni invariati. Diagnosi: 116 residui incompatibili su latte/lana, 50 gia al prezzo minimo iniziale. Prossimo passo: nuovo protocollo per il ricavo certo dei prodotti non acquistabili gia al minimo e, separatamente, saturazione durante il batch. Nessuna modifica ai modelli o ai seed riservati; nessuna nuova partita o submission.

[Report H005](model_specs/codex/evolution/reports/H005/REPORT.md) · [Protocollo](model_specs/codex/evolution/H005_PROTOCOL.md).
'''
for name in ['PROJECT_STATE.md', 'NEW_SESSION.md']:
    path = ROOT / 'docs' / name
    text = path.read_text(encoding='utf-8')
    if not text.startswith(checkpoint.splitlines()[0]):
        path.write_text(checkpoint + '\n---\n\n' + text, encoding='utf-8')
path = ROOT / 'docs/EXPERIMENT_LOG.md'
text = path.read_text(encoding='utf-8')
if checkpoint.splitlines()[0] not in text:
    path.write_text(text.rstrip() + '\n\n' + checkpoint, encoding='utf-8')
path = BASE / 'README.md'
text = path.read_text(encoding='utf-8')
if '## H005: transazioni miste' not in text:
    path.write_text(text.rstrip() + '''

## H005: transazioni miste

[Protocollo](H005_PROTOCOL.md) e [report conclusivo](reports/H005/REPORT.md). Copertura 31/84, nessun riordino: non adottato. Stesse soglie e stesso campione diagnostico di H004.

Eseguire dalla radice, in sequenza con `.venv/Scripts/python.exe`: `docs/model_specs/codex/evolution/tools/test_h005_accounting.py`, `run_h005.py`, `check_h005.py`, `diagnose_h005.py`, `close_h005.py` (gli ultimi quattro nella stessa directory tools). Il runner congela le predizioni prima della valutazione; la chiusura aggiunge interpretazione e manifest.
''', encoding='utf-8')
paths = [p for p in OUT.glob('*.json') if p.name != 'MANIFEST.json'] + [report, BASE / 'H005_PROTOCOL.md', registry_path]
paths += [BASE / 'tools' / name for name in ['infer_market_order_mixed.py', 'run_h005.py', 'check_h005.py', 'test_h005_accounting.py', 'diagnose_h005.py', 'close_h005.py']]
(OUT / 'MANIFEST.json').write_text(json.dumps(dict(status='complete', sha256={p.relative_to(ROOT).as_posix(): sha(p) for p in paths}), indent=2) + '\n')
