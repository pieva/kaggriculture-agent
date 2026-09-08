"""One-time editorial migration. Preserve originals before updating reading paths."""
from pathlib import Path
import hashlib
import importlib.metadata
import json
import re
import shutil

ROOT=Path(__file__).resolve().parents[1]
F=ROOT/'docs/foundation'
ARCH=ROOT/'docs/governance/history/foundation_documentation_20260908'
if (ARCH/'manifest.json').exists():
    raise SystemExit('Migration already recorded; do not reapply over editorial changes.')
ARCH.mkdir(parents=True,exist_ok=True)
def write(p,s):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(s,encoding='utf-8')
records=[]
for p in F.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(F)
    dst=ARCH/rel
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(p,dst)
    records.append(dict(original=str(p.relative_to(ROOT)).replace('\\','/'),archive=str(dst.relative_to(ROOT)).replace('\\','/'),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
write(ARCH/'manifest.json',json.dumps(records,indent=2))
write(ARCH/'README.md','# Archivio della revisione documentale\n\nCopie byte per byte dei documenti prima della separazione fra descrizione, strategia e cronologia. Il manifest registra i percorsi originari e gli hash. Le indicazioni operative qui presenti sono storiche; per la lettura corrente usare [Foundation](../../../foundation/README.md).\n')

paths={
 'ontology':'ontology/ONTOLOGY_C2_1.md',
 'state':'state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md',
 'feature':'feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md',
}
introductions={
'ontology':'''# Ontologia — entità e concetti del gioco

L'ontologia dà un significato comune alle parole usate per descrivere la
fattoria. Distingue ciò che esiste, ciò che cambia nel tempo e ciò che viene
misurato. Consente a modelli diversi di parlare dello stesso fenomeno senza
confondere le regole del gioco con le proprie scelte strategiche.

## Come leggere il dominio

| Famiglia | Entità e concetti | Esempio di distinzione |
|---|---|---|
| Terreno | Fattoria, quadrante, casella, superficie disponibile e coltivata. | Terreno acquistato non equivale a terreno produttivo. |
| Produzione | Pianta, animale, struttura, ciclo biologico e prodotto. | Un pascolo vuoto è una struttura, non un animale produttivo. |
| Lavoro | Persona, posizione, azione, tempo disponibile e lavoro necessario. | Avere persone disponibili non garantisce che un servizio sia completabile. |
| Logistica | Semi, inventario personale, deposito e capacità. | Un prodotto raccolto non è ancora una vendita. |
| Economia | Cassa, costo, ricavo, mercato e risultato finale. | La cassa osservata è un dato; la riserva desiderata è una scelta del modello. |
| Tempo e controllo | Evento, scadenza, condizione di legalità e risultato di esecuzione. | Un comando richiesto può non produrre una transizione. |

Le proprietà osservate, le grandezze derivate, le previsioni del modello e i
risultati misurati a posteriori restano distinti. Il catalogo seguente conserva
i nomi tecnici dei concetti per collegare descrizione, feature e codice.

Per le regole operative leggere il [contratto dell'engine](../ENGINE_CONTRACT.md);
per le transizioni la [macchina a stati](../state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md);
per formule e osservabilità il [Feature Model](../feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md).

''',
'state':'''# Macchina a stati — come evolve la fattoria

La macchina a stati descrive come un'azione o il passare del tempo modifica
la partita. Per ogni transizione identifica lo stato iniziale, le condizioni
necessarie e il risultato. Il piano dell'agente sceglie le azioni; l'engine
decide quali effetti producono.

## Le trasformazioni principali

| Sistema | Evoluzione | Evento determinante |
|---|---|---|
| Coltura | Casella vuota → pianta in crescita → raccolta disponibile → terreno libero o nuova produzione. | Semina, età biologica e HARVEST. |
| Fine ciclo | Pianta esaurita → perdita della resa residua → infestante. | Decadimento dopo la fine della vita produttiva. |
| Carenza idrica | Pianta → infestante. | Raggiungimento della soglia di giorni senza acqua al refresh. |
| Animale | Struttura vuota → animale presente → prodotto disponibile. | Collocazione e calendario di produzione. |
| Carenza alimentare | Struttura con animale → struttura vuota. | Fuga al raggiungimento della soglia senza alimentazione. |
| Lavoro | Assunzione → persona disponibile → fine del contratto giornaliero. | HIRE e cambio di giornata. |
| Prodotto | Casella → inventario della persona → deposito → denaro. | Raccolta, trasferimento e vendita. |

Le transizioni avvengono in un ordine preciso. Le azioni delle persone
precedono il mercato; decadimento e refresh vengono dopo. Lo stato mostrato
prima di un turno non è il risultato delle azioni che verranno eseguite in
quel turno. Le sezioni seguenti definiscono guardie, clock e ordine degli eventi.

Il [contratto dell'engine](../ENGINE_CONTRACT.md) introduce il funzionamento
generale; l'[ontologia](../ontology/ONTOLOGY_C2_1.md) definisce i concetti usati qui.

''',
'feature':'''# Feature Model — informazioni disponibili per decidere

Il Feature Model descrive come trasformare lo stato del gioco in informazioni
utilizzabili da una policy. Per ogni informazione stabilisce significato,
fonte, formula, unità di misura e momento in cui è disponibile. Non assegna
priorità alle azioni e non sceglie la strategia.

## Dallo stato alle misure

| Informazione | Come si ottiene | Uso e limite |
|---|---|---|
| Cassa, posizione, oggetti presenti | Lettura dell'osservazione corrente. | Descrivono la situazione al momento della decisione. |
| Età di una pianta, distanza, capacità residua del deposito | Calcolo sui campi osservati e sulle regole. | Richiedono formule e unità esplicite. |
| Lavoro previsto e prenotazioni di persone | Calcolo del planner del singolo modello. | Sono previsioni o decisioni di policy, non fatti garantiti dall'engine. |
| Servizi riusciti, perdite, ricavi realizzati | Confronto degli stati prima e dopo l'esecuzione. | Misurano ciò che è avvenuto; non anticipano l'esito di un'azione futura. |

Per esempio, il numero di WATER riusciti non misura da solo la copertura
idrica: deve essere confrontato con le piante che richiedevano acqua nella
stessa finestra temporale. Analogamente, PASS misura un comando di attesa;
per stabilire se fosse evitabile servono stato, lavori disponibili e vincoli.

## Completezza e uso nel codice

Una feature utilizzabile richiede formula, denominatore quando applicabile,
finestra temporale e provenienza. Se uno di questi elementi non è definito,
il limite deve essere dichiarato: un nome plausibile non basta a rendere
una misura operativa.

La MODEL_SPEC indica quali feature usa e quali file le calcolano e le
consumano. La sola dichiarazione di utilizzo non dimostra che influenzino
le decisioni: la verifica richiede un collegamento al percorso eseguito nel codice.

L'[ontologia](../ontology/ONTOLOGY_C2_1.md) definisce i concetti; la
[macchina a stati](../state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md) definisce
gli eventi da cui derivano. Il catalogo tecnico seguente è il riferimento
per implementare misure coerenti fra modelli e report.

'''
}

def cut(s,start,end):
    a=s.index(start); b=s.index(end,a)
    return s[:a]+s[b:]
for kind,rel in paths.items():
    p=F/rel
    s=p.read_text(encoding='utf-8')
    # Replace audit metadata and status introduction with descriptive reading guide.
    if kind=='ontology':
        s=s[s.index('### 1.1 Separazione'):s.index('## 9. Delta')]
        s=cut(s,'## 7. Tracciabilità','## 8. Contratto')
    elif kind=='state':
        s=s[s.index('### 1.1 Separazione'):s.index('## 10. Audit')]
    else:
        s=s[s.index('### 1.1 Confine'):s.index('## 21. Delta')]
        s=cut(s,'## 19. Matrice di Copertura','## 20. Matrice di Mapping')
    s=re.sub(r'\s*\(CORR-\d+(?:,\s*CORR-\d+)*\)','',s)
    s=re.sub(r'\s*\(AGG-\d+\)','',s)
    # Versions remain in filenames for existing references, not in explanatory headings.
    lines=[]
    for line in s.splitlines():
        if line.startswith('#'):
            line=re.sub(r'\bC2(?:\.1)?\b','',line)
            line=line.replace('post-3Q','').replace('Frozen','').replace('Frozen','')
            line=re.sub(r'^(#{2,6})\s+\d+(?:\.\d+)*\.?\s+',r'\1 ',line)
            line=re.sub(' +',' ',line).rstrip()
        lines.append(line)
    s='\n'.join(lines)
    s=s.replace('Il registry canonico C2 consolida **85 concept_id**','Il catalogo definisce **85 concept_id**')
    s=s.replace('Parametri Biologici Frozen','Parametri biologici')
    s=s.replace('KAGGRICULTURE_FEATURE_MODEL_C2_1.md', 'KAGGRICULTURE_FEATURE_MODEL_C2_1.md')
    # Old path spellings inside prose become references to the current concepts.
    s=s.replace('Mapping concettuale verso ONTOLOGY_C2.md','Mapping concettuale verso l’ontologia')
    s=s.replace('dell’ambiente congelato','dell’ambiente di riferimento')
    write(p,introductions[kind]+s.rstrip('\n- ')+'\n\n## Fonti e documenti precedenti\n\nLe regole sono descritte nel [contratto dell’engine](../ENGINE_CONTRACT.md).\nLe versioni precedenti e i verbali sono [conservati nell’archivio](../../governance/history/foundation_documentation_20260908/README.md).\nI nomi tecnici e le formule del catalogo rimangono riferimenti di implementazione; questa revisione riorganizza la documentazione e non modifica il codice del gioco.\n')

# Keep the wide implementation table available, but separate it from the reading guide.
p=F/paths['feature']; s=p.read_text(encoding='utf-8')
a=s.index('| feature_id |'); b=s.index('\n---',a)
table=s[a:b]
write(F/'feature_model/FEATURE_CATALOG.md','# Catalogo tecnico delle feature\n\nTabella di consultazione per implementazione e audit. Per significato delle classi, esempi e criteri d’uso leggere il [Feature Model](KAGGRICULTURE_FEATURE_MODEL_C2_1.md). Identificatori, formule e campi sono mantenuti dal catalogo precedente.\n\n'+table.strip()+'\n')
s=s[:a]+'La [tabella completa delle feature](FEATURE_CATALOG.md) raccoglie identificatori, campi sorgente, formule, unità, condizioni di validità e limiti di osservabilità. È separata da questa spiegazione perché serve come riferimento di implementazione.\n'+s[b:]
write(p,s)

# Move model-local planning out of the shared domain description, retaining a compatibility link.
old=F/'V48_PLANNING_AND_BUILD_IT.md'
target=ROOT/'docs/model_specs/codex/e19/design/V48_PLANNING_AND_BUILD_IT.md'
text=old.read_text(encoding='utf-8')
write(target,text)
write(old,'# Pianificazione Codex 770\n\nIl piano è un documento del modello Codex, separato dalla Foundation condivisa.\n\nLeggere [pianificazione, produzione e verifiche della V48](../model_specs/codex/e19/design/V48_PLANNING_AND_BUILD_IT.md) e la [specifica della strategia](../model_specs/codex/e19/MODEL_SPEC_CODEX_770_V48.md).\n')

write(F/'README.md','''# Foundation — descrizione condivisa di Kaggriculture

La Foundation spiega il mondo in cui operano le policy. I documenti si leggono
in questo ordine e hanno responsabilità distinte:

| Documento | Cosa descrive |
|---|---|
| [Contratto dell’engine](ENGINE_CONTRACT.md) | Come si svolge la partita e quali regole applica il simulatore. |
| [Ontologia](ontology/ONTOLOGY_C2_1.md) | Entità, proprietà e significato dei concetti del gioco. |
| [Macchina a stati](state_machine/KAGGRICULTURE_STATE_MACHINE_C2_1.md) | Transizioni, condizioni e ordine degli eventi. |
| [Feature Model](feature_model/KAGGRICULTURE_FEATURE_MODEL_C2_1.md) | Informazioni osservabili o calcolabili e limiti del loro utilizzo. |
| [Catalogo tecnico delle feature](feature_model/FEATURE_CATALOG.md) | Identificatori e formule per implementazione e audit. |

Le strategie, la pianificazione e la mappa dei sorgenti delle policy sono
nelle [MODEL_SPEC](../model_specs/README.md). Stato del lavoro e risultati
sono nel [Project State](../PROJECT_STATE.md) e nei report degli esperimenti.

Il [manifest](FOUNDATION_C2_1_MANIFEST.md) identifica i documenti correnti e
le fonti. I nomi dei file esistenti sono mantenuti per compatibilità dei link.
Le copie C1/C2 e i materiali in `evidence/` sono storici o di provenienza,
non descrizioni correnti né istruzioni operative. Le copie precedenti a
questa revisione sono anche disponibili nell’[archivio documentale](../governance/history/foundation_documentation_20260908/README.md).
''')

engine=ROOT/'.venv/Lib/site-packages/kaggle_environments/envs/kaggriculture'
source_manifest=dict(package='kaggle-environments',version=importlib.metadata.version('kaggle-environments'),scope='Local installed engine, not a verification of current Kaggle server',files={n:hashlib.sha256((engine/n).read_bytes()).hexdigest() for n in ['kaggriculture.py','kaggriculture.json','README.md']})
write(F/'ENGINE_SOURCE_MANIFEST.json',json.dumps(source_manifest,indent=2))
hashpaths=['ENGINE_CONTRACT.md',*paths.values(),'feature_model/FEATURE_CATALOG.md']
rows='\n'.join('| '+p+' | `'+p+'` | `'+hashlib.sha256((F/p).read_bytes()).hexdigest().upper()+'` |' for p in hashpaths)
write(F/'FOUNDATION_C2_1_MANIFEST.md','''# Manifest della Foundation

Questo indice identifica le descrizioni correnti del dominio e ne registra
gli hash per verificarne l’integrità. Non contiene il piano di sviluppo delle policy.
La [guida di lettura](README.md) spiega il ruolo di ciascun documento.

## Documenti correnti

| Documento | File | SHA-256 |
|---|---|---|
'''+rows+'''

## Fonti e confini

Le fonti effettivamente lette per l’engine sono identificate in
[ENGINE_SOURCE_MANIFEST.json](ENGINE_SOURCE_MANIFEST.json). Il contratto
osservativo del progetto è in [observation_contract.py](../../src/agricola/core/observation_contract.py).
Quest’ultimo normalizza osservazioni, clock e snapshot; non definisce una strategia.

I modelli condividono concetti, regole e definizioni delle misure. Planner,
priorità e routine appartengono alle MODEL_SPEC. La revisione editoriale
non modifica engine o policy e non costituisce una nuova certificazione incrociata.

## Archivio e provenienza

- [Copie precedenti e manifest dei loro hash](../governance/history/foundation_documentation_20260908/README.md).
- [Verbale storico di riconciliazione dell’engine](../governance/history/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md).
- [Inventario degli artefatti conservati localmente](evidence/LOCAL_ARTIFACTS_20260908.json).

Le vecchie copie C1/C2 e le evidenze di ambiente sono conservate per audit;
non sostituiscono i documenti correnti elencati sopra.
''')

# Point the project introduction to the description, not the historical verdict.
p=ROOT/'README.md';s=p.read_text(encoding='utf-8')
s=s.replace('docs/governance/history/model_spec_c2/foundation_revision/ANTIGRAVITY_C2_FINAL_ENGINE_CONTRACT_RECONCILIATION.md','docs/foundation/ENGINE_CONTRACT.md')
write(p,s)
print('Archived',len(records),'files; revised shared descriptions and manifest; moved V48 plan.')
