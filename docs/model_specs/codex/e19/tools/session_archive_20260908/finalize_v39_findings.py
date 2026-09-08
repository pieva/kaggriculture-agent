from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools/build_spent_renewal_770_report.py')
s=p.read_text(encoding='utf-8').replace("('Morti idriche totali','water_deaths')", "('Morti idriche totali','water_deaths'),('Perdite animali totali','animal_losses'),('Vittorie contro V4D','wins')")
s=s.replace('<h2>Decisione</h2><p>V39 rimane un esperimento locale:', '<h2>Regressione da correggere: servizi animali</h2><p>V39 perde quattro animali complessivi, tutti a D23: uno per partita sui semi 180903001 e 180903003, in entrambe le posizioni. V33 e V38 ne perdevano zero. Le vittorie scendono da 6/6 della V38 a 4/6. Tra D21 e D25 FEED medio passa da 13,6 a 13,2 e CARE da 11,53 a 11; PLANT cresce da 3,27 a 6,67. Il rinnovo migliora il portafoglio ma non mantiene la copertura dei servizi. La fattibilita del percorso stimato non garantisce che venga poi eseguito: serve riservare ed eseguire i servizi animali prima di impegnare altra capacita nei rinnovi. Questa e una direzione di correzione, non una causa dimostrata con una prova isolata.</p><h2>Decisione</h2><p>V39 non sostituisce V38 o V33 a causa delle nuove perdite animali. Rimane un esperimento locale:')
p.write_text(s,encoding='utf-8')
for name in ['docs/NEW_SESSION.md','docs/PROJECT_STATE.md']:
    p=Path(name);s=p.read_text(encoding='utf-8')
    s=s.replace('Solo 770. V39 deriva', 'ATTENZIONE: V39 non promossa. Quattro perdite animali a D23 (semi 001 e 003, entrambe le posizioni), contro zero V33/V38; vittorie 4/6 contro 6/6 V38. Rinnovi migliorano ma copertura FEED/CARE regredisce. Prossimo intervento: proteggere esecuzione dei servizi animali nel carico dei rinnovi.\n\nSolo 770. V39 deriva',1)
    p.write_text(s,encoding='utf-8')
