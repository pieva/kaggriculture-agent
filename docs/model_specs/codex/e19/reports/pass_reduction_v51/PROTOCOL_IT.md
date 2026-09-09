# V51 — percorsi impegnati al giorno 29

Baseline congelata V49F. Prima modifica: costruire missioni complete FEED, CARE,
WATER, HARVEST con prelievi esatti, risorse condivise riservate, costo delle
mosse e rientro richiesto inclusi. Le missioni sono inserite direttamente nel
controllore e confermate dal suo normale riscontro sull'osservazione.
Le destinazioni ancora impegnate non sono offerte a un altro lavoratore.
Nessuna assunzione aggiuntiva se tutte le obbligazioni osservate sono impegnate.

Primo screening: seed 180903003 posto 0; poi 180903001/2 posto 0.
Solo se tutti i gate aggregati passano, estensione ai tre posti 1, e infine
seed nuovi 260909201/202 entrambi i posti. Nessun uso anticipato di questi seed.
Gate invariati V50: PASS assoluti e quota inferiori, MOVE non superiori,
cash medio non inferiore e nessun caso sotto il 98% della baseline, nessun
peggioramento dei servizi e deficit biologici. Runtime diagnostico 120 secondi;
eventuale candidato richiede poi confezionamento, parità e runtime standard.
Nessuna submission esterna prevista.

## Revisioni osservate nello sviluppo

- A: percorsi impegnati, ma la deduplicazione conserva il ripiego HARVEST
  quando segue WATER/HARVEST. Tre casi: cash medio −822, PASS −49,
  MOVE −54,33. Respinta per regressione economica.
- B: conserva la visita con più comandi necessari per ciascuna destinazione.
  Nel primo caso recupera il cash, ma la logica ereditata assume ancora sei
  lavoratori per tre visite residue: screening dei tre seed già esposti.
- C: limita quelle assunzioni al minimo che contiene le visite residue usando
  lo stesso compilatore di percorsi. Considera gli spawn effettivi, il turno
  necessario per osservare l'assunzione, le scorte dopo gli impegni e le vendite;
  non anticipa l'effetto di acquisti. I lavoratori già impegnati non sono
  considerati capacità libera per questa decisione.

Le revisioni restano in file distinti; i risultati di A e B non vengono riscritti.

V51C supera i tre casi iniziali: delta medi cash +345, PASS −53, MOVE −34,33;
FEED/CARE/WATER invariati, HARVEST +0,33, nessun peggioramento nei deficit
misurati. Il bundle è fissato prima di aprire i seed nuovi, SHA256:
`43d5c6c3b70cf2940afaa83f3a243cba75e52f89db459d31ecb96187c4f13fda`.
La matrice del secondo posto resta necessaria prima della validazione.

La matrice completa dei sei casi è passata, mantenendo le stesse medie.
Il 2026-09-09 alle 13:45:22 UTC sono stati aperti i due seed nuovi, entrambi
i posti, con V49F abbinata. Vedere `validation_opened.json`: da questo momento
i seed sono esposti e non devono essere riutilizzati come nuovi holdout.

Validazione completata senza modifiche al candidato: quattro casi, tutti i
gate aggregati passati. Cash medio +64,50, PASS −45,50, MOVE −61;
FEED/CARE/WATER/HARVEST e deficit biologici invariati. Seed 260909201:
cash −164, PASS +15, MOVE −97; seed 260909202: cash +293, PASS −106,
MOVE −25. I due posti danno gli stessi delta e non sono repliche indipendenti.
