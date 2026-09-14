"""Render completed coop/crop audit and paired terminal cash results."""
import hashlib
import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e22/reports/e22_1_q2_coop_20260914'


def main():
    results=json.loads((OUT/'CROP_COUNTERFACTUALS.json').read_text())
    summary=json.loads((OUT/'CROP_SUMMARY.json').read_text())
    patterns={xy:dict(Counter(str(r['arms'][0]['neighborhood'][1]['tiles'][xy].get('crop')) for r in results)) for xy in ['3,6','4,7','2,6','2,8']}
    assert patterns['3,6']=={'WHEAT':20} and patterns['4,7']=={'WHEAT':20}
    md='''# E22.1 — dal pollaio vuoto alla coltura finale

**Sì: conviene riutilizzare (3,7) con una coltura breve seminata a D28.** Il pollaio previsto a D29 H5 resta vuoto in tutti i 20 replay e non produce reddito. Con il motore effettivo, grano e carote aggiungono due unità raccolte e vendute entro D30, senza assunzioni aggiuntive e senza ridurre le altre raccolte verificate.

## Risultati economici

| Successione dopo le fragole | Incremento medio cassa | Minimo | Massimo | Replay positivi | Costo seme |
|---|---:|---:|---:|---:|---:|
'''
    for name,label,cost in [('WHEAT','Grano',10),('CARROT','Carote',20)]:
        s=summary[name]
        md+=f"| {label} | +{s['mean']:.2f} | +{s['min']:.0f} | +{s['max']:.0f} | {s['positive']}/20 | {cost} |\n"
    md+='''
Gli incrementi sono differenze della cassa finale dell'intera fattoria, dopo costo del seme, vendite effettive e cambiamenti di prezzo. Non sono stime ottenute moltiplicando il raccolto per un prezzo fisso. Nessun acquisto di fertilizzante; acqua senza costo monetario diretto. Il costo della manodopera resta invariato: si riassegnano comandi all'interno delle giornate già pagate. Carote migliori del grano in 11/20 casi; il vantaggio medio di 4,15 non prova una superiorità generale.

## Abbinamento con le caselle vicine

| Casella | Situazione a D28 | Coltura finale D29–D30 | Collegamento operativo |
|---|---|---|---|
| (3,7) | Ultima raccolta fragole D28 H6; DIG H7 | Nuovo grano o carote | Stesso lavoratore 10, semina H8 e acqua H9 |
| (3,6), nord | Fragole a fine ciclo | Grano, 20/20 replay | Stesso calendario di maturazione D30 |
| (4,7), est | Fragole a fine ciclo | Grano, 20/20 replay | Il lavoratore 10 lo raccoglie a D30, poi visita (3,7) |
| (2,7), ovest | Ultime fragole | Liberata a D29 | Attraversata dal giro del lavoratore 6 |
| (3,8), sud | Ultime fragole | Fine ciclo; nessuna nuova coltura | Il DIG subito dopo la raccolta si può omettere |
| (2,6), nord-ovest | Fragole a fine ciclo | Grano | Altra successione breve già presente |
| (2,8), sud-ovest | Carote | Carote | Conferma che anche la seconda alternativa è compatibile col settore |

**Scelta consigliata per un calendario semplice: grano in (3,7).** Si inserisce nel gruppo di grano a nord ed est, ha il seme meno caro e il minimo incremento osservato più alto. Le carote restano un'alternativa valida con rendimento medio leggermente maggiore; nei due esperimenti hanno esattamente lo stesso costo di manodopera. L'omogeneità delle colture, da sola, non fa risparmiare comandi nel motore: il risparmio concreto deriva dalle visite condivise e dalla consegna accorpata.

## Calendario verificato e manodopera

1. D28: si conservano raccolta fragole H6 e DIG H7. Il lavoratore 10 semina a H8 e irriga a H9. Il seme viene acquistato a H7, prima del turno di semina, evitando conflitti con le altre richieste PLANT.
2. Per recuperare i due comandi, si omettono il DIG finale in (3,8) e l'acqua non produttiva D28 delle carote giovani in (1,7). Il controllo dei 20 casi conferma la sopravvivenza e la raccolta invariata delle carote; il percorso torna al calendario originale prima di fine giornata.
3. D29 H5: il lavoratore 6, già in (3,7), irriga invece di costruire il pollaio. Non cambia percorso.
4. D30: il lavoratore 10, dopo il grano di (4,7), compie WEST → WATER → HARVEST → EAST. Irrigazione H9 e raccolta H10 in (3,7), per due unità. Si eliminano un PASS iniziale e la prima consegna intermedia, si usano due PASS finali e si accorpa il trasporto alla consegna H22. Le vendite H22 incassano i prodotti entro la chiusura.

Non basta cambiare BUILD_COOP in PLANT a D29: la maturazione minima di due giorni cadrebbe a D31. Nuove fragole, pomodori e meloni sono troppo lenti. Anche (4,5) viene liberata solo a D29 H3 nel calendario attuale: non offre la stessa finestra senza anticipare altre operazioni. Per questo il test conserva le fragole esistenti fino all'ultima raccolta e usa direttamente (3,7).

## Metodo e limiti

20 replay E22.1, submission 56206528, con hash originali verificati. Per ogni replay: ripartenza dallo stato reale all'inizio di D28 e tre esecuzioni del motore fino alla fine, baseline + grano + carote (60 esecuzioni). La baseline riproduce esattamente fattorie, inventari privati e mercato a ogni passo. Le altre due esecuzioni mantengono le azioni avversarie registrate e ricalcolano prezzi, consumi e cassa.

Verificati: due unità aggiuntive, nessuna diminuzione delle altre raccolte confrontate, identici inventari e semi finali alla baseline e nessun prodotto aggiuntivo invenduto. Il confronto automatico dei totali di raccolta esclude i ritorni notturni H24; i comandi H24 restano invariati. È un esperimento diagnostico su avversari congelati e su un intervento scelto guardando questi replay, non un test indipendente o un aumento dimostrato del rating. Le due colture sono state provate solo nel piano locale dell'esperimento: nessuna modifica ai bundle E22.1 o E22.2 fix pubblicata.

[Risultati sintetici](CROP_SUMMARY.json) · [Stati, comandi e cassa per replay](CROP_COUNTERFACTUALS.json) · [Audit del pollaio e delle due caselle](EVIDENCE.json).
'''
    (OUT/'REPORT.md').write_text(md,encoding='utf-8')
    def inline(s):
        s=html.escape(s)
        s=re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',s)
        return re.sub(r'\[([^]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',s)
    blocks=[]
    for part in md.strip().split('\n\n'):
        if part.startswith('# '):blocks.append('<h1>'+inline(part[2:])+'</h1>')
        elif part.startswith('## '):blocks.append('<h2>'+inline(part[3:])+'</h2>')
        elif part.startswith('|'):
            rows=part.splitlines(); table='<table>'
            for i,row in enumerate(rows):
                if i==1:continue
                tag='th' if i==0 else 'td'
                table+='<tr>'+''.join(f'<{tag}>{inline(v.strip())}</{tag}>' for v in row.strip('|').split('|'))+'</tr>'
            blocks.append('<div class="table">'+table+'</table></div>')
        elif part.startswith('1. '):blocks.append('<ol>'+''.join('<li>'+inline(re.sub(r'^\d+\. ','',line))+'</li>' for line in part.splitlines())+'</ol>')
        else:blocks.append('<p>'+inline(part)+'</p>')
    (OUT/'REPORT.html').write_text('''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>E22.1 · Coltura finale Q2</title><style>body{font:16px/1.6 system-ui;background:#f2f5f8;color:#203348;margin:0}main{max-width:1060px;margin:36px auto;background:white;padding:32px;border-radius:16px}h1{font-size:32px;line-height:1.2}h2{margin-top:32px;color:#126153}.table{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:10px;border-bottom:1px solid #dbe4e9}th{background:#e8f4ef}a{color:#126153}li{margin:12px 0}p{max-width:96ch}@media(max-width:700px){main{margin:0;padding:18px}h1{font-size:26px}}</style></head><body><main>'''+''.join(blocks)+'</main></body></html>',encoding='utf-8')
    manifest=[dict(path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(OUT.iterdir()) if p.is_file() and p.name not in ['MANIFEST.json','CROP_RUN.log']]
    (OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(dict(summary=summary,neighbors=patterns),indent=2))


if __name__=='__main__':main()
