# E18.28 C — diagnosi esterna dei PASS e delle sconfitte

Campione congelato il 2026-09-05: submission **56036993**, tutti i 30 episodi competitivi completati mostrati nella cronologia, fino a **105876558**; escluso il self-test. Nessuna selezione per rating, avversario o topologia. E18.29 B3 non è pubblicata: questi risultati descrivono il parent E18.28 C.

## Metodo e limiti

Per ogni replay: 720 stati DONE/DONE, episodio e SHA-256 verificati; 719 decisioni ricostruite dal controller E18.28 senza cambiare lo stato registrato e confrontate integralmente con le azioni pubblicate. Nessun disaccordo. Non sono nuove simulazioni né stime controfattuali del punteggio. Il motivo del PASS è il ramo effettivo del dispatcher, non una deduzione dal grafico.

Finestre assegnate al giorno pre-azione. PASS comprende ogni lavoratore già presente e ogni comando omesso; quota normalizzata sugli slot realmente disponibili. Un worker assunto nel batch non aggiunge retroattivamente uno slot. Gli avversari possono avere topologie/personale diversi: il confronto esterno è diagnostico, non una ablation causale.

I flussi monetari e WATER/FEED/CARE/HARVEST vengono verificati nel motore sui batch registrati. Eventuali episodi con mancata riconciliazione restano nel campione PASS/score, ma sono esclusi dalle medie dei flussi verificati e segnalati sotto. Non si imputano valori zero. I vecchi derivati nella directory senza suffisso v2 sono preliminari e non vanno usati: V2 corregge la normalizzazione NORTH/SOUTH/EAST/WEST e conserva anche le eccezioni di audit.

Nessuno dei 17 avversari vincitori ha esattamente la topologia finale Q0=7/Q1=7/Q2=0/Q3=0. Le cause del nostro dispatcher sono verificate sulla nostra 770; i divari di mix/ricavo avversario servono a formulare ipotesi, non a scegliere una topologia o quantificare guadagni ottenibili a parità di architettura.

## Risultati — vittorie come controllo

| Campione | N | Cassa nostra | Cassa avversaria | PASS nostri | Min–max PASS | PASS D15–D30 | % slot D15–D30 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ALL | 30 | 81,294.4 | 80,967.0 | 1,573.7 | 1552–1786 | 741.0 | 15.81% |
| LOSS | 17 | 82,076.1 | 96,951.4 | 1,578.9 | 1552–1786 | 746.3 | 15.92% |
| WIN | 13 | 80,272.2 | 60,064.3 | 1,566.9 | 1554–1606 | 734.0 | 15.66% |

## Motivi osservati nelle sconfitte

| Finestra | PASS nostri | Coda esaurita | Attesa orario | Prerequisito bloccato | PASS avversari | % slot nostri / avversari |
|---|---:|---:|---:|---:|---:|---:|
| D01_D06 | 270.8 | 253.9 | 12.2 | 4.7 | 280.8 | 34.37% / 33.57% |
| D07_D12 | 526.6 | 459.9 | 59.1 | 7.6 | 180.0 | 35.02% / 13.52% |
| D13_D15 | 50.7 | 44.2 | 6.4 | 0.1 | 37.3 | 8.13% / 4.57% |
| D15_D30 | 746.3 | 622.8 | 123.5 | 0.0 | 181.2 | 15.92% / 4.05% |
| D16_D24 | 527.0 | 439.5 | 87.5 | 0.0 | 60.7 | 19.65% / 2.35% |
| D25_D30 | 203.8 | 170.3 | 33.5 | 0.0 | 105.8 | 11.48% / 6.55% |

Coda esaurita non significa che tutta la farm non abbia lavoro: significa che la coda assegnata a quel worker non contiene più task produttivi. Attesa orario può essere intenzionale. Un blocco di prerequisito conta i PASS immediati, non tutti gli effetti futuri di un acquisto mancato.

## Servizio, produzione e ricavi nelle sconfitte

Flussi verificati: 17/17 sconfitte.

