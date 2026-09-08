from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools/build_water_route_770_report.py')
s=p.read_text(encoding='utf-8')
s=s.replace("else 'v43'","else 'v44'").replace("['v33','v38','v39','v41','v43']","['v33','v38','v39','v41','v44']").replace("['v41','v42','v43']","['v41','v42','v43','v44']")
s=s.replace("<p><strong>{chosen.upper()}, sei casi:","<p>La V43 e anch'essa una prova su un caso, non una versione promossa. La V44 torna alla V41 e corregge la coda: un servizio esistente puo essere candidato oltre una semina o un rinnovo non ancora ammesso. L'ordine fra servizi esistenti e la precedenza delle missioni ammissibili restano invariati. Non modifica le priorita, il recupero fuori area o il calendario idrico della V41. Il filtro e temporaneo durante la preparazione dell'alternativa, non cancella il rinnovo dal piano.</p><p><strong>{chosen.upper()}, sei casi:")
s=s.replace("BASE/'tests/test_water_route_rescue_v43.py'","BASE/'tests/test_water_route_rescue_v43.py',BASE/'tests/test_provisional_queue_v44.py'")
p.write_text(s,encoding='utf-8')
