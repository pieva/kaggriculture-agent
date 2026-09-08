from pathlib import Path
b=Path('docs/model_specs/codex/e19/tools')
s=(b/'build_renewal_770_report.py').read_text(encoding='utf-8')
s=s.replace('renewal_certificate_770_20260908','biological_deadlines_770_20260908')
s=s.replace("else 'v32'", "else 'v35'")
s=s.replace("['v29','v32','v33']", "['v33','v35','v36']")
s=s.replace("['v29','v30','v31','v32','v33']", "['v33','v34','v35','v36']")
start=s.index('    diagnosis=f')
end=s.index("    template=Path(__file__)",start)
diagnosis='''    diagnosis=f"""<h2>Proteggere i servizi senza abbandonare la produzione</h2>
<p>Partenza dalla V33. La V34 dà precedenza assoluta a WATER/FEED in scadenza e consente il recupero fuori area fin dal mattino. Nel caso preliminare azzera le morti idriche ma riduce fortemente superficie e cassa: il miglioramento di un solo KPI non basta. Rimane una prova su un caso, non una revisione promossa.</p>
<p>La V35 conserva le aree assegnate. Per ogni servizio in scadenza stima quando l'addetto lo raggiungerà, includendo missione attiva, spostamenti, prelievi e visite che lo precedono nella coda. Se la stima raggiunge o supera il tempo residuo, il servizio può essere recuperato da un altro lavoratore. Resta il precedente recupero nelle ultime sei ore. Acqua e cibo in scadenza ricevono precedenza sulle nuove coltivazioni.</p>
<p>La V36 assegna precedenza anche alla visita completa che contiene il servizio urgente: acqua, raccolta e gli altri comandi già previsti vengono conservati insieme. Il servizio breve rimane disponibile come alternativa. L'obiettivo è evitare di risparmiare una pianta al prezzo di due viaggi e di una raccolta persa.</p>
<p><strong>{chosen.upper()}, sei casi:</strong> cassa media {fmt(new['cash'])}, V4D avversaria {fmt(new['opponent_cash'])}, scarto relativo {fmt(new['relative_pct'])}%. Morti idriche {new['water_deaths']}, perdite animali {new['animal_losses']}, perdite inventario {new['inventory_loss']} unità. Infestanti mediane D30: {fmt(new['weeds_D30'])}. Casi senza semine in entrambi D21–D22: {new['zero_sowing_cases']}/6. Grano mediano D20–D25: {', '.join(fmt(x) for x in new['wheat'].values())}.</p>
<p>Il confronto va letto su tutte le colonne: cassa propria e avversaria, coltivate, fragole, grano, carote, MOVE, PASS, WATER, FEED e CARE. Il mercato è condiviso: produrre e vendere diversamente modifica anche i risultati di V4D. Una crescita della sola cassa non dimostra maggiore competitività.</p>
<p>La previsione del ritardo è una stima sul piano corrente, non una garanzia multigiorno. Le infestanti possono derivare da sete oppure dalla fine del ciclo: lo stock finale non equivale al numero di morti idriche. D26–D30 conserva la chiusura precedente; il calendario dedicato delle carote resta aperto.</p>
<p>Verificati prefisso D1–D11 identico, topologia 7–7–0, 719 chiamate e 720 stati per partita, assenza di errori e missioni incomplete. Tempi misurati localmente con simulazioni concorrenti, non su Kaggle. Sei casi già usati nello sviluppo: nessuna validazione indipendente o nuova submission. Solo 770; 662 non modificata.</p>"""
'''
s=s[:start]+diagnosis+s[end:]
s=s.replace('Successione certificata ', 'Scadenze biologiche ').replace(': visita raccolta–risemina e controllo dei percorsi.', ': servizio urgente, percorsi e produzione.')
s=s.replace("'V29'", "'V33'").replace("'V29 locale'", "'V33 locale'").replace("prof('v29')", "prof('v33')")
s=s.replace('le prove V30 e V31 sono confrontate su un solo caso. V29 è la versione pubblicata, riesaminata qui sul corpus locale.', 'V34 è confrontata su un solo caso. V33 è il riferimento locale scelto dall’utente; V29 resta la submission pubblicata.')
s=s.replace('Prove preliminari su un caso riportate separatamente.', 'Prove preliminari su un caso riportate separatamente.')
s=s.replace("ROOT/'scratch/diagnose_v29_succession.py',ROOT/'scratch/v29_succession_diagnosis.json',ROOT/'scratch/run_v31_diagnostic.py',RAW/'daily_routes_v31_diagnostic_180903001_0.json',", '')
(b/'build_biological_deadlines_770_report.py').write_text(s,encoding='utf-8')
