# Osservatorio Non Una Di Meno — note di lavorazione

Ultima verifica: 14 novembre 2026.

## Infografica (decisa il 14 novembre 2026, modello B)

1. **Grafico principale:** femminicidi per anno, 2020–2026 (2026 parziale, all'8 novembre). Accanto, una piccola tabella con le altre voci (transcidi, suicidi indotti, casi in accertamento), mai sommate ai femminicidi.
2. **Dettaglio 1, "Almeno una su otto aveva già chiesto aiuto":** femminicidi con denunce o contatti precedenti con centri antiviolenza o servizi sociali, per anno.
3. **Dettaglio 2, "Il reato di femminicidio nel 2026":** donne uccise da partner o ex nel 2026, per reato contestato.

Esclusi per scelta: nomi, città, cause di morte, descrizioni, nazionalità, sex work, disabilità (dati personali o a rischio di stereotipi); età e suicidi degli autori (ripetono Istat).

## Da dove vengono i valori

- `originali/I dati del AAAA.csv`: file scaricati dall'archivio dati del sito (https://osservatorionazionale.nonunadimeno.net/), un caso per riga, il 13 novembre 2026. **Non si modificano.** Versioni: 2020–2024 "ottobre 2025", 2025 "dicembre 2025", 2026 "novembre 2026".
- `elabora.py` legge gli originali e scrive:
  - `pubblicabili/nudm_AAAA.csv`: copie senza nomi (vittima e presunto autore) e senza testi liberi (descrizioni del caso, delle altre persone uccise, della giustificazione e della disabilità riportate dai media, "cosa succede dopo", descrizione e iter del reato). Sono queste, e non gli originali, a poter andare nell'archivio pubblico.
  - `dati.csv`: i valori dell'infografica.
- Per aggiornare: scaricare il nuovo file del 2026 in `originali/`, correggere `PERIODO` in `elabora.py`, rilanciare `python3 elabora.py`.

## Come sono contati

- **Femminicidi:** righe con Tipo "omicidio" e vittima indicata come donna ("(F)"). Coincide con la voce "femminicidi" del sito.
- **Transcidi:** Tipo "omicidio" e persona trans. **Suicidi indotti:** Tipo "suicidio" (donne, persone trans e, in tre anni, un uomo). **In accertamento:** Tipo "in corso di accertamento". **Altre voci:** persone scomparse, "non accettazione", uomini uccisi negli stessi contesti.
- **Denunce o contatti precedenti:** colonna "Denunce e/o contatti/accesso a CAV o SS" = SI, solo fra i femminicidi. È un minimo: dipende da ciò che riportano i giornali.
- **Relazione con l'autore:** raggruppata da noi (partner o ex; altro familiare; altri; non indicata). L'elenco delle voci è in `elabora.py`.
- **Reato contestato (solo 2026):** colonna presente solo nel file 2026, raggruppata da noi (femminicidio art. 577-bis; omicidio volontario anche aggravato; preterintenzionale o colposo; reato estinto per morte dell'autore; non indicato). Riporta ciò che dicono i media e può cambiare con le indagini.

## Confronto con le cifre del sito (14 novembre 2026)

| Anno | Femminicidi nel file | Sul sito | Nota |
|---|---|---|---|
| 2020 | 118 | 118 | La voce "femminicidi" esiste già nel 2020: la serie parte dal 2020 |
| 2021 | 115 | "115 donne uccise" | Stessa voce: il 2021 non va saltato |
| 2022 | 107 | 107 | |
| 2023 | 106 | 107 (totale 123; file 122) | **Deciso (14/11): si usa il sito, 107 e 123** (correzione in `elabora.py`) |
| 2024 | 99 | 99 | |
| 2025 | 84 | 84 | Suicidi indotti: 6 nel file, 7 sul sito (forse il caso "non accettazione") |
| 2026 | 70 | 71 (totale 83 = file) | **In attesa del file aggiornato all'8 dicembre.** Il totale 83 coincide: la somma 84 della bozza era un errore di lettura |

In pagina si usano i valori del file, citando la versione e la data di download.

## Transcidi e lesbicidi: una differenza di definizione

- L'Osservatorio conta a parte le persone trans uccise (transcidi) e quelle morte per suicidio indotto. Istat e Ministero classificano le vittime solo come maschi o femmine, secondo i dati di polizia: una donna trans può risultare in una delle due voci e non è riconoscibile.
- "Lesbicidi" compare nel nome dell'Osservatorio, ma nei file non c'è una voce che li distingua: eventuali casi sono dentro i femminicidi. Né Istat né il Ministero rilevano l'orientamento sessuale della vittima.
- Scelta: il numero principale resta "femminicidi" (senza persone trans); i transcidi sono mostrati come voce separata, mai sommata. È anche un esempio per la domanda 5: le statistiche ufficiali non vedono le persone trans.

## Licenza

CC BY-SA 4.0: citare sempre l'Osservatorio; le rielaborazioni (copie pubblicabili, `dati.csv`) vanno pubblicate con la stessa licenza.

## Da fare

- [x] 2023: si usa il valore del sito (107).
- [ ] 2026: ricontrollare dopo l'aggiornamento dell'8 dicembre.
- [ ] Rivedere insieme il raggruppamento delle relazioni in `elabora.py`.
- [ ] Ogni mese, dopo l'8: riscaricare il file del 2026 e rilanciare `elabora.py`.
