# Ministero dell'Interno, omicidi volontari e femminicidi — note di lavorazione

Ultima verifica: 13 novembre 2026.

## Da dove vengono i valori

Tutti i valori di `dati.csv` vengono dal report "Omicidi volontari e femminicidi", Servizio Analisi Criminale, Roma, ottobre 2026 (file `report_omicidi_iii_trimestre.pdf`, 8 pagine, letto direttamente).

| Valori | Pagina del PDF |
|---|---|
| Triennio 2023–2025 (omicidi, ambito familiare/affettivo, partner/ex, con vittime donne) | 3 |
| Femminicidi art. 577 bis: zero fra il 17 e il 31 dicembre 2025; 15 fra gennaio e settembre 2026 | 5 |
| Gennaio–settembre 2025 e 2026: le tre tavole complete (omicidi volontari, femminicidi, totale delle due voci), sia il totale sia le vittime donne | 6 e 7 |
| Età dei presunti autori noti, gennaio–settembre 2025 e 2026 (valori assoluti letti dai grafici a torta) | 8 |

Eccezione decisa il 13 novembre 2026: per questa fonte le tavole delle pagine 7 e 8 sono riportate per intero, anche le righe che l'infografica non usa. Per le altre fonti vale la regola generale: solo i valori che servono all'infografica.

## Come leggere i numeri del 2026

Dal 2026 il ministero tiene separate due voci:
- omicidi volontari (art. 575): 215 vittime, di cui 52 donne;
- femminicidi (art. 577 bis): 15 vittime.

Il totale delle donne uccise è quindi 52 + 15 = **67**. Nello stesso periodo del 2025 erano 77.

Donne uccise da partner o ex nei primi nove mesi del 2026: 23 registrate come omicidio volontario + 15 come femminicidio = **38**.

## Età dei presunti autori (pagina 8)

- I valori in `dati.csv` sono i numeri assoluti dei grafici a torta: 570 nel 2025, 517 nel 2026. Le percentuali non sono riportate perché si ricavano dai numeri.
- L'unità non sono le persone ma **denunce e arresti** a carico di presunti autori noti. Secondo la nota del report, possono riferirsi anche a fatti di anni precedenti, quindi non vanno confrontati con il numero delle vittime.
- I dati riguardano gli autori di tutti gli omicidi, con vittime di entrambi i sessi, non solo quelli con vittime donne.
- **Incongruenza nel report:** il testo dice che il 2025 comprende "solo omicidi volontari", mentre il titolo del grafico indica gli artt. 575 e 577 bis. Nei primi nove mesi del 2025 il femminicidio non era ancora reato, quindi le due versioni coincidono nei fatti.
- **Arrotondamento:** il report indica 7% per gli over 65 nel 2026, ma 33 su 517 fa 6,4%. Sembra un arrotondamento forzato per far tornare il totale a 100.

## Cosa il report non contiene

- Nessun dettaglio territoriale.
- Nessuna informazione su denunce precedenti o misure di protezione.
- Nessuna spiegazione del criterio con cui un caso è registrato come femminicidio.
- Sesso e nazionalità degli autori; c'è solo l'età, e non separata fra omicidi e femminicidi né per sesso della vittima.
- La pagina 4 del PDF contiene un grafico senza testo estraibile: da guardare a occhio.

## Incongruenze con altre fonti, da spiegare

- Donne uccise nel 2023 e nel 2024: 119 per il ministero, 117 e 116 per Istat. Stessa banca dati, ma il ministero pubblica dati operativi e Istat dati consolidati.
- Omicidi totali nel 2025: 296 in questo report; a gennaio 2026 la stampa riportava 286 dal consuntivo del ministero. I dati operativi vengono rivisti.
- Il Dossier di Ferragosto 2026 riportava 34 donne uccise nel primo semestre.

## Da fare

- [x] PDF spostato in `originali/` (12 novembre 2026). Facoltativo: aggiungere la data al nome del file.
- [ ] Recuperare i report del primo e del secondo trimestre 2026.
- [x] Pagina 4 del PDF: tre grafici con gli stessi valori della tabella di pagina 3; coincidono (13 novembre 2026).
- [ ] Verificare cadenza e data del prossimo report.
- [ ] Verificare la licenza.
