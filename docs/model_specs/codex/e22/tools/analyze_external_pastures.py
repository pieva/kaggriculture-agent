"""Read-only extraction of observed pasture types, tile service and worker routes."""
import contextlib
import csv
import hashlib
import html
import io
import json
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
ORIGINAL = Path('C:/Users/pietr/Projects/kaggriculture-agent')
SOURCE = ORIGINAL / 'docs/model_specs/codex/e22/reports/external_e22_20260913'
OUT = ROOT / 'docs/model_specs/codex/e22/reports/external_pasture_trajectories'
TARGETS = [(4, 1), (3, 2), (2, 3)]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        import importlib
        engine = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    families = json.loads((SOURCE / 'FAMILIES.json').read_text(encoding='utf-8'))
    cohort = json.loads((SOURCE / 'COHORT.json').read_text(encoding='utf-8'))
    details, inventory, csvrows = [], [], []
    actions = {}
    for f in families:
        profile = json.loads((SOURCE / 'profiles' / f"{f['episode']}.json").read_text(encoding='utf-8'))
        seat = 1-profile['seat']
        side = profile['sides'][seat]
        inventory.append(f)
        if not f['q0_three_pastures']: continue
        raw = ORIGINAL / profile['raw']
        assert hashlib.sha256(raw.read_bytes()).hexdigest() == profile['sha256']
        game = json.loads(raw.read_text(encoding='utf-8'))
        events, routes, transitions = [], [], []
        actions[f['episode']] = [st[seat]['action'] for st in game['steps'][1:]]
        for i in range(719):
            obs = game['steps'][i][seat]['observation']
            farm, private = deepcopy(obs['farms'][seat]), deepcopy(obs['private'])
            a = game['steps'][i+1][seat]['action']
            for w, cmd in enumerate([a.get('farmer', ['PASS'])] + a.get('hands', [])):
                pos = engine._farmer_position(farm, w)
                if pos is None or not cmd: continue
                x, y = pos
                old = deepcopy(farm['tiles'][y][x])
                inv = deepcopy(private['inventories'][w])
                engine._apply_unit_action(farm, private, w, cmd, 10, obs['day'], 24, 100)
                tile = farm['tiles'][y][x]
                routes.append(dict(day=obs['day']+1, hour=obs['hour']+1, worker=w, x=x, y=y, command=cmd))
                if isinstance(tile, dict) and tile.get('kind') == 'PASTURE':
                    changed = tile != old
                    gain = {k: v-inv.get(k, 0) for k, v in private['inventories'][w].items() if v > inv.get(k, 0)}
                    if cmd[0] in ['BUILD_PASTURE', 'PLACE', 'FEED', 'CARE', 'HARVEST', 'COLLECT_FERTILIZER']:
                        events.append(dict(day=obs['day']+1, hour=obs['hour']+1, worker=w, x=x, y=y,
                                           op=cmd[0], command=cmd, animal=tile.get('animal'),
                                           effective=changed or bool(gain), gain=gain,
                                           cash_before=obs['farms'][seat]['money'], wheat_carried=inv.get('WHEAT', 0)))
                    if changed and (not isinstance(old, dict) or old.get('kind') != tile.get('kind') or old.get('animal') != tile.get('animal')):
                        transitions.append(dict(day=obs['day']+1, hour=obs['hour']+1, x=x, y=y,
                                                kind=tile.get('kind'), animal=tile.get('animal')))
        final = game['steps'][-1][seat]['observation']['farms'][seat]
        coords = [(x, y) for y, line in enumerate(final['tiles']) for x, t in enumerate(line) if isinstance(t, dict) and t.get('kind') == 'PASTURE']
        tile_daily = []
        for day in range(1, 31):
            obs = game['steps'][day*24-1][seat]['observation']
            for x, y in coords:
                tile = obs['farms'][seat]['tiles'][y][x]
                ev = [e for e in events if e['day'] == day and e['x'] == x and e['y'] == y and e['effective']]
                rec = dict(submission=f['opponent_submission'], episode=f['episode'], day=day, x=x, y=y,
                           animal=tile.get('animal', '') if isinstance(tile, dict) else '',
                           kind=tile.get('kind', '') if isinstance(tile, dict) else str(tile),
                           feed_hours=','.join(str(e['hour']) for e in ev if e['op'] == 'FEED'),
                           care_hours=','.join(str(e['hour']) for e in ev if e['op'] == 'CARE'),
                           harvest_hours=','.join(str(e['hour']) for e in ev if e['op'] == 'HARVEST'),
                           collected=sum(e['gain'].get('WOOL', 0)+e['gain'].get('MILK', 0) for e in ev if e['op'] == 'HARVEST'),
                           workers=','.join(map(str, sorted({e['worker'] for e in ev}))))
                tile_daily.append(rec); csvrows.append(rec)
        detail = dict(**f, seat=seat, source_sha256=profile['sha256'],
                      transitions=transitions, tile_daily=tile_daily, events=events,
                      routes=routes, daily=side['daily'], ledger=side.get('ledger'))
        (OUT / f"{f['episode']}.json").write_text(json.dumps(detail, separators=(',', ':')), encoding='utf-8')
        details.append(detail)
        print('EXTRACTED', f['episode'], f['opponent_submission'], 'events', len(events), flush=True)
    similarities = []
    for i, a in enumerate(details):
        for b in details[i+1:]:
            aa, bb = actions[a['episode']], actions[b['episode']]
            similarities.append(dict(a=a['opponent_submission'], b=b['opponent_submission'],
                                     exact_batches=sum(x == y for x, y in zip(aa, bb)),
                                     worker_batches=sum((x.get('farmer'), x.get('hands')) == (y.get('farmer'), y.get('hands')) for x, y in zip(aa, bb)), total=719))
    summary = dict(available_replays=len(families), frozen_games=len(cohort['games']),
                   selected_three_pastures=len(details), inventory=inventory,
                   pairwise_action_similarity=similarities,
                   target_transitions=[dict(submission=d['opponent_submission'], episode=d['episode'], mix=d['opponent_mix'], q2_coop=d['q2_coop'], transitions=[e for e in d['transitions'] if (e['x'], e['y']) in TARGETS]) for d in details])
    patterns = []
    for xy in TARGETS:
        observations = []
        for d in details:
            ev = [e for e in d['events'] if (e['x'], e['y']) == xy and e['op'] == 'HARVEST' and e['effective']]
            observations.append(dict(submission=d['opponent_submission'], harvest_days=[e['day'] for e in ev],
                                     units=[e['gain'].get('WOOL', 0) for e in ev]))
        patterns.append(dict(x=xy[0], y=xy[1], observations=observations))
    summary['harvest_patterns'] = patterns
    pair = [next(d for d in details if d['opponent_submission'] == sid) for sid in (56165125, 56205921)]
    def signature(d, xy):
        return [(e['day'], e['hour'], e['op'], e['effective'], e['gain']) for e in d['events'] if (e['x'], e['y']) == xy]
    summary['identical_q0_service'] = dict(submissions=[56165125, 56205921],
        coordinates=[dict(x=xy[0], y=xy[1], equal=signature(pair[0], xy)==signature(pair[1], xy),
                          requests=len(signature(pair[0], xy))) for xy in TARGETS])
    template = dict(status='Observed reusable pattern, not a tested policy or recovered source',
        schedule=[dict(x=3,y=2,place_day=11,place_hours=[19,20],harvest_days=[17,20,23,26,29]),
                  dict(x=2,y=3,place_day=12,place_hours=[7],harvest_days=[18,21,24,27,30]),
                  dict(x=4,y=1,place_day=11,place_hours=[20,21],harvest_days=[17,20,23,26,29],
                       optional=True,observed_empty_submissions=[56165125,56205921])],
        guards=['Check pasture and carried sheep before PLACE; purchase only with cash and room.',
                'Feed one carried wheat per animal/day, care only once; detect unsuccessful feed.',
                'Harvest actual positive yield from age 6 then every 3 days; cap 6 units.',
                'Deliver and sell final day wool; no terminal inventory valuation.',
                'Do not copy failed feed actions or infer intentional vacancy from absent placement.'],
        warning='6C10S must preserve full coordinate mix; 56171606 reaches 6C10S after losing a sheep at (5,2) on D10.')
    (OUT / 'OBSERVED_TEMPLATE.json').write_text(json.dumps(template,indent=2),encoding='utf-8')
    (OUT / 'SUMMARY.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    with (OUT / 'TILE_DAILY.csv').open('w', newline='', encoding='utf-8') as out:
        writer = csv.DictWriter(out, fieldnames=list(csvrows[0])); writer.writeheader(); writer.writerows(csvrows)
    intro = ('Analisi dei 20 replay E22 disponibili nel campione congelato di 78 partite. Tutti gli avversari sono inventariati; '
             'i sei con pascoli su tutte e tre le coordinate Q0 hanno estrazione dettagliata. Non sono 78 replay analizzati né repliche multiple della stessa submission. '
             'Le azioni di servizio sono riapplicate su copie dello stato precedente per distinguere esiti effettivi e richieste senza effetto. '
             'Le traiettorie usano coordinate zero-based e D/H visuali one-based; operaio 0 = fattore. Nessun codice sorgente degli avversari è stato recuperato.')
    md = '# Pascoli degli avversari E22: tipologie e traiettorie\n\n' + intro + '\n\n'
    md += '| Submission | Episodio | Mix finale | Pollaio Q2 | Margine su E22 | Fughe |\n|---|---|---|---|---:|---:|\n'
    for d in details: md += f"| {d['opponent_submission']} | {d['episode']} | {d['opponent_mix']} | {d['q2_coop']} | {-d['margin']:+,} | {d['opponent_escapes']} |\n"
    md += '\n## Costruzioni e collocamenti nelle tre coordinate\n\n'
    findings = ('Il motore ha un unico tipo PASTURE, utilizzabile da mucche o pecore: le tipologie osservate sono differenze di occupazione, mix e calendario. '
                'Tutti e sei i casi costruiscono (2,3) a D11 H15 e collocano la pecora a D12 H7. '
                '(3,2) viene costruito a D11 H18–19 e popolato a H19–20; (4,1) a H19–20, popolato a H20–21 in quattro casi e mai popolato negli altri due.\n\n'
                'La regola di raccolta si ripete in tutti i casi popolati: (3,2) e (4,1) a D17/20/23/26/29; (2,3) a D18/21/24/27/30. '
                'La prima raccolta rende 5–6 lane nei casi osservati; le successive spesso 4, ma scendono a 3 e in un caso a 1 quando il servizio diverge. '
                'Quindi è riproducibile il calendario relativo (età 6 giorni, poi ogni 3); la resa richiede verifica di alimentazione e cure.\n\n'
                '56165125 e 56205921 condividono tutte le 186 richieste di servizio sulle tre coordinate con identici giorno, ora, operazione, efficacia e quantità '
                '(62 in (4,1), 66 in (3,2), 58 in (2,3)); (4,1) resta sempre vuoto. Le azioni complete di tutti gli operai coincidono solo in 455/719 turni, '
                'le azioni complete incluse le transazioni in 420/719: il modulo Q0 è stabile, il piano globale no. '
                'I loro margini osservati su E22 sono +8.990 e +56.815: la stessa traiettoria Q0 non spiega da sola il risultato economico.\n\n'
                '56171606 popola anche (4,1), ma perde una pecora in (5,2) alla transizione D10: il suo 6C10S finale non equivale al 6C10S con pascolo vuoto. '
                '56124096 usa 5C11S; 56020742 9C8S; 56198022 espande oltre le tre caselle e chiude 7C14S2G. '
                'Manca la ripetizione della stessa submission su più seed nel campione disponibile: questa è evidenza di un modulo condiviso tra replay, non prova di robustezza del codice.\n\n'
                'Trasferimento consigliato: riusare collocamenti e cicli produttivi con controlli sullo stato; tenere separati 8C9S e replica 6C10S. '
                'Non riprodurre le alimentazioni fallite: nei due casi con pascolo vuoto (3,2) non riceve FEED efficace a D14/26/29 e (2,3) a D14/25. '
                'Il template osservato è in OBSERVED_TEMPLATE.json, i percorsi di tutti gli operai nei JSON per episodio.')
    md += findings + '\n\n'
    for d in details:
        md += f"### Submission {d['opponent_submission']} · episodio {d['episode']}\n\n"
        for e in d['transitions']:
            if (e['x'], e['y']) in TARGETS: md += f"- D{e['day']} H{e['hour']} · ({e['x']},{e['y']}) · {e['animal'] or 'pascolo vuoto'}\n"
        md += '\n'
    md += '\n[Dashboard mappe e traiettorie](REPORT.html) · [Tutte le traiettorie per casella, CSV](TILE_DAILY.csv) · [Sintesi e similarità](SUMMARY.json)\n'
    (OUT / 'REPORT.md').write_text(md, encoding='utf-8')
    body = '<h1>Pascoli nei replay E22</h1><p>' + intro + '</p><details open><summary>Comportamento riproducibile e limiti</summary><p>' + findings.replace('\n\n', '</p><p>') + '</p></details><p><a href="REPORT.md">Interpretazione</a> · <a href="TILE_DAILY.csv">Traiettorie CSV</a> · <a href="SUMMARY.json">Similarità tra piani</a> · <a href="OBSERVED_TEMPLATE.json">Template osservato</a></p><label>Submission <select id="match">'
    body += ''.join(f'<option value="{i}">{d["opponent_submission"]} · episodio {d["episode"]}</option>' for i, d in enumerate(details)) + '</select></label>'
    for i, d in enumerate(details):
        body += f'<section data-i="{i}"' + (' hidden' if i else '') + f'><h2>{d["opponent_submission"]} · {d["opponent_mix"]}</h2><p>Margine su E22 {-d["margin"]:+,}; fughe {d["opponent_escapes"]}. <a href="{d["episode"]}.json">Dati completi, eventi e percorsi di ogni operaio</a>.</p>'
        body += '<div class="maps">'
        for day in [1, 7, 10, 11, 12, 18, 24, 30]:
            cells = {(c['x'], c['y']): c for c in d['daily'][day-1]['cells']}
            body += f'<div><h3>D{day} H24</h3><div class="board">'
            for y in range(10):
                for x in range(10):
                    cell = cells.get((x, y), {})
                    animal = cell.get('animal'); kind = cell.get('kind', '')
                    label = {'COW': 'C', 'SHEEP': 'S', 'GOOSE': 'G'}.get(animal, 'P' if kind == 'PASTURE' else 'O' if kind == 'COOP' else '·')
                    color = '#bbdfc6' if animal == 'SHEEP' else '#a8c8ed' if animal == 'COW' else '#eee4bf' if kind == 'PASTURE' else '#eee'
                    body += f'<span style="background:{color};' + ('outline:2px solid #ca3a33;' if (x,y) in TARGETS else '') + f'" title="({x},{y}) {animal or kind}">{label}</span>'
            body += '</div></div>'
        body += '</div><p>C mucca · S pecora · G oca · P pascolo vuoto · O pollaio vuoto. Bordo rosso: tre coordinate Q0. Colonne x e righe y da 0 a 9.</p>'
        body += '<h3>Calendario di tutti i pascoli</h3><table><tr><th>Posizione</th><th>Costruzione / collocamenti effettivi</th></tr>'
        for xy in sorted({(e['x'],e['y']) for e in d['transitions']}):
            es = [e for e in d['transitions'] if (e['x'], e['y']) == xy]
            body += '<tr><td>' + str(xy) + '</td><td>' + '; '.join(f"D{e['day']} H{e['hour']}: {e['animal'] or 'PASTURE'}" for e in es) + '</td></tr>'
        body += '</table><h3>Servizio delle tre caselle Q0</h3><p>F = ore alimentazione; C = ore cura; R = ore raccolta e unità effettive. Trattino: nessuna azione efficace.</p><table><tr><th>Giorno</th>' + ''.join(f'<th>{xy}</th>' for xy in TARGETS) + '</tr>'
        for day in range(1,31):
            body += f'<tr><td>D{day}</td>'
            for x,y in TARGETS:
                t = next(t for t in d['tile_daily'] if t['day']==day and t['x']==x and t['y']==y)
                body += f"<td>{t['animal'] or t['kind']} · F {t['feed_hours'] or '—'} · C {t['care_hours'] or '—'} · R {t['harvest_hours'] or '—'} ({t['collected']})</td>"
            body += '</tr>'
        body += '</table></section>'
    body += '<script>document.getElementById("match").addEventListener("change",e=>document.querySelectorAll("section[data-i]").forEach(x=>x.hidden=x.dataset.i!==e.target.value));</script>'
    (OUT / 'REPORT.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Traiettorie pascoli E22</title><style>body{font:16px system-ui;max-width:1450px;margin:30px auto;padding:0 24px;color:#23372a;background:#f5f6f2}p{line-height:1.6}section{background:white;padding:24px;margin:20px 0;border-radius:12px}.maps{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}.board{display:grid;grid-template-columns:repeat(10,1fr);gap:2px}.board span{text-align:center;padding:4px;font-size:12px}table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:8px;text-align:left;border-bottom:1px solid #ddd}select{padding:10px;font:inherit}@media(max-width:950px){.maps{grid-template-columns:repeat(2,1fr)}} </style>' + body + '</html>', encoding='utf-8')
    print(json.dumps(summary['target_transitions']), flush=True)

if __name__ == '__main__': main()
