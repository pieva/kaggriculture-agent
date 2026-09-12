"""Add the verified interpretation and artifact validation to the report."""
import hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parent
OUT=BASE/'reports/trajectory_774_772_775'
SUMMARY='''<section id="interpretazione"><h2>A chi assomiglia?</h2>
<p><strong>D1–D11: Q0 coincide con la 775; Q1 coincide con entrambe.</strong> La piccola differenza rispetto alla 772 in Q0 riguarda il pollaio vuoto e i PASS a D11. L’apertura E18 è conservata per costruzione: questa coincidenza iniziale non è una scoperta di superiorità biologica. La prima azione diversa dalla E18 è D12 H2; rispetto alla E20.2 è D11 H15.</p>
<p><strong>D12–D19: la 774 rimane complessivamente più vicina alla 775 in entrambi i quadranti.</strong> Distanze normalizzate Q0: 0,126 dalla 775 contro 0,430 dalla 772; Q1: 0,245 contro 0,389. Non tutti i KPI sono più vicini singolarmente; le distanze per indicatore sono nel JSON.</p>
<h2>Una pecora esclusa dalla casella, poi ricollocata</h2>
<p>In tutti i 14 replay E18 verificati la casella (x=4,y=7) ospita una pecora. Nel caso usato per i grafici, lo stato mostra il pascolo a D12 H10 e la pecora a D12 H18; sono gli orari dello stato successivo all’azione. Nella ricostruzione la casella diventa grano.</p>
<p><strong>Gli animali totali non rimangono uno in meno.</strong> A D12: 774 = 8 mucche + 9 pecore + 1 oca (18); 775 = 8 + 10 + 1 (19). A D13 la ricostruzione colloca una pecora nel pascolo prima vuoto (6,3), osservata a H6, e torna a 19 animali, con tutti i 18 pascoli occupati. E18 mantiene 19 animali e un pascolo vuoto. Gli acquisti totali restano 8 mucche, 11 pecore e un’oca in entrambe. Quindi questo esperimento modifica spazio e distribuzione, non realizza ancora la riduzione coerente di un animale prevista per una futura E21.</p>
<h2>Cosa è stato effettivamente ricostruito</h2>
<p>Prima run: sola riattivazione del ramo superstite e correzione tecnica del confronto con una casella di tipo dizionario. Il reclaim non si attiva; il controller resta in RECOVERY, chiude 775, zero rollback. Seconda run: attivazione fissa a D12, target (4,7), filtri persistenti senza rollback anche al terminale e routing ereditato dal meccanismo E20v39, ridotto a una casella. Apertura E18 e pollaio conservati; cap aggregato COW/SHEEP 18 prima di Q2 e 19 dopo, senza tagliare gli acquisti residui. Non è l’eseguibile storico 774 né la nuova E21 con missioni biologiche complete.</p>
<p><a href="../../RECONSTRUCTION_PROTOCOL.json">Protocollo prima run</a> · <a href="../../FIXED774_PROTOCOL.json">Protocollo 774 persistente</a> · <a href="MANIFEST.json">Hash e verifiche</a></p></section>'''
def main():
    p=OUT/'REPORT.html';h=p.read_text(encoding='utf-8')
    h=h.replace('Il semplice ramo superstite riattivato torna alla 775; è conservato separatamente.','Nel ramo superstite riattivato il reclaim non si attiva: resta in RECOVERY e chiude 775, con zero rollback. La prima run è conservata separatamente.')
    h=h.replace('prima riattivazione con rollback conservato','prima riattivazione con rollback conservato ma mai attivato')
    if 'id="interpretazione"' not in h:h=h.replace('<table>',SUMMARY+'<table>',1)
    p.write_text(h,encoding='utf-8')
    p=OUT/'REPORT.md';md=p.read_text(encoding='utf-8')
    md=md.replace('Il semplice ramo superstite riattivato torna alla 775; è conservato separatamente.','Il ramo superstite non attiva il reclaim: resta in RECOVERY e chiude 775, zero rollback.')
    md='\n'.join(line for line in md.splitlines() if not line.startswith('Target (x=4,y=7):'))
    if '## Interpretazione verificata' not in md:
        md+='\n\n## Interpretazione verificata\n\nD1–D11: Q0 identica alla 775; Q1 identica a entrambe. D12–D19: complessivamente più vicina alla 775 in entrambi i quadranti. L’apertura coincide per costruzione, non è prova di superiorità.\n\nIl target ospita una pecora in 14/14 replay. La 774 ha 18 animali a D12, poi 19 da D13 dopo la collocazione di una pecora nel pascolo prima vuoto (6,3). Acquisti invariati rispetto a E18: 8 mucche, 11 pecore, 1 oca. Non è una riduzione persistente degli animali.\n\nPrima run: reclaim mai attivato, RECOVERY e zero rollback, finale 775. Seconda: envelope persistente D12 con routing ereditato E20v39 ridotto a un target, senza rollback né bypass terminale, cap 18/19. È una ricostruzione moderna, non la variante storica esatta e non E21 biologica.\n'
    p.write_text(md+'\n',encoding='utf-8')
    manifest=json.loads((OUT/'MANIFEST.json').read_text())
    manifest['interpretation']='774 fills formerly empty pasture by D13; animal count reduction is transient'
    manifest['visual_qa']='PNG figures inspected; legend moved into unused panel to avoid axis overlap'
    manifest['outputs']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.name!='MANIFEST.json'}
    manifest['sources'][str(Path(__file__).relative_to(BASE.parents[3]))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
