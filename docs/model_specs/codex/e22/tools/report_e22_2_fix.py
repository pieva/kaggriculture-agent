"""Publish local bug-fix evidence and the established 22 KPI + price charts."""
import csv
import gzip
import hashlib
import html
import json
import statistics as st
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from docs.model_specs.codex.e22.tools.report_external_20260914 import METRICS, aggregate, page, rowdata
OUT = ROOT / 'docs/model_specs/codex/e22/reports/e22_2_fix_v1'
ART = ROOT / 'docs/model_specs/codex/e22/artifacts/e22_2_fix_v1'


def read_gzip(path):
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        return json.load(f)


def closing_losses(game, seat):
    import kaggle_environments.envs.kaggriculture.kaggriculture as engine
    result = []
    cfg = SimpleNamespace(**game['configuration'])
    cap = int(game['configuration'].get('shedCapacity', 100))
    def stock(private):
        return Counter(private['shed']) + sum((Counter(inv) for inv in private['inventories']), Counter())
    for i in range(23, 719, 24):
        before, after = game['steps'][i:i+2]
        obs = before[0]['observation']
        farms, market = deepcopy(obs['farms']), deepcopy(obs['market'])
        states = [SimpleNamespace(action=s['action'] or {}, observation=SimpleNamespace(farms=farms, market=market, private=deepcopy(before[j]['observation']['private']))) for j, s in enumerate(after)]
        for j, state in enumerate(states):
            commands = [state.action.get('farmer', ['PASS'])] + state.action.get('hands', [])
            demand = Counter(c[1] for c in commands if len(c) > 1 and c[0] == 'PLANT')
            blocked = {k for k, n in demand.items() if n > state.observation.private['seeds'].get(k, 0)}
            for w, cmd in enumerate(commands):
                allowed = ['PASS'] if cmd and cmd[0] == 'PLANT' and cmd[1] in blocked else cmd
                engine._apply_unit_action(farms[j], state.observation.private, w, allowed, 10, obs['day'], 24, cap)
        engine._process_market(states, SimpleNamespace(configuration=cfg))
        expected, actual = stock(states[seat].observation.private), stock(after[seat]['observation']['private'])
        assert not actual - expected
        lost = expected - actual
        assert sum(lost.values()) == max(0, sum(expected.values()) - cap)
        if lost:
            result.append(dict(day=obs['day']+1, discarded=dict(lost)))
    return result


