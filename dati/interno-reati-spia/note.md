# Denunce dei reati spia — note

Versione 0.1 — 18 novembre 2026. Estratto da `WebApp/dati/istat-denunce/note.md` (v0.2), dove ci sono tutti i controlli.

## File originali

In `originali/`, scaricati il 18/11/2026:

- `denunce-fonte-SDI-SSD-2014-2023.xlsx` (pagina Istat "Il percorso giudiziario"), con indice in PDF.
  - Tavola 1: delitti denunciati e quota di vittime donne (per età e cittadinanza), per regione, 2014–2023.
  - Tavola 2: persone denunciate o arrestate, per sesso, età, cittadinanza, regione, 2014–2023.
- IstatData `DCCV_AUTVITTPS_6` (CSV): autori e vittime dei delitti violenti per sesso ed età, regioni 2007–2024.

## Come è ricavato `dati.csv`

`python elabora.py`. Solo Italia.

| indicatore | categoria | da dove |
|---|---|---|
| `delitti_denunciati` | reato | tavola 1, colonna "Numero di delitti denunciati" |
| `quota_vittime_donne` | reato | tavola 1, "Vittime di sesso femminile (% sul totale delle vittime)", × 100, una cifra decimale |
| `persone_denunciate` | reato; reato`_femmine` | tavola 2, colonne TOTALE e TOTALE FEMMINE |
| `vittime_donne` | reato | IstatData, `DATA_TYPE=VICTIM`, `SEX=2`, `AGE=TOTAL`, Italia, 2023 e 2024 |

Reati: `maltrattamenti`, `stalking`, `percosse`, `violenze_sessuali`, `omicidi` (solo tavola 2 e IstatData), `diffusione_immagini` (dal 2019), `sfregio_viso` e `matrimonio_forzato` (dal 2021).

Calcolati dal sito (non nel CSV): quota di uomini fra le persone denunciate = (totale − femmine) / totale.

## Avvertenze

- Rotture di serie nella tavola 2: violenze sessuali 7.633 (2016) → 4.429 (2017); maltrattamenti 23.057 (2020) → 17.445 (2021); stalking 15.389 → 12.055. I delitti nello stesso periodo crescono. La serie delle persone non è mostrata.
- Tavola 1, regioni 2014–2016: percentuali per cittadinanza di maltrattamenti e stalking scambiate. Non usate.
- In tavola 2 gli anni dal 2019 sono scritti come testo: `elabora.py` li converte.
- Stalking: reato dal febbraio 2009.
