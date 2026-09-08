from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
s=(p/'build_spent_renewal_770_report.py').read_text(encoding='utf-8')
s=s.replace('reports/spent_renewal_770_20260908','reports/animal_service_770_20260908').replace("else 'v39'","else 'v41'")
s=s.replace("['v33','v38','v39']","['v33','v38','v39','v41']",1)
s=s.replace("for v in ['v33','v38','v39']:","for v in ['v33','v38','v39','v40','v41']:")
s=s.replace("len(r['crop_starvation']),*[", "len(r['crop_starvation']),sum(d['verified_animal_losses'] for d in r['operational_daily']),*[")
s=s.replace("['Versione','Cassa','Morti idriche','Semine D21'", "['Versione','Cassa','Morti idriche','Perdite animali','Semine D21'")
a=s.index('    base=summary');b=s.index('    template=',a)
s=s[:a]+'''    base=summary['v39']
    diagnosis=f"""<h2>Protezione delle visite animali durante i rinnovi</h2>
<p>La V39 recupera terreno con i rinnovi ma perde quattro animali a D23. Nel motore due giornate consecutive senza FEED causano la fuga: CARE da solo non la evita. Nel dispatcher V39 una successione urgente precede i servizi animali; il percorso a inserimento puo inoltre collocare semine prima di FEED. Il certificato verifica un piano possibile, non impone che venga eseguito.</p>
<p>La V40 prova una precedenza generale alle visite complete con FEED o CARE, sia nel percorso sia nella selezione delle missioni. La prova su un caso perde molta cassa ed e scartata senza estensione a sei casi. La V41 restringe questa protezione alle visite degli animali gia rimasti senza cibo il giorno precedente. Queste visite possono essere recuperate anche fuori area durante la giornata, mantenendo FEED e gli altri servizi nella stessa missione. Le altre priorita della V39 restano operative.</p>
<p><strong>{chosen.upper()}, sei casi:</strong> cassa media {fmt(new['cash'])} contro {fmt(base['cash'])} V39, vittorie {new['wins']}/6 contro {base['wins']}/6. Perdite animali {new['animal_losses']} contro {base['animal_losses']}; perdite idriche {new['water_deaths']} contro {base['water_deaths']}. Coltivate mediane D25 {fmt(new['cultivated']['25'])} contro {fmt(base['cultivated']['25'])}; infestanti mediane D30 {fmt(new['weeds_D30'])} contro {fmt(base['weeds_D30'])}.</p>
<p>Le tabelle includono cassa avversaria, FEED, CARE, WATER, MOVE, PASS, portafoglio e semine per fase. Sei casi di sviluppo, tre semi nelle due posizioni: non sono una validazione indipendente. Il mercato condiviso modifica anche la cassa avversaria. Il Top e un corpus storico descrittivo; gli altri confronti locali usano gli stessi semi. Bande min-max osservate, non intervalli di confidenza.</p>
<p>Prefisso D1–D11 e topologia 7–7–0 verificati, simulazioni complete senza errori o missioni incomplete. D26–D30 eredita la chiusura precedente. Tempi locali con simulazioni concorrenti. Solo 770, nessuna submission. V33 resta riferimento, V29 pubblicata.</p>
<h2>Valutazione</h2><p>La protezione dei servizi non e sufficiente se peggiora produzione, acqua o cassa. Questa revisione resta un esperimento: esaminare le regressioni nelle tabelle prima di scegliere una sostituzione.</p>"""
''' +s[b:]
s=s.replace("('V38','V38 locale',aggregate(prof('v38')),'TOP770')","('V38','V38 locale',aggregate(prof('v38')),'TOP770'),('V39','V39 locale',aggregate(prof('v39')),'TOP770')")
s=s.replace("BASE/'tests/test_spent_renewal_v39.py'","BASE/'tests/test_spent_renewal_v39.py',BASE/'tests/test_protected_routes_v40.py'")
(p/'build_animal_service_770_report.py').write_text(s,encoding='utf-8')
