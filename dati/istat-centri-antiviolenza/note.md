# Centri antiviolenza — note

Versione 0.1 — 16 novembre 2026.

## File originali

`originali/2024/` (scaricati il 16/11/2026 dalla pagina Istat "I Centri antiviolenza e le donne che hanno avviato il percorso di uscita dalla violenza – Anno 2024", pubblicata il 10/03/2026):

- `Centri-antiviolenza_Istat-DPO_Anno-2024.pdf` — report con nota metodologica (PDF del 10/03/2026).
- `Tavole-appendice-Centri-Antiviolenza_2024.xlsx` — 41 tavole sui centri (modificate il 06/03/2026).
- `Tavole_Appendice__UtenzaCav_2024.xlsx` — 25 tavole sulle donne in percorso (modificate il 09/03/2026).
- I due indici delle tavole (PDF).

La pagina Istat riporta una modifica del 16/10/2026, ma i file scaricati sono quelli di marzo: nessuna revisione visibile.

## Cosa contiene

- Solo l'anno 2024. Nessuna serie nelle tavole.
- Nel testo del report: centri attivi 281 (2017) → 409 (2024, +1,2% sul 2023); donne in percorso negli stessi centri 26.000 (2022), 31.700 (2023), circa 35.550 (2024; più 850 in centri nuovi o non rispondenti nel 2023).
- Le edizioni precedenti (centri dal 2017, utenza dal 2020) non sono ancora scaricate.

## Controlli fatti (16/11/2026)

Coerenti:
- 409 centri attivi, 364 rispondenti (89,0%), 36.408 donne in percorso: tavole e report coincidono.
- Tavola 1 utenza (anno di inizio del percorso) somma a 36.408.

