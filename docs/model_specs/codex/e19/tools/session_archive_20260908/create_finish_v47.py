from pathlib import Path
s=Path('scratch/finish_v46.py').read_text(encoding='utf-8')
s=s.replace('final_services_770_20260908','final_water_770_20260908').replace('v46_TOP770','v47_TOP770')
s=s.replace("['v41','v45','v46']","['v41','v45','v46','v47']")
s=s.replace('# V46: servizi pianificati fino a D29', '# V47: servizi finali e protezione idrica D28–D29')
s=s.replace('Solo 770. V46 deriva da V45:', 'Solo 770. V47 deriva da V46 e aggiunge protezione WATER per piante gia stressate a D28–D29 (priorita 8 e recupero fuori area), escludendo PLANT/DIG. V46 aveva aggiunto 12 perdite idriche finali (10 carote, 2 fragole) rispetto a V45. V46 deriva da V45:')
s=s.replace('Quattro test mirati passati su CARE utile/non utile, FEED D29 e delega terminale D30.', 'Sette test mirati passati: quattro V46 su CARE/FEED/terminale, tre V47 su finestre temporali, esclusione nuove semine e ordine protetto dei percorsi.')
Path('scratch/finish_v47.py').write_text(s,encoding='utf-8')
