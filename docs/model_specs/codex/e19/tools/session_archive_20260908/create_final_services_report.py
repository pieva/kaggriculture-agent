from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
s=(p/'build_closure_bridge_770_report.py').read_text(encoding='utf-8')
s=s.replace('reports/closure_bridge_770_20260908','reports/final_services_770_20260908').replace("else 'v45'","else 'v46'")
s=s.replace("['v33','v38','v39','v41','v44','v45']","['v33','v38','v39','v41','v44','v45','v46']",1)
s=s.replace("['v41','v44','v45']","['v41','v45','v46']")
s=s.replace("zip(groups['v44'],groups[chosen])","zip(groups['v45'],groups[chosen])").replace('[:25]','[:27]').replace('D1-D25 ledger','D1-D27 ledger')
s=s.replace('[(12,20),(21,25),(26,27),(26,30)]','[(12,20),(21,25),(26,27),(28,30)]')
s=s.replace("closing_versions=['v41','v44',chosen]","closing_versions=['v41','v45',chosen]").replace("['daily'][25:]","['daily'][27:]").replace('Raccolte e vendite D26–D30','Raccolte e vendite D28–D30').replace('precedenti a D26','precedenti a D28')
a=s.index("    base=summary['v44']");b=s.index('    template=',a)
s=s[:a]+'''    base=summary['v45']
    diagnosis=f"""<h2>Servizi fino a D29: V46</h2>
<p>Nella V45 FEED passa da 14 interventi a D27 a 5,67 medi a D28, quando termina la gestione pianificata. La V46 mantiene pianificazione, percorsi e priorita fino a D29 incluso. CARE a D28–D29 viene proposto solo se il suo bonus puo essere utilizzato da una produzione entro fine partita, tenendo conto del ciclo e della capacita di prodotto detenuto. FEED rimane attivo; a D30 torna la gestione terminale precedente.</p>
<p>Restano le scadenze delle semine della V45: nessun nuovo ciclo pianificato da D27, mentre le colture gia presenti vengono servite e raccolte. Consistenze, ledger giornalieri e KPI operativi D1–D27 sono verificati uguali a V45. La modifica riguarda la transizione finale.</p>
<p><strong>{chosen.upper()}, sei casi:</strong> cassa media {fmt(new['cash'])} contro {fmt(base['cash'])} V45; vittorie {new['wins']}/6 contro {base['wins']}/6; perdite idriche {new['water_deaths']} contro {base['water_deaths']}; perdite animali {new['animal_losses']} contro {base['animal_losses']}; infestanti mediane D30 {fmt(new['weeds_D30'])} contro {fmt(base['weeds_D30'])}.</p>
<p>Le tabelle distinguono raccolte, vendite e prezzo realizzato nel mercato condiviso. Tre semi di sviluppo nelle due posizioni, non sei semi indipendenti. Top770-001 e un corpus storico descrittivo. Prefisso, topologia 7–7–0 e completamento verificati; nessun errore o missione incompleta. Solo 770, nessuna submission.</p>
<h2>Valutazione</h2><p>Valutare insieme servizi, spostamenti, PASS, raccolte e cassa. Conservare i riferimenti precedenti: nessuna promozione automatica basata sul solo aumento di FEED.</p>"""
''' +s[b:]
s=s.replace("('TOP770','Top770-001',aggregate(top,frozen),'V44')","('TOP770','Top770-001',aggregate(top,frozen),'V45')")
s=s.replace("('V44','V44 locale',aggregate(prof('v44')),'TOP770')","('V44','V44 locale',aggregate(prof('v44')),'TOP770'),('V45','V45 locale',aggregate(prof('v45')),'TOP770')")
s=s.replace("BASE/'tests/test_closure_bridge_v45.py'","BASE/'tests/test_closure_bridge_v45.py',BASE/'tests/test_final_services_v46.py'")
(p/'build_final_services_770_report.py').write_text(s,encoding='utf-8')