Incoerenze (da chiedere a Istat insieme alle altre domande):
1. Tavola 13 utenza: "Ex fidanzato" vale "2,93" come testo; dovrebbe essere circa 2.930 (9.853 − 6.923). "Sconosciuto" compare sotto "Amico, conoscente, collega".
2. Tavole 13 e 22: stessi 37.808 autori, distribuzione diversa (partner attuale 19.968 contro 20.238; amico/conoscente/collega 3.946 contro 3.656).
3. Tavole 15 e 20: base di 21.224 "autori denunciati"; secondo la tavola 22 i denunciati sono 16.411 (18.716 con le segnalazioni informali).
4. Tavola 9 utenza (violenza subita nell'anno), riga "Meno di 29": 13.981 casi di violenza psicologica su 7.879 donne sotto i 30 anni (tavola 4). Valore impossibile anche con risposte multiple per tipo. Si usa la tavola 8.

## Decisione (16/11/2026)

- Si usano i dati sui centri (tavole centri) e sulle donne in percorso: età, cittadinanza, violenze subite (tavola 8), durata (tavola 10), a chi si erano rivolte prima (tavola 3), emergenza (tavola 2).
- Si tengono fuori, per ora, autori, denunce, imputazioni, condanne e provvedimenti (tavole 13, 15–23 utenza) e la tavola 9. Nell'app un riquadro "dati non utilizzati in questa versione" con il motivo.
- La mail a Istat si scrive quando saranno raccolti i dati di tutte le fonti mancanti.

## Limiti da dichiarare

1. Ha risposto l'89% dei centri, con forti differenze regionali (Sicilia 55,9%, Basilicata 50%, Umbria 66,7%, Campania e Molise 75%, Puglia 86,2%, Lombardia 93%). Le percentuali sono sui centri rispondenti.
2. Conta le donne in percorso nell'anno, comprese quelle che lo avevano iniziato dal 2020 in poi (23,6%): non è un flusso e non si confronta con le chiamate al 1522.
3. 61.370 donne hanno contattato un centro, 36.408 hanno avviato un percorso; i contatti ripetuti non sono pubblicati (raccolta difforme fra centri).
4. Molte informazioni mancanti (alcune domande non sono obbligatorie).
5. Risposte multiple su tipo di violenza e su chi la donna aveva contattato prima.

## Valori principali (% sulle 36.408 donne)

- Prima del centro (tavola 3): parenti o amici 55,6; forze dell'ordine 40,2; servizi sociali 21,5; pronto soccorso o ospedale 20,8; avvocato 17,0; psicologo 13,0; 1522 8,4; altri centri 6,2.
- Violenze subite (tavola 8): psicologica 89,1; fisica 64,5; minacce 52,3; economica 39,7; stalking 22,8; altra violenza sessuale 13,6; stupro o tentato stupro 10,4.
- Durata (tavola 10): più di 5 anni 41,8; 1–5 anni 32,6; 6 mesi–1 anno 13,2; fino a 6 mesi 8,6; un episodio 3,8.
- Età 30–49 anni: 54,4% (tavola 4); straniere 26,9% (9.797).
- In emergenza: 16,5% (5.994, tavola 2). Iniziato nel 2024: 27.816 (76,4%).
- Centri: 0,14 ogni 10 mila donne (Sud 0,18, Nord 0,11); 702 sportelli in 193 centri; personale 6.994, volontario il 48,5% (56,1% nel 2017); donne per centro: Nord-ovest 241, Nord-est 238, Sud 72, Italia 169.
- 99,7% dei centri aderisce al 1522 (tavola 14 centri).

## Mockup

Riga 13 della tela "GBV-Data – Tre mockup della web app": A (prima le donne) e B (prima il territorio), solo computer. **Scelta la B** (16/11/2026): numeri chiave, tabella regionale con centri, centri ogni 10 mila donne e centri rispondenti (⚠ sotto l'80%), donne per centro, andamento nel tempo, poi le donne in percorso, riquadro sui dati esclusi, limiti, scheda, domanda finale.

## Edizioni precedenti (controllate il 16/11/2026)

Cartelle in `originali/`, per anno dei dati (riorganizzate il 16/11/2026):
- `2018/` → report centri 2018 (pubblicato ott 2020).
- `2019/` → tavole centri 2019 (il foglio "Quanti sono" riporta i 281 centri rispondenti; gli attivi erano 340).
- `2020/` → tavole centri 2020; report centri e case rifugio 2020 (pubbl. 2022); utenza 2020 ("Effetti della pandemia", 2021).
- `2021/` → centri 2021 (report "Il sistema della protezione", mar 2023, e tavole); utenza 2021 (report e tavole).
- `2022/`, `2023/`, `2024/` → centri e utenza dell'anno.
- Manca un report sul 2017: il dato (281 centri) è citato nei report successivi.

Spostati in altre cartelle: case rifugio 2019, 2020, 2021 → `dati/istat-case-rifugio/originali/<anno>/`; tavole 1522 del 2021 e del 2022 → `dati/istat-1522/originali/2021/` e `2022/`; tavole sugli omicidi (`Tavole263847.xlsx`) → `dati/istat-omicidi/originali/`.

### Serie ricostruita

| Anno | Centri attivi | Centri rispondenti | Risposta | Donne che hanno contattato un centro | Donne in percorso (indagine sull'utenza) |
|---|---|---|---|---|---|
| 2017 | 281 | — | — | — | — |
| 2018 | 302 | 257 | 85% | 49.394 | — |
| 2019 | 340 | 281 | 83% | circa 50.600 (ricavato: 2020 meno 3.964) | — |
| 2020 | 350 | 263 | 75% | 54.609 | 15.387 (solo percorsi iniziati nel 2020; 270 centri su 365) |
| 2021 | 373 | 307 | 82% | 56.349 | 19.592 |
| 2022 | 385 | 349 | 91% | 60.751 | 26.131 (poi 26.000 a centri costanti) |
| 2023 | 404 | 363 | 90% | 61.514 | 31.593 (poi 31.700 a centri costanti) |
| 2024 | 409 | 364 | 89% | 61.370 | 36.408 |

Fonti: tavole 1 e 2 delle appendici sui centri (2019 "Quanti sono" = rispondenti; 2020 "RISP" e "ATT"); testi dei report per 2017, 2018, 2019, contatti e utenza.

### Cosa si può confrontare

- **Centri attivi 2017–2024:** sì, con una nota (dal 2017 i centri sono quelli che rispettano i requisiti dell'Intesa Stato-Regioni del 2014; da verificare se l'Intesa del 2022 ha cambiato il perimetro).
- **Donne che hanno contattato un centro 2018–2024:** sì, ma sono contate solo nei centri che rispondono, e la risposta varia dal 75% al 91%. Parte dell'aumento può dipendere da più centri rispondenti.
- **Donne in percorso (utenza):** solo 2022–2024, con i valori a centri costanti del report 2024. Prima la partecipazione all'indagine era più bassa e il 2020 contava solo i percorsi iniziati nell'anno.
- **Tassi:** nel report 2018 per 10 mila abitanti (0,05); dal 2020 anche per 10 mila donne. Si usa solo il tasso per donne.
- **Due misure diverse di "donne in percorso":** il questionario dei centri dà numeri aggregati più alti (30.359 nel 2020; 34.500 al 31/12/2021) dell'indagine sull'utenza (schede individuali). Non vanno mescolate: si usa l'indagine sull'utenza.

### Da verificare

- [ ] Effetto dell'Intesa Stato-Regioni del 2022 sul perimetro dei centri contati.
- [x] File di altre fonti spostati e cartelle rinominate per anno dei dati (16/11/2026).

## Anno 2025 (verificato il 16/11/2026)

Non ancora pubblicato. La pagina Istat della rilevazione indica il 2025 come periodo in raccolta per l'utenza. Edizioni precedenti uscite a novembre 2024 (dati 2023) e marzo 2026 (dati 2024): data del 2025 non annunciata. Ricontrollare dopo il 25/11/2026.

Dato collegato: indagine Istat sulla sicurezza delle donne 2025, ricorso ai centri antiviolenza delle vittime di partner o ex 8,7% (4,4% nel 2014), donne italiane 16–70 anni (Rapporto SDGs 2026, Goal 5). È un'indagine campionaria, non un registro dei centri: va citata a parte.
