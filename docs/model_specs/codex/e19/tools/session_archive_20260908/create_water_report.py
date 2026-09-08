from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
s=(p/'build_animal_service_770_report.py').read_text(encoding='utf-8')
s=s.replace('reports/animal_service_770_20260908','reports/water_route_770_20260908').replace("else 'v41'","else 'v43'")
s=s.replace("['v33','v38','v39','v41']","['v33','v38','v39','v41','v43']",1)
s=s.replace("['v33','v38','v39','v40','v41']","['v41','v42','v43']")
a=s.index('    base=summary');b=s.index('    template=',a)
s=s[:a]+'''    base=summary['v41']
    diagnosis=f"""<h2>Copertura idrica e recupero del percorso</h2>
<p>La V41 protegge le visite animali a rischio e azzera le fughe, ma registra 26 perdite idriche sui sei casi. La V42 estende la precedenza di percorso e selezione alle colture gia rimaste un giorno senza acqua, mantenendo la visita completa. Nel caso preliminare azzera tutte le perdite, ma riduce superficie e competitivita: resta una prova su un solo caso.</p>
<p>La V43 conserva priorita e pianificazione V41. Per una coltura a rischio stima il completamento della visita dell'addetto assegnato, includendo missione attiva, tragitto, servizi precedenti e prelievi. Se il tempo stimato raggiunge il residuo meno due turni, oppure manca un addetto assegnato, permette il recupero fuori area. Non alza la priorita di tutte le irrigazioni e non considera l'acqua delle nuove semine un debito idrico esistente. La stima puo sovrastimare prelievi coperti dalla missione attiva; non e una garanzia di esecuzione.</p>
<p><strong>{chosen.upper()}, sei casi:</strong> cassa media {fmt(new['cash'])} contro {fmt(base['cash'])} V41, vittorie {new['wins']}/6 contro {base['wins']}/6. Perdite animali {new['animal_losses']} contro {base['animal_losses']}; perdite idriche {new['water_deaths']} contro {base['water_deaths']}. Coltivate mediane D25 {fmt(new['cultivated']['25'])} contro {fmt(base['cultivated']['25'])}; infestanti mediane D30 {fmt(new['weeds_D30'])} contro {fmt(base['weeds_D30'])}.</p>
<p>Tutte le fasi includono FEED, CARE, WATER, MOVE, PASS, portafoglio e semine. Il margine sulla cassa avversaria e distinto dalle vittorie. Tre semi di sviluppo nelle due posizioni: non sono sei semi indipendenti. Top770-001 e un corpus storico descrittivo; i confronti locali usano gli stessi casi. Le fasce rappresentano min-max osservati.</p>
<p>Prefisso D1–D11, topologia 7–7–0 e completamento delle partite verificati, nessun errore o missione incompleta. D26–D30 conserva la chiusura precedente. Solo 770, nessuna submission. V33 resta riferimento, V29 pubblicata. Sorgenti e dati verificati con SHA256.</p>
<h2>Valutazione</h2><p>Il recupero idrico va giudicato insieme alla superficie e alla cassa: una riduzione delle perdite non basta se la produzione arretra. Questa revisione resta un esperimento locale.</p>"""
''' +s[b:]
s=s.replace("('V39','V39 locale',aggregate(prof('v39')),'TOP770')","('V39','V39 locale',aggregate(prof('v39')),'TOP770'),('V41','V41 locale',aggregate(prof('v41')),'TOP770')")
s=s.replace("BASE/'tests/test_protected_routes_v40.py'","BASE/'tests/test_protected_routes_v40.py',BASE/'tests/test_biological_protection_v42.py',BASE/'tests/test_water_route_rescue_v43.py'")
(p/'build_water_route_770_report.py').write_text(s,encoding='utf-8')
