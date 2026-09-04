"""
Generate EVIDENCE_MATRIX.csv and detailed data structures for report.
"""

import csv
from pathlib import Path

OUT_DIR = Path("results/e13/episode_101971376/antigravity")

evidence_matrix = [
    {
        "claim": "Harith vince semplicemente perche compra Q2",
        "classification": "CONTRADICTED",
        "evidence": "Pietro ha sbloccato Q2 a Day 17 (3 quadranti posseduti per 13 giorni, reward $7,123 vs Harith $133,049). Entrambi possedevano 75 tile.",
        "counterevidence": "Harith ha sbloccato Q2 prima (Day 12 vs Day 17), ma il possesso di Q2 senza crop throughput non ha salvato Pietro dal collasso a $7.1k.",
        "confidence": "HIGH",
        "observability": "OBSERVED"
    },
    {
        "claim": "Harith vince semplicemente perche ha piu Hands",
        "classification": "CONTRADICTED",
        "evidence": "Pietro ha eseguito 292 HIRE totali vs Harith 291 HIRE totali. Entrambi hanno mantenuto 12 Hands attive nel mid-late game.",
        "counterevidence": "Harith ha assunto prima a Day 1 (8 Hands vs 5 Hands), ma la quantita totale di ore lavoro acquistata e equivalente.",
        "confidence": "HIGH",
        "observability": "OBSERVED"
    },
    {
        "claim": "Harith vince semplicemente perche ha piu livestock",
        "classification": "CONTRADICTED",
        "evidence": "Pietro possedeva 18 animali in campo a fine partita (14 Cow + 4 Sheep) vs Harith 15 animali (8 Cow + 7 Sheep).",
        "counterevidence": "Harith ha orientato il herd verso Sheep (Wool $200/unit, 162 venduti = $38.0k) e ha alimentato gli animali con surplus interno invece di comprare a mercato.",
        "confidence": "HIGH",
        "observability": "OBSERVED"
    },
    {
        "claim": "Harith vince perche mantiene il campo piu pulito",
        "classification": "NOT_SUPPORTED",
        "evidence": "Pietro ha totalizzato solo 91 DIG e poche erbacce nel late game perche non coltivava crop tiles (campo vuoto).",
        "counterevidence": "La pulizia del campo e una condizione necessaria ma non sufficiente; la generazione di cassa deriva dalle colture irrigate e raccolte.",
        "confidence": "HIGH",
        "observability": "OBSERVED"
    },
    {
        "claim": "Harith vince perche usa piu superficie",
        "classification": "SUPPORTED",
        "evidence": "Harith ha mantenuto 48-59 crop tiles attive + 15-16 pasture tiles (65-74 productive tiles su 75). Pietro ha saturato solo 18 pasture tiles con 0-9 crop tiles (max 27 productive tiles su 75).",
        "counterevidence": "La superficie posseduta era identica (75 tile), ma la superficie effettivamente coltivata e produttiva differiva di 2.7x.",
        "confidence": "HIGH",
        "observability": "OBSERVED"
    },
    {
        "claim": "Harith vince soprattutto per crop revenue",
        "classification": "SUPPORTED",
        "evidence": "Harith ha generato $89,446 di crop revenue ($56.3k Strawberry + $20.2k Melon + $12.9k Wheat), pari al 52.0% del suo fatturato totale ($171.9k). Pietro ha generato $0 Strawberry e $0 Melon.",
        "counterevidence": "Anche il livestock product revenue ($65.4k) e il fertilizer ($17.0k) hanno contribuito in modo sostanziale.",
        "confidence": "HIGH",
        "observability": "OBSERVED"
    },
    {
        "claim": "Harith vince soprattutto per livestock-product revenue",
        "classification": "PARTIALLY_SUPPORTED",
        "evidence": "Harith ha realizzato $65,441 da Milk e Wool (vs Pietro $43,933, delta +$21,508).",
        "counterevidence": "Il crop revenue ($89,446) ha superato il livestock revenue ($65,441) e il delta crop (+$51,346) spiega piu del doppio del delta livestock.",
        "confidence": "HIGH",
        "observability": "OBSERVED"
    },
    {
        "claim": "Il gap nasce principalmente nel late game",
        "classification": "CONTRADICTED",
        "evidence": "La divergenza materiale si apre a Day 1 Turn 6: Harith irriga 17 colture e imposta il compounding; Pietro esegue 0 WATER e va in loop HARVEST su tile vuote. A Day 13 Harith e a $10.8k vs Pietro a $935.",
        "counterevidence": "La forbice monetaria assoluta si allarga esponenzialmente negli ultimi 10 giorni ($43k vs $0.5k a Day 20), ma e il risultato del compounding avviato a Day 1.",
        "confidence": "HIGH",
        "observability": "OBSERVED"
    },
    {
        "claim": "Le due architetture sono realmente simili economicamente, non solo visivamente",
        "classification": "CONTRADICTED",
        "evidence": "Visivamente entrambe sbloccano Q1/Q2 e comprano animali. Economicamente, Pietro e un consumer netto di grano ($42.5k spesa feed vs $38.1k vendita grano = -$4.4k net) e genera $0 da cash crops, mentre Harith e un motore duale autosufficiente.",
        "counterevidence": "Entrambi usano 12 Hands e layout a 3 quadranti con pascoli centrali.",
        "confidence": "HIGH",
        "observability": "OBSERVED"
    }
]

with open(OUT_DIR / "EVIDENCE_MATRIX.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["claim", "classification", "evidence", "counterevidence", "confidence", "observability"])
    writer.writeheader()
    writer.writerows(evidence_matrix)

print("EVIDENCE_MATRIX.csv created successfully.")
