# V50 — protocollo prima dei nuovi confronti

Baseline locale: V49F, hash eabe7bc782fcffab354ffbe9f454bdc1a1b5d37419e30b957c5d260193c96f31.
V48 pubblicata e tutti gli artefatti V49 rimangono invariati. Nessuna submission.

Diagnosi: replay esposto 106843637, parità 719/719 anche dopo le sonde offline.
Le sonde rimuovono soltanto il filtro di percorso per servizi non già assegnati:
fattibilità non implica redditività né una riduzione globale dei movimenti.
D12/13/14/15/29: rispettivamente 8/8/6/11/10 slot PASS con almeno una visita
fattibile. Il campione non dimostra che tutti i PASS con prenotazioni siano evitabili.

Prima ipotesi V50A: sostituire la riduzione arbitraria dell'organico D29 con
un limite basato sul packing completo dei servizi osservati, includendo viaggio,
input, missione attiva, disponibilità dei nuovi manovali dal tick successivo
e rientro. Conservare le altre decisioni di mercato. Il packing certifica un
piano possibile, non che il dispatcher successivo lo esegua: verificare in replay.

Sviluppo: 180903001–180903003, due posti, V4D esposto. Anche 260909101/102 sono
ormai esposti; non usarli come holdout. Nuova partizione preregistrata:
260909201 e 260909202, entrambi i posti, da aprire solo dopo freeze e gate di
sviluppo. Stesso controllo V4D, nessuna validazione esterna indipendente.

Gate invariati rispetto a V49: partite complete, zero errori/incompleti,
PASS assoluti e quota inferiori, MOVE medi non superiori, cassa media non
inferiore e nessun caso sotto -2%, nessun peggioramento di perdite produttive,
fughe o deficit osservati, FEED/CARE/HARVEST aggregati non inferiori.
Registrare ogni regressione individuale. Runtime standard in prova seriale
separata; non certificare Kaggle sulla base dei benchmark con timeout ampliato.

Evoluzione sul solo sviluppo, prima di aprire nuovi seed:

- Il primo avvio A è stato interrotto prima di ottenere risultati, per
  completare le guardie su rientro e scorte. Il run A verificato è conservato.
- A controlla solo H1; B tutte le assunzioni D29; C aggiunge il rientro durante
  l'inserimento; D vincola il packing anche alle scorte condivise. Nessuna di
  queste revisioni riduce effettivamente gli HIRE sullo screen 180903003/0.
- L'ispezione separa i rifiuti del certificato: i prelievi attivi impegnano tutto
  il grano, e un piano che assegna FEED ad altri lavoratori richiede scorte
  aggiuntive. Le sonde non vengono eseguite nel runtime della policy.
- E cambia il packing reale in D29 per rispettare scorte e inventari; F lo
  combina con D. Sullo screen: cassa +32, MOVE -2, PASS +3. Gate PASS fallito.
- G eredita la guardia di rientro della baseline (scarico notturno ammesso
  quando non occorre rientrare): ancora nessuna variazione degli HIRE.
- H usa come carico FEED/CARE/WATER/HARVEST osservati; esclude FERTILIZE e
  COLLECT_FERTILIZER facoltativi dal certificato, conservando integralmente
  le missioni già ammesse e il dispatcher. I applica anche la rimozione della
  raccolta del fertilizzante nei servizi reali: sullo screen perde 9 di cassa
  e aggiunge 30 PASS, quindi è respinta.
- H è estesa agli altri due seed di sviluppo, posto 0: cassa migliore e
  PASS inferiori, ma MOVE medi +1,33. Rimane fuori dal gate. J combina H ed E;
  K combina H, E e la rimozione della raccolta facoltativa.

Un certificato di packing è un piano possibile per il carico incluso, non
una prova che il dispatcher lo eseguirà. La guardia di rientro è una stima
osservata ereditata; non garantisce da sola la capacità del deposito per tutto
il resto della giornata. Sono i confronti eseguiti e gli audit biologici a
determinare l'accettazione, senza nascondere le regressioni individuali.

Chiusura dello sviluppo: 11 prototipi, 17 partite candidate. H, J e K sono
state estese ai tre seed, posto 0. H e J falliscono anche i gate servizi e
obblighi (due FEED in meno nel campione), oltre ai MOVE; K fallisce i MOVE.
J: delta medi cassa +143,33, PASS -52,33, MOVE +6,33. Nessuna promozione.
Non eseguiti i posti 1 né aperti i seed nuovi, perché il gate di sviluppo
fallisce già. V49F resta il riferimento; il bundle J è conservato per audit.
La prova runtime standard riguarda V49F e non rende accettata V50.

Runtime seriale V49F completato sul seed 180903001, posti 0 e 1: 719 azioni
in parità in entrambi, nessun errore o azione assente. actTimeout=1, overage
consumato 18,109 e 20,296 secondi su 60. La prova usa il punto d'ingresso del
bundle standalone. È verifica locale, non equivalenza dell'hardware Kaggle.
