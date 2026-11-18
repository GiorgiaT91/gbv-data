# Processi e condanne — note

Versione 0.1 — 18 novembre 2026. Estratto da `WebApp/dati/istat-denunce/note.md` (v0.2), dove ci sono tutti i controlli.

## File originali

In `originali/`, scaricati il 18/11/2026 dalla pagina Istat "Il percorso giudiziario":

| Passo | File | Cosa conta | Anni |
|---|---|---|---|
| Procura | `grafici2018.xlsx` (indice in `Indice-tavole-autori-2018.pdf`) | autori indagati: azione penale o archiviazione; motivi; tempi | 2012–2018 |
| Tribunale | `Tavole-Min-Giustizia-DIT-2021_2023-Sez_DIB.xlsx` | procedimenti iscritti e definiti nelle sezioni dibattimentali; condanna, assoluzione, altro | 2021–2023 |
| Condanna definitiva | `Tavola_*_per_pena_inflitta.xlsx` (3 file) | condannati con sentenza irrevocabile, per reato più grave | 2010–2018 (2018 provvisorio) |
| Carcere | `DETENUTI-anni-2024-fonte-DAP.xlsx` | detenuti adulti presenti | 2010–2024 |

## Come è ricavato `dati.csv`

`python elabora.py`. Solo Italia.

| indicatore | da dove |
|---|---|
| `indagati_azione_penale`, `indagati_archiviati` | procure, tavola 1 (anche `stalking_partner_ex`) |
| `archiviati_nel_merito`, `archiviati_improcedibilita`, `archiviati_prescrizione`, `archiviati_altri_motivi` | procure, tavola 4, 2018 |
| `giorni_mediani_azione_penale`, `giorni_mediani_archiviazione` | procure, tavola 2, 2018 (mediana in giorni fra iscrizione e decisione) |
| `procedimenti_iscritti`, `procedimenti_definiti` | tribunali, Tab. 1 |
| `definiti_condanna`, `definiti_assoluzione`, `definiti_altro` | tribunali, Tab. 2 (fogli 2021, 2022, 2023 affiancati) |
| `condannati_definitivi` | riga "tutte le voci" delle tavole sulle condanne |
| `detenuti` | primo blocco della tavola DAP (valori assoluti), colonna "totale", riga "Totale" cittadinanza |

Calcolati dal sito: quote di azione penale, di archiviazione per motivo, di condanna e assoluzione.

## Avvertenze

- Unità e anni diversi a ogni passo: nessun rapporto "denunce → condanne".
- Tribunali: le righe non si sommano (più reati nello stesso procedimento); la condanna comprende i patteggiamenti.
- Condanne: classificate per reato più grave. Violenza sessuale 2017: 49 condanne a "sola multa", valore anomalo (nel 2016 erano 0).
- Detenuti: due percentuali impossibili nel 2015 per la tratta (errore Istat, non usato).
