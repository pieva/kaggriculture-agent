from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
s=(p/'build_final_water_770_report.py').read_text(encoding='utf-8')
s=s.replace('reports/final_water_770_20260908','reports/productive_water_770_20260908').replace("else 'v47'","else 'v48'")
s=s.replace("['v33','v38','v39','v41','v44','v45','v46','v47']","['v33','v38','v39','v41','v44','v45','v46','v47','v48']",1)
s=s.replace("['v41','v45','v46','v47']","['v41','v45','v47','v48']")
s=s.replace("zip(groups['v45'],groups[chosen])","zip(groups['v47'],groups[chosen])")
s=s.replace("closing_versions=['v41','v45','v46',chosen]","closing_versions=['v41','v45','v47',chosen]")
a=s.index("    base=summary['v45']");b=s.index('    template=',a)
s=s[:a]+'''    base=summary['v47']
    diagnosis=f"""<h2>Acqua produttiva prima della raccolta: V48</h2>
<p>La V47 riduce una visita in scadenza al solo HARVEST. Nel motore WATER puo ancora aggiungere resa alle colture annuali, se non irrigate oggi, nella finestra di maturazione e sotto la resa massima. La V48 conserva WATER prima di HARVEST in questi casi, solo a D28–D30. Il valore della visita include l'incremento stimato al prezzo corrente; non promette un prezzo futuro.</p>
<p>Il solo HARVEST resta disponibile con priorita inferiore. Se il lavoro completo non entra nel tempo residuo, il dispatcher non puo trasformarlo nel solo WATER: considera la raccolta breve. Le due alternative vengono preparate con i normali controlli di percorso e ritorno al deposito. Non aggiunge irrigazioni a piante gia irrigate, a resa massima o perenni; non modifica le scelte precedenti a D28.</p>
<p><strong>{chosen.upper()}, sei casi:</strong> cassa media {fmt(new['cash'])} contro {fmt(base['cash'])} V47; vittorie {new['wins']}/6 contro {base['wins']}/6; perdite idriche {new['water_deaths']} contro {base['water_deaths']}; perdite animali {new['animal_losses']} contro {base['animal_losses']}; infestanti mediane D30 {fmt(new['weeds_D30'])} contro {fmt(base['weeds_D30'])}.</p>
<p>Consistenze, ledger giornalieri e KPI operativi D1–D27 verificati uguali a V47. Le tabelle distinguono raccolte, vendite e prezzo realizzato nel mercato condiviso. Tre semi di sviluppo nelle due posizioni, non sei semi indipendenti. Top770-001 e un corpus storico descrittivo. Prefisso, topologia 7–7–0 e completamento verificati; nessun errore o missione incompleta. Solo 770, nessuna submission.</p>
<h2>Valutazione</h2><p>Il test deve dimostrare un incremento di prodotto raccolto e venduto, non soltanto piu WATER. La raccolta breve di ripiego resta necessaria: l'aumento di resa non deve causare la perdita della raccolta.</p>"""
''' +s[b:]
s=s.replace("('TOP770','Top770-001',aggregate(top,frozen),'V45')","('TOP770','Top770-001',aggregate(top,frozen),'V47')")
s=s.replace("('V46','V46 locale',aggregate(prof('v46')),'TOP770')","('V46','V46 locale',aggregate(prof('v46')),'TOP770'),('V47','V47 locale',aggregate(prof('v47')),'TOP770')")
s=s.replace("BASE/'tests/test_final_water_v47.py'","BASE/'tests/test_final_water_v47.py',BASE/'tests/test_productive_water_v48.py'")
(p/'build_productive_water_770_report.py').write_text(s,encoding='utf-8')