| KPI medio | E18.28 C | Avversari vincitori |
|---|---:|---:|
| executed_actions:CARE | 249.35 | 263.35 |
| executed_actions:FEED | 323.12 | 288.35 |
| executed_actions:WATER | 1,144.35 | 855.76 |
| executed_actions:FERTILIZE | 31.29 | 79.29 |
| executed_actions:HARVEST | 341.24 | 295.76 |
| harvested:MILK | 197.88 | 186.94 |
| harvested:WOOL | 93.18 | 132.24 |
| harvested:STRAWBERRY | 141.53 | 233.35 |
| harvested:WHEAT | 503.88 | 187.00 |
| harvested:CARROT | 83.00 | 21.88 |
| harvested:MELON | 65.41 | 113.47 |
| sales_cash:MILK | 25,607.82 | 25,935.47 |
| sales_cash:WOOL | 14,506.94 | 21,718.88 |
| sales_cash:STRAWBERRY | 27,841.12 | 42,904.29 |
| sales_cash:WHEAT | 17,001.12 | 16,466.82 |
| sales_cash:CARROT | 3,836.71 | 941.71 |
| sales_cash:MELON | 14,771.94 | 15,505.82 |
| sales_cash:FERTILIZER | 6,429.59 | 13,886.76 |
| sold_units:MILK | 197.88 | 184.59 |
| sold_units:WOOL | 93.18 | 130.65 |
| sold_units:STRAWBERRY | 141.53 | 227.65 |
| sold_units:WHEAT | 390.35 | 398.41 |
| sold_units:CARROT | 83.00 | 21.88 |
| sold_units:MELON | 65.41 | 110.12 |
| sold_units:FERTILIZER | 75.18 | 211.53 |

## Opportunità locali: proxy, non denaro già recuperabile

Conteggi deduplicati per giorno/tile/opcode in presenza di almeno un PASS D15–D30. Le categorie si sovrappongono: non sommarle. HARVEST può anticipare una raccolta già prenotata; WATER può essere deliberatamente omesso; CARE rende solo con FEED, maturazione, raccolta e vendita; fertilizzante richiede spazio nello shed e consegna. Nessun prezzo spot viene moltiplicato ingenuamente per il numero di PASS.

| Tipo | Tile-giorni medi nelle sconfitte |
|---|---:|
| HARVEST | 83.59 |
| CARE | 23.00 |
| COLLECT_FERTILIZER | 32.06 |
| WATER | 52.18 |
| DROP | 0.12 |

## Episodi — campione completo

