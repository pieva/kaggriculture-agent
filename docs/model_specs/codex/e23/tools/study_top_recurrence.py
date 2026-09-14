"""Read the frozen 25-replay atlas; extract successful crop starts and price paths."""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

SOURCE = Path('C:/Users/pietr/.codex/worktrees/756c/kaggriculture-agent')
ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT / 'docs/model_specs/codex/e23/reports/recurrence_20260914'
ATLAS = SOURCE / 'docs/model_specs/codex/e22/reports/top_2750_3000_20260914'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cohort = json.loads((ATLAS / 'COHORT.json').read_text())
    results = []
    for entry in cohort:
        raw = (SOURCE / entry['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == entry['sha256']
        replay = json.loads(raw)
        seat = entry['seat']
        assert len(replay['steps']) == 720
        observations = [s[seat]['observation'] for s in replay['steps']]
        crops, animals = [], []
        last_crop = {}
        for step in range(1, 720):
            before, after = observations[step-1:step+1]
            old_tiles = before['farms'][seat]['tiles']
            for y, row in enumerate(after['farms'][seat]['tiles']):
                for x, tile in enumerate(row):
                    old = old_tiles[y][x]
                    old = old if isinstance(old, dict) else {}
                    if old.get('crop'):
                        last_crop[x, y] = old['crop']
                    if not isinstance(tile, dict):
                        continue
                    if tile.get('crop') and (old.get('crop'), old.get('planted_day')) != (tile['crop'], tile.get('planted_day')) and tile.get('planted_day') == before['day']:
                        crops.append(dict(day=before['day']+1, hour=before['hour']+1, x=x, y=y,
                                          previous=last_crop.get((x,y)), crop=tile['crop'],
                                          price=before['market']['prices'][tile['crop']], shops=before['town']['unlocked_shops']))
                    if tile.get('animal') and old.get('animal') != tile['animal']:
                        animals.append(dict(day=before['day']+1, x=x, y=y, previous=old.get('animal'), animal=tile['animal']))
        daily = []
        for day in range(1, 31):
            obs = observations[day*24-1]
            cells = [t for row in obs['farms'][seat]['tiles'] for t in row if isinstance(t, dict)]
            daily.append(dict(day=day, crops=dict(Counter(t['crop'] for t in cells if t.get('crop'))),
                              animals=dict(Counter(t['animal'] for t in cells if t.get('animal'))), prices=obs['market']['prices']))
        price_stats = {}
        for product in ['WOOL','MILK','EGG','STRAWBERRY','TOMATO']:
            prices = [d['prices'][product] for d in daily[11:]]
            peak = prices[0]
            drawdown = 0
            for price in prices:
                peak = max(peak, price)
                drawdown = max(drawdown, (peak-price)/peak)
            price_stats[product] = dict(max_drawdown=drawdown, down_days=sum(b<a for a,b in zip(prices,prices[1:])),
                                        low_price_days=sum(p<=20 for p in prices))
        results.append(dict(submission=entry['submission'], score=entry['score'], episode=entry['episode'],
                            sha256=entry['sha256'], crops=crops, animal_starts=animals, daily=daily, price_stats=price_stats))
        print('READ',entry['episode'],flush=True)
    (OUT/'ANALYSIS.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# E23 — ricorrenze colturali e prezzi nei top 2750–3000', '',
             'Analisi aggiuntiva del campione congelato il 14 settembre: cinque submission, cinque replay ciascuna. Tutti i 25 hash verificati. Nessuna nuova simulazione o lettura live del rating.', '',
             'Semine: nuove colture effettivamente osservate, con planted_day coerente; precedente = ultima coltura osservata sulla casella, anche se rimossa in un turno precedente. Le mappe sono checkpoint H24 prima dell’eventuale ultima azione. Frequenze descrittive, non prova di rendimento.', '']
    for sid in sorted({r['submission'] for r in results}):
        games = [r for r in results if r['submission']==sid]
        lines += [f'## Submission {sid} — score selezione {games[0]["score"]}', '', '| Replay | Colture D20 | Colture D25 | Colture D29 |', '|---|---|---|---|']
        for game in games:
            values = ['; '.join(f'{k}:{v}' for k,v in sorted(game['daily'][d-1]['crops'].items())) for d in [20,25,29]]
            lines.append(f'| {game["episode"]} | '+ ' | '.join(values)+' |')
        frequency = Counter()
        for game in games:
            frequency.update(set((c['day'], c['previous'] or 'vuoto', c['crop']) for c in game['crops'] if c['day']>=12))
        lines += ['', 'Successioni giorno/specie presenti in almeno 3/5 replay (non implicano uguali coordinate o quantità):', '']
        for (day, old, new), n in sorted(frequency.items()):
            if n>=3:
                counts=[sum(c['day']==day and (c['previous'] or 'vuoto')==old and c['crop']==new for c in g['crops']) for g in games]
                lines.append(f'- D{day}: {old} → {new}, {n}/5; caselle per replay {counts}.')
        lines.append('')
    lines += ['## Stabilità dei prezzi D12–D30', '', 'Prezzi ai 19 checkpoint giornalieri, non prezzi realizzati. Drawdown = massima caduta percentuale da un massimo precedente nella stessa partita. Media sui 25 replay; mercato condiviso con avversario. Non misura causalmente l’effetto delle nostre vendite.', '', '| Prodotto | Drawdown massimo medio | Giorni in calo medi (su 18) | Giorni prezzo ≤20 medi (su 19) |', '|---|---:|---:|---:|']
    for product in ['WOOL','MILK','EGG','STRAWBERRY','TOMATO']:
        stats=[r['price_stats'][product] for r in results]
        lines.append(f'| {product} | {mean(s["max_drawdown"] for s in stats):.1%} | {mean(s["down_days"] for s in stats):.2f} | {mean(s["low_price_days"] for s in stats):.2f} |')
    lines += ['', 'Le sostituzioni animali dirette sono registrate separatamente dalle nuove collocazioni: una scomparsa o una fuga non è classificata come rotazione deliberata. Per stimare il beneficio delle successioni servono vendite realizzate, servizi, capitale e confronto della scelta alternativa nello stesso mercato.', '']
    (OUT/'REPORT.md').write_text('\n'.join(lines),encoding='utf-8')


if __name__ == '__main__':
    main()