def main():
    rows = json.loads((OUT / 'RESULTS.json').read_text())
    groups = {arm: sorted([r for r in rows if r['arm'] == arm], key=lambda r:r['episode']) for arm in ('published', 'fix')}
    assert len(groups['fix']) == len(groups['published']) == 20
    direct = json.loads((OUT / 'direct/RESULTS.json').read_text())
    prior = json.loads((OUT.parent / 'q0_8c9s_v1/RESULTS.json').read_text())
    assert len(direct) == len(prior) == 14
    current_hash = hashlib.sha256((ROOT / 'submission/submission_codex_e22_2_fix_v1.py').read_bytes()).hexdigest()
    assert all(r['hash'] == current_hash for r in groups['fix'])
    assert all(r['hashes']['candidate'] == current_hash for r in direct)
    ps = {arm: [read_gzip(ART / f"{r['episode']}_{arm}.profile.json.gz") for r in group] for arm, group in groups.items()}
    losses = []
    for arm, group in groups.items():
        for row in group:
            game = read_gzip(ART / f"{row['episode']}_{arm}.replay.json.gz")
            events = closing_losses(game, row['seat'])
            losses.append(dict(episode=row['episode'], arm=arm, events=events))
    summary = {}
    for arm, group in groups.items():
        summary[arm] = dict(n=len(group), mixes=dict(Counter(str(r['mix']) for r in group)),
            escapes=sum(r['escaped'] for r in group), missing_worker_batches=sum(len(r['missing_workers']) for r in group),
            failed_plants=sum(r['failed'].get('PLANT', 0) for r in group), unfed=sum(r['unfed'] for r in group),
            crop_stress=sum(len(p['crop_starvation']) for p in ps[arm]),
            product_loss=dict(sum((Counter(r['animal_product_lost']) for r in group), Counter())),
            overflow=dict(sum((Counter(e['discarded']) for r in losses if r['arm']==arm for e in r['events']), Counter())),
            fertilizer_residual=sum(r['terminal']['carried'].get('FERTILIZER', 0)+r['terminal']['shed'].get('FERTILIZER',0) for r in group),
            cash_mean=st.mean(r['rewards'][r['seat']] for r in group))
    def direct_summary(data):
        return dict(n=len(data), wins=sum(r['margin']>0 for r in data), cash_mean=st.mean(r['rewards'][r['seat']] for r in data), mean_margin=st.mean(r['margin'] for r in data), median_margin=st.median(r['margin'] for r in data))
    summary['direct_published'] = direct_summary(prior)
    summary['direct_fix'] = direct_summary(direct)
    assert all(r['mix'] == {'COW': 8, 'SHEEP': 9} and not r['escaped'] and not r['missing_workers'] and not any(r['animal_product_lost'].values()) and not any(r['residual'].values()) for r in groups['fix'])
    assert summary['fix']['failed_plants'] == summary['fix']['fertilizer_residual'] == 0
    assert not summary['fix']['overflow']
    assert all(r['checks']['mix'] == {'COW':8,'SHEEP':9} and r['checks']['escapes'] == 0 for r in direct)
    assert all(ledger['cash_parity_errors'] == 0 for r in direct for ledger in r['ledgers'])
    assert all(p['ledger']['cash_parity_errors'] == 0 and not p['policy_differences'] for group in ps.values() for p in group)
    (OUT / 'SUMMARY.json').write_text(json.dumps(summary, indent=2))
    (OUT / 'OVERFLOW.json').write_text(json.dumps(losses, indent=2))
    views = [dict(title='20 scenari esterni: aggregato', labels=['E22.2 fix v1', 'E22.2 pubblicata'], note='Replay diagnostici: stessi semi, avversario con azioni registrate e mercato ricalcolato. Non sono nuovi risultati Kaggle. Mediana e min–max.', series=[aggregate(ps['fix']),aggregate(ps['published'])])]
    for i, row in enumerate(groups['fix']):
        views.append(dict(title=f"Scenario {row['episode']}", labels=['E22.2 fix v1','E22.2 pubblicata'], note='Confronto dello stesso scenario con azioni avversarie congelate; gli acquisti e le vendite possono avere esiti diversi.', series=[aggregate([ps['fix'][i]]),aggregate([ps['published'][i]])]))
    data = dict(metrics=METRICS, views=views)
    csvrows = [dict(episode=r['episode'], arm=arm, **d) for arm in ps for r,p in zip(groups[arm],ps[arm]) for d in rowdata(p)]
    with (OUT / 'DAILY_22_KPI_PRICES.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(csvrows[0]));writer.writeheader();writer.writerows(csvrows)
    a,b=summary['published'],summary['fix']
    table='| Controllo nei 20 scenari | Pubblicata | Fix v1 |\n|---|---:|---:|\n'
    for label,k in [('Fughe','escapes'),('Batch con lavoratori mancanti','missing_worker_batches'),('Semine senza effetto','failed_plants'),('Giorni-animale senza pasto','unfed'),('Colture trasformate in infestanti dopo stress','crop_stress'),('Fertilizzante finale non venduto','fertilizer_residual')]:
        table+=f"| {label} | {a[k]} | {b[k]} |\n"
    table+=f"| Scarti al rientro notturno | {a['overflow']} | {b['overflow']} |\n"
    d0,d1=summary['direct_published'],summary['direct_fix']
    md='# E22.2 fix v1 — correzioni e verifica locale\n\n'
    md+='Nuovo bundle autonomo `submission_codex_e22_2_fix_v1.py`; E22.2 pubblicata (56212495) resta immutata. Nessuna nuova pubblicazione.\n\n'
    md+='Correzioni: vendita condizionale prima delle assunzioni non finanziate; recupero del pasto D2 della mucca centrale e riallineamento della rotta; rimozione infestanti e semina nel successivo slot WATER; rispetto delle sementi disponibili per evitare il blocco atomico; uso di slot inattivi/ridondanti per cibo, cura e acqua; spazio per il rientro notturno; consegna e vendita delle scorte finali. Restano il mix 8C9S e i tre pascoli Q0.\n\n'+table
    md+='\n**8C9S in tutti i 20 scenari corretti**, senza animali bloccati, fughe o prodotti animali raccolti e poi persi. Risolte anche la risemina del grano D16 senza irrigazione e la perdita della fragola dopo il passaggio D21. Rimangono giornate senza pasto: questa è una correzione delle anomalie riproducibili, non una riscrittura completa del calendario. I comandi innocui ridondanti non sono tutti eliminati.\n\n'
    md+=f"Confronto diretto con E22.1, 7 semi già esposti × 2 lati: fix **{d1['wins']}/14 vittorie**, margine medio **{d1['mean_margin']:+.1f}**, mediano **{d1['median_margin']:+.1f}**. E22.2 pubblicata sugli stessi casi: {d0['wins']}/14, medio {d0['mean_margin']:+.1f}, mediano {d0['median_margin']:+.1f}. Tutte le 14 partite del fix chiudono 8C9S senza fughe.\n\n"
    md+='Metodo: i 20 avversari esterni sono riprodotti mediante le loro azioni registrate, senza disporre del loro codice. Il motore ricalcola esiti e prezzi; sono prove diagnostiche, non stime di rating. Il controllo riutilizza i replay originali già auditati (campo `source`); ogni scenario del candidato finale viene eseguito nel loader Kaggle. Il test diretto usa invece i due bundle reali. Nessun seme riservato è stato usato.\n\n'
    md+='22 KPI standard + 9 pannelli volumi + 9 prezzi realizzati. Parità contabile, 719 azioni per lato e riconciliazione dei prodotti controllate; gli scarti notturni sono verificati nel motore su 29 refresh per partita.\n\n[Report interattivo](REPORT.html) · [Riepilogo](SUMMARY.json) · [Scarti](OVERFLOW.json) · [CSV KPI e prezzi](DAILY_22_KPI_PRICES.csv) · [Confronti diretti](direct/RESULTS.json).\n'
    (OUT/'REPORT.md').write_text(md,encoding='utf-8')
    body=f'<p>Versione locale corretta · controllo pubblicato 56212495 · <b>non pubblicata</b>.</p><p class="note"><b>20/20 scenari con 8 mucche e 9 pecore, zero fughe, zero scarti notturni e zero semine fallite.</b> Verifica diagnostica con azioni avversarie congelate; nessuna stima di rating.</p><p>Confronti diretti con E22.1: <b>{d1["wins"]}/14 vittorie</b>, margine medio {d1["mean_margin"]:+.1f}, mediano {d1["median_margin"]:+.1f}. Persistono {b["unfed"]} giorni-animale senza pasto e {b["crop_stress"]} transizioni di colture a infestanti dopo stress nel campione corretto.</p><p><a href="REPORT.md">Correzioni, risultati e limiti</a> · <a href="SUMMARY.json">Riepilogo</a> · <a href="DAILY_22_KPI_PRICES.csv">CSV 22 KPI e prezzi</a> · <a href="OVERFLOW.json">Audit scarti</a></p>'
    (OUT/'REPORT.html').write_text(page('E22.2 fix v1 · verifica delle correzioni',body,data),encoding='utf-8')
    verification=dict(candidate_sha256=current_hash, replay_scenarios=20, direct_games=14, kpi=22, panels=len(METRICS), views=len(views), cash_parity_errors=0, candidate_actions_verified=20*719, daily_returns_audited=40*29, reserved_seeds_used=0, published=False)
    verification['cash_ledgers_verified'] = 40 + 2 * len(direct)
    verification['execution'] = 'Every final candidate scenario executed with this exact bundle hash via the Kaggle file loader.'
    (OUT/'VERIFICATION.json').write_text(json.dumps(verification,indent=2))
    protocol=dict(candidate='submission/submission_codex_e22_2_fix_v1.py', candidate_sha256=current_hash,
        published_control=56212495, episode_ids=[r['episode'] for r in groups['fix']],
        exposed_seeds=list(range(180911301,180911308)), seats=[0,1], reserved_seeds_used=[],
        diagnostic_opponents='Recorded actions only; rewards, inventory and prices recomputed in local engine.',
        direct_opponent='E22.1 published policy via actual Kaggle file loader.',
        revision_verification=verification['execution'], publication=False)
    (OUT/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2))
    local=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(ART.rglob('*.gz'))]
    (OUT/'LOCAL_ARTIFACTS.json').write_text(json.dumps(local,indent=2))
    manifest=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='MANIFEST.json' and p.suffix!='.log']
    (OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(summary),flush=True)


if __name__ == '__main__':
    main()
