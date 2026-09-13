"""Append audited feed findings to the trigger dossier and HTML generator output."""
import json,html
from pathlib import Path
from docs.model_specs.codex.e22.tools import report_trigger_pilot as base

OUT=base.OUT
def main():
    data=json.loads((OUT/'FEED_SUMMARY.json').read_text(encoding='utf-8'))
    headers=['Modello','Replay','Raccolto','Comprato','Venduto','FEED','Spesa acquisti']
    rows=[]
    for m in data['models']:
        v=m['mean'];rows.append([m['name'],str(m['n']),*[f'{v[k]:.1f}' for k in ['harvested','bought','sold','fed','purchase_cash']]])
    intro='Bilancio fisico del grano e cassa verificati in 28/30 replay del pilota. Medie per partita; la spesa indica monete effettivamente pagate, non risparmi stimati.'
    conclusion='Tutti i sei modelli producono, in media, più grano dei FEED, ma comprano e vendono quantità rilevanti. Questo non dimostra sprechi: prezzi, liquidità e disponibilità temporale possono giustificare gli scambi. La priorità è verificare la scorta prima dei servizi animali, confrontando trattenimento, vendita e riacquisto nello stesso intervallo. Le quantità non identificano univocamente la provenienza delle razioni.'
    limitations='Esclusi soltanto da questa tabella Majkel1337/108488494 (discrepanza inventario di 2 unità al passo 690) e THIRD FARM CLUB/108500556 (residuo fisico di 14 unità). Le discrepanze della ricostruzione restano aperte; non sono perdite attribuite agli agenti. I confronti economici fra modelli sono descrittivi e non accoppiati.'
    md='\n## Audit del grano: primi risultati\n\n'+intro+'\n\n|'+'|'.join(headers)+'|\n|'+'|'.join(['---']*len(headers))+'|\n'+'\n'.join('|'+'|'.join(r)+'|' for r in rows)+'\n\n'+conclusion+'\n\n'+limitations+'\n\nDati: [FEED_SUMMARY.json](FEED_SUMMARY.json), dettagli giornalieri in `feed_profiles/`. Nessun risparmio netto ancora stimato: serve un controfattuale che includa mercato, terreno, lavoro, semi e ricavi rinunciati.\n'
    path=OUT/'REPORT.md';text=path.read_text(encoding='utf-8').replace('## Priorità consigliata per la prossima analisi\n\n','').split('\n## Audit del grano: primi risultati')[0];path.write_text(text+md,encoding='utf-8')
    base.main()
    section='<section><h2>Diversificazione preventiva e autoconsumo</h2><p>Alla semina il prezzo futuro è incerto. Confrontare un portafoglio concentrato, uno diversificato preventivamente e uno diversificato con aggiustamenti osservati. Valutare anche le date di raccolta, la produzione avversaria e i picchi di lavoro.</p><p>FEED consuma un grano per animale. Il grano trattenuto può evitare acquisti, ma rinuncia a una vendita; coltivarlo occupa terreno e lavoro e richiede semi e servizi. Includere anche il fertilizzante animale destinato alle colture, senza doppio conteggio.</p><h3>Grano: produzione, mercato e nutrimento</h3><p>'+intro+'</p><div class="overflow"><table><tr>'+''.join('<th>'+h+'</th>' for h in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(c)+'</td>' for c in r)+'</tr>' for r in rows)+'</table></div><p>'+conclusion+'</p><p class="muted">'+limitations+'</p><p><a href="FEED_SUMMARY.json">Bilancio e limiti</a> · Nessun risparmio netto ancora stimato.</p></section>'
    groups='''<section><h2>Tre categorie di competitor</h2><table><tr><th>Categoria</th><th>Competitor</th><th>Distinzione</th></tr><tr><td>1. Configurazione quasi invariata</td><td>s56165462</td><td>Geometria, mix e colture identici nei 30 snapshot dei tre replay.</td></tr><tr><td>2. Mix variabile su geometria stabile</td><td>Denis Revenko, Sam-wiz, kiki yi2</td><td>Area sostanzialmente stabile; possono cambiare specie e tipo di struttura. Kiki conserva le stesse 17 coordinate animali a D20 nei cinque replay.</td></tr><tr><td>3. Variazione anche della dimensione o disposizione produttiva</td><td>spbforce, Rheinmetall, Majkel1337, Mengfei Li, THIRD FARM CLUB</td><td>Cambiano superfici, quantità o posizioni produttive; spbforce passa da 17 a 23 strutture animali a D20.</td></tr></table><p>Olympus: vicino alla categoria 2, provvisorio per replay deteriorati. EnricRovira: categoria 3 negli stati osservati, ma parte della variabilità comprende perdite animali. Le categorie non misurano efficacia o complessità del codice.</p><p><a href="COMPETITOR_GROUPS.md">Criteri, evidenze e casi provvisori</a></p></section>'''
    path=OUT/'REPORT.html';path.write_text(path.read_text(encoding='utf-8').replace('<section><h2>Esplora',groups+section+'\n<section><h2>Esplora'),encoding='utf-8')

if __name__=='__main__':main()