| Replay | Esito | Avversario | Seat | Cassa nostra | Cassa avversaria | PASS | PASS D15–D30 | Morti crop |
|---|---|---|---:|---:|---:|---:|---:|---:|
| [105851840](https://www.kaggle.com/competitions/episodes/105851840/replay.json) | WIN | Ethan Benjamin Cole | 1 | 62,944 | 2,711 | 1557 | 727 | 0 |
| [105852748](https://www.kaggle.com/competitions/episodes/105852748/replay.json) | WIN | Spiros Skarmoutsos | 0 | 66,754 | 43,831 | 1558 | 728 | 0 |
| [105853656](https://www.kaggle.com/competitions/episodes/105853656/replay.json) | WIN | Panagiotis Charalabopoulos | 1 | 89,617 | 86,539 | 1567 | 738 | 1 |
| [105854552](https://www.kaggle.com/competitions/episodes/105854552/replay.json) | LOSS | GzmCR632 | 0 | 77,319 | 105,196 | 1558 | 728 | 0 |
| [105855480](https://www.kaggle.com/competitions/episodes/105855480/replay.json) | LOSS | izack2666 | 1 | 71,131 | 74,977 | 1562 | 728 | 0 |
| [105856416](https://www.kaggle.com/competitions/episodes/105856416/replay.json) | WIN | Harith Al-Ani | 0 | 84,601 | 37,879 | 1562 | 728 | 0 |
| [105857319](https://www.kaggle.com/competitions/episodes/105857319/replay.json) | WIN | Karl0106 | 1 | 96,527 | 92,763 | 1603 | 762 | 1 |
| [105858255](https://www.kaggle.com/competitions/episodes/105858255/replay.json) | LOSS | Rudranarayan Pradhan | 0 | 112,671 | 117,751 | 1559 | 728 | 0 |
| [105859109](https://www.kaggle.com/competitions/episodes/105859109/replay.json) | LOSS | mbscgi | 1 | 67,460 | 93,703 | 1558 | 728 | 0 |
| [105860059](https://www.kaggle.com/competitions/episodes/105860059/replay.json) | WIN | Vidushiii | 1 | 100,326 | 81,864 | 1555 | 728 | 0 |
| [105860150](https://www.kaggle.com/competitions/episodes/105860150/replay.json) | WIN | Chaowei Liang | 0 | 64,802 | 59,877 | 1563 | 728 | 0 |
| [105860993](https://www.kaggle.com/competitions/episodes/105860993/replay.json) | WIN | Abhi Kumar Agrawal | 1 | 58,810 | 34,883 | 1566 | 732 | 1 |
| [105861920](https://www.kaggle.com/competitions/episodes/105861920/replay.json) | LOSS | Ankit Sain | 1 | 80,953 | 95,196 | 1566 | 728 | 0 |
| [105862849](https://www.kaggle.com/competitions/episodes/105862849/replay.json) | LOSS | Shivam Shrivastava | 1 | 70,991 | 71,423 | 1568 | 728 | 0 |
| [105863747](https://www.kaggle.com/competitions/episodes/105863747/replay.json) | WIN | Dhruv_Goyal990 | 1 | 82,869 | 72,228 | 1563 | 728 | 0 |
| [105864674](https://www.kaggle.com/competitions/episodes/105864674/replay.json) | LOSS | Jeff Borschowa | 0 | 50,144 | 93,378 | 1655 | 826 | 9 |
| [105865541](https://www.kaggle.com/competitions/episodes/105865541/replay.json) | WIN | Friaseus  | 0 | 74,656 | 68,519 | 1606 | 759 | 0 |
| [105865598](https://www.kaggle.com/competitions/episodes/105865598/replay.json) | LOSS | uzair | 1 | 88,375 | 125,347 | 1557 | 727 | 0 |
| [105866516](https://www.kaggle.com/competitions/episodes/105866516/replay.json) | WIN | Tatsuhito Yoshikawa | 1 | 66,242 | 64,159 | 1558 | 728 | 0 |
| [105867417](https://www.kaggle.com/competitions/episodes/105867417/replay.json) | LOSS | Cow Boy | 1 | 81,669 | 82,538 | 1562 | 728 | 0 |
| [105868327](https://www.kaggle.com/competitions/episodes/105868327/replay.json) | LOSS | crothety liu | 1 | 89,184 | 94,898 | 1562 | 728 | 0 |
| [105869285](https://www.kaggle.com/competitions/episodes/105869285/replay.json) | LOSS | Adil Khabibullin | 0 | 79,547 | 93,014 | 1552 | 728 | 0 |
| [105870210](https://www.kaggle.com/competitions/episodes/105870210/replay.json) | WIN | Finn Brooks | 1 | 107,791 | 79,706 | 1554 | 728 | 0 |
| [105871121](https://www.kaggle.com/competitions/episodes/105871121/replay.json) | LOSS | Tony T | 0 | 113,853 | 129,729 | 1559 | 728 | 0 |
| [105872004](https://www.kaggle.com/competitions/episodes/105872004/replay.json) | LOSS | nya654nya | 0 | 99,031 | 123,568 | 1556 | 728 | 0 |
| [105872959](https://www.kaggle.com/competitions/episodes/105872959/replay.json) | LOSS | Aldibek [dsmlkz] | 1 | 70,616 | 70,981 | 1562 | 728 | 0 |
| [105873859](https://www.kaggle.com/competitions/episodes/105873859/replay.json) | WIN | Nerozud | 0 | 87,600 | 55,877 | 1558 | 728 | 0 |
| [105874761](https://www.kaggle.com/competitions/episodes/105874761/replay.json) | LOSS | BONPU👨‍🌾 | 0 | 55,091 | 82,373 | 1786 | 942 | 23 |
| [105875671](https://www.kaggle.com/competitions/episodes/105875671/replay.json) | LOSS | hikarimaru | 1 | 71,589 | 76,063 | 1562 | 728 | 0 |
| [105876558](https://www.kaggle.com/competitions/episodes/105876558/replay.json) | LOSS | Hunter Mimaroglu | 0 | 115,670 | 118,039 | 1557 | 728 | 0 |

## Provenienza e recupero

I 30 grezzi sono nei percorsi Downloads indicati dal manifest JSON; non sono stati copiati nel repository né cancellati. I link canonici consentono il recupero; verificare SHA-256 e ID prima del riuso. I derivati V2 conservano eventi PASS per worker/turno, stato locale, coda, ledger giornalieri e fonti. Questa raccolta è development/diagnostica, non holdout.

Dataset: `artifacts\derived\E18_28_EXTERNAL_PASS_DIAGNOSIS_20260905_V2.json`.

Eccezioni di riconciliazione:

- Episodio 105852748: `[{'index': 549, 'seat': 1, 'expected': 27623.0, 'reconstructed': 27542.0}]`. Flussi non utilizzati; PASS e score osservati restano validi.

## Verifiche e stato

Nessuna policy, topologia, config, piano o submission modificata. Nessun tuning sugli avversari pubblici, holdout, promozione, pulizia generale, commit o push. [Cause, casi critici e azioni prioritarie](E18_28_EXTERNAL_PASS_CAUSES_AND_NEXT_ACTIONS_IT.md).
