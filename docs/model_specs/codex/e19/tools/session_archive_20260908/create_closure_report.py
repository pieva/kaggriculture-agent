from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
s=(p/'build_water_route_770_report.py').read_text(encoding='utf-8')
s=s.replace('reports/water_route_770_20260908','reports/closure_bridge_770_20260908').replace("else 'v44'","else 'v45'")
s=s.replace("['v33','v38','v39','v41','v44']","['v33','v38','v39','v41','v44','v45']",1)
s=s.replace("['v41','v42','v43','v44']","['v41','v44','v45']")
s=s.replace('[(12,20),(21,25),(26,30)]','[(12,20),(21,25),(26,27),(26,30)]')
a=s.index('    base=summary');b=s.index('    template=',a)
s=s[:a]+'''    closing_versions=['v41','v44',chosen]
    closing_rows=[]
    for product in ['WHEAT','CARROT','STRAWBERRY','MILK','WOOL','FERTILIZER']:
        for metric in ['harvested','sold_units','sales_cash','realized_unit_price']:
            vals=[]
            for v in closing_versions:
                ps=prof(v)
                if metric=='realized_unit_price':
                    units=sum(d['sold_units'].get(product,0) for p in ps for d in p['ledger']['daily'][25:])
                    cash=sum(d['sales_cash'].get(product,0) for p in ps for d in p['ledger']['daily'][25:])
                    value=cash/units if units else 0
                else:value=mean(sum(d[metric].get(product,0) for d in p['ledger']['daily'][25:]) for p in ps)
                vals.append(fmt(value))
            closing_rows.append([product,metric,*vals])
    overview+='<h2>Raccolte e vendite D26–D30</h2><p>Quantita e ricavi medi per partita. Prezzo realizzato ponderato = ricavi / unita vendute; zero indica assenza di vendite. Le vendite possono includere scorte precedenti a D26.</p>'+table(['Prodotto','Misura',*closing_versions],closing_rows)
    overview+='<h2>Cassa ai checkpoint</h2>'+table(['Giorno',*closing_versions],[[d,*[fmt(mean(p['daily'][d-1]['money'] for p in prof(v))) for v in closing_versions]] for d in [20,25,27,30]])
    base=summary['v44']
    diagnosis=f"""<h2>Transizione alla chiusura: V45</h2>
<p>La V44 recupera superficie rispetto a V41, ma perde circa 2.190 di cassa media al checkpoint D25 e circa 6.980 al termine. Nei batch D26–D30 raccoglie 49,33 unita di latte contro 56,33 V41; vende 66,33 contro 69,33. Il prezzo realizzato cambia inoltre da circa 159,22 a 122,03: il mercato condiviso impedisce di attribuire l'intero divario alla sola gestione delle persone.</p>
<p>La V45 parte da V44 e prolunga il piano fino a D27 incluso. A D26, sulle caselle rinnovabili, ammette grano o carote soltanto se il ciclo completo termina entro D29, lasciando D30 per raccolta e vendita. A D27 nessuna nuova semina soddisfa questa riserva. D28–D30 riprende la chiusura precedente. Le scelte D1–D25 vengono verificate contro V44 nei ledger, nelle consistenze e nei KPI operativi; la modifica non riscrive la partenza.</p>
<p><strong>{chosen.upper()}, sei casi:</strong> cassa media {fmt(new['cash'])} contro {fmt(base['cash'])} V44; vittorie {new['wins']}/6 contro {base['wins']}/6; perdite idriche {new['water_deaths']} contro {base['water_deaths']}; perdite animali {new['animal_losses']} contro {base['animal_losses']}; infestanti mediane D30 {fmt(new['weeds_D30'])} contro {fmt(base['weeds_D30'])}.</p>
<p>Tre semi di sviluppo nelle due posizioni, non sei semi indipendenti. Top770-001 e un corpus storico descrittivo. Prefisso iniziale, topologia 7–7–0, completamento e sorgenti verificati; nessun errore o missione incompleta. Solo 770, nessuna nuova submission. V33 resta riferimento, V29 pubblicata.</p>
<h2>Valutazione</h2><p>Giudicare la transizione su servizi, raccolte, prezzi e cassa. Il piano prolunga una gestione esistente: non dimostra da solo che l'intero portafoglio finale sia ottimale.</p>"""
''' +s[b:]
s=s.replace("('V41','V41 locale',aggregate(prof('v41')),'TOP770')","('V41','V41 locale',aggregate(prof('v41')),'TOP770'),('V44','V44 locale',aggregate(prof('v44')),'TOP770')")
s=s.replace("BASE/'tests/test_provisional_queue_v44.py'","BASE/'tests/test_provisional_queue_v44.py',BASE/'tests/test_closure_bridge_v45.py'")
# The full action ledger and checkpoint state must remain unchanged to D25.
s=s.replace("    assert chosen in groups", """    assert chosen in groups
    for old,newrun in zip(groups['v44'],groups[chosen]):
        for key in ['daily','operational_daily']:
            assert old['sides']['candidate'][key][:25]==newrun['sides']['candidate'][key][:25],key
        assert old['sides']['candidate']['ledger']['daily'][:25]==newrun['sides']['candidate']['ledger']['daily'][:25],'D1-D25 ledger'
""")
(p/'build_closure_bridge_770_report.py').write_text(s,encoding='utf-8')
