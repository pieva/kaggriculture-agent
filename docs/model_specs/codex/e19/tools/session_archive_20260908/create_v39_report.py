from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
s=(p/'build_biological_deadlines_770_report.py').read_text(encoding='utf-8')
s=s.replace('reports/biological_deadlines_770_20260908','reports/spent_renewal_770_20260908').replace("else 'v38'","else 'v39'")
s=s.replace("['v33','v35','v38']","['v33','v38','v39']").replace("['v33','v34','v35','v36','v37','v38']","['v33','v38','v39']")
a=s.index('    diagnosis=f');b=s.index('    template=',a)
s=s[:a]+'''    base=summary['v33'];previous=summary['v38']
    diagnosis=f"""<h2>Rinnovo delle colture a fine ciclo: V39</h2>
<p>La V39 conserva il calendario idrico alternato della V38. Corregge l'esclusione dal rinnovo delle piante perenni già raccolte e giunte all'ultima produzione: possono ricevere DIG, PLANT e WATER nella stessa visita, senza un HARVEST vuoto. Il percorso ammette queste sostituzioni anche quando manca una visita ordinaria. Le produzioni future e il prodotto ancora presente sono protetti.</p>
<p>Quando una nuova fragola non arriverebbe alla prima produzione entro fine partita, il piano confronta grano e carote per margine corrente stimato per giorno, limitandosi a cicli con maturazione completa e un giorno residuo. Non è ancora una pianificazione della chiusura: i prezzi futuri non sono previsti e la selezione può favorire il grano. D26–D30 mantiene il precedente controllo.</p>
<p><strong>Sei casi V39:</strong> cassa media {fmt(new['cash'])}, contro {fmt(previous['cash'])} della V38 e {fmt(base['cash'])} della V33. Vittorie contro V4D: {new['wins']}/6; scarto medio relativo {fmt(new['relative_pct'])}%. Morti idriche: {new['water_deaths']}, contro {previous['water_deaths']} e {base['water_deaths']}. Coltivate mediane D25: {fmt(new['cultivated']['25'])}, contro {fmt(previous['cultivated']['25'])} e {fmt(base['cultivated']['25'])}. Infestanti mediane D30: {fmt(new['weeds_D30'])}, contro {fmt(previous['weeds_D30'])} e {fmt(base['weeds_D30'])}.</p>
<p>Il miglioramento di superficie va valutato insieme a PASS, MOVE, acqua, FEED, CARE, perdite e cassa. Le tabelle presentano tutte le fasi e tutti i casi; le fasce dei grafici sono minimi e massimi osservati, non intervalli di confidenza. Le infestanti comprendono anche fine ciclo, non soltanto morte per sete.</p>
<p>Prefisso D1–D11 identico, topologia 7–7–0, simulazioni complete, zero errori e missioni incomplete verificati. Quattro controlli mirati proteggono le produzioni future e l'ordine dei comandi. Sei casi già utilizzati nello sviluppo, tre semi nelle due posizioni: non costituiscono validazione indipendente. Il mercato condiviso modifica anche la cassa avversaria. Top770-001 è un corpus storico descrittivo, V33 e V38 usano gli stessi casi locali.</p>
<h2>Decisione</h2><p>V39 rimane un esperimento locale: nessuna promozione automatica o pubblicazione. V33 resta il riferimento e V29 la submission esterna. Occorre ancora valutare il portafoglio di chiusura e le perdite residue; 662 non modificata.</p>"""
''' +s[b:]
s=s.replace("('V33','V33 locale',aggregate(prof('v33')),'TOP770')", "('V33','V33 locale',aggregate(prof('v33')),'TOP770'),('V38','V38 locale',aggregate(prof('v38')),'TOP770')")
s=s.replace('V34 è confrontata su un solo caso.','V33, V38 e V39 sono confrontate sugli stessi sei casi.')
s=s.replace("BASE/'tests/test_biological_water_calendar_v38.py'","BASE/'tests/test_biological_water_calendar_v38.py',BASE/'tests/test_spent_renewal_v39.py'")
(p/'build_spent_renewal_770_report.py').write_text(s,encoding='utf-8')
