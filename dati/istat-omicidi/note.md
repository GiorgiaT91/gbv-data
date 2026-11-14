# Istat, le vittime di omicidio — note di lavorazione

Ultima verifica: 13 novembre 2026.

## Infografica (decisa il 13 novembre 2026, impaginazione B del mockup)

1. **Grafico principale, "Cento l'anno":** serie 2002–2024 delle donne uccise per tipo di autore, in tre gruppi (partner o ex; altro familiare; altri o autore non identificato), con la linea dei femminicidi stimati 2019–2024. Titolo-messaggio: "Da oltre vent'anni, circa cento donne l'anno vengono uccise da un partner o da un familiare".
2. **Donne e uomini, chi li uccide (2024):** due barre divise per tipo di autore. Titolo: "Le donne sono uccise quasi sempre in famiglia, gli uomini soprattutto da sconosciuti".
3. **Età (2021–2024 sommati):** quota di vittime per fascia d'età, donne e uomini. Titolo: "Quasi quattro donne uccise su dieci avevano 65 anni o più".

Scelte: percentuali e non tassi (da rivalutare con il rapporto 2025); territorio escluso (non ritenuto utile); `dati.csv` contiene i valori assoluti, le percentuali si calcolano nel sito.

## Da dove vengono i valori

File in `originali/`:
- `Report_Le-vittime-di-omicidio_Anno-2024.pdf` (Istat, 25 novembre 2025), 12 pagine.
- `Appendice-statistica_Vittime-di-omicidio_Anno-2024.xlsx`, appendice statistica dello stesso report.
- Report PDF e appendici Excel 2021, 2022, 2023 (per il 2023 le regioni sono nel file separato `Appendice-statistica_regione_Anno-2023.xlsx`).

| Valori in `dati.csv` | Dove |
|---|---|
| Donne uccise per tipo di autore, 2002–2024 | Excel, tavola A7, valori assoluti |
| Femminicidi stimati, 2019–2024 | PDF, pagina 8 (non presenti nell'Excel) |
| Femminicidi stimati 2024 per autore (62, 37, 7) | PDF, pagina 8 |
| Donne e uomini uccisi nel 2024 per autore (grafico 2) | Excel 2024, tavola A1, riga ITALIA |
| Donne e uomini uccisi per età, 2021–2024 sommati (grafico 3) | Excel 2021, 2022, 2023, 2024, tavole A2 |

**Raggruppamenti fatti da noi** (tavola A7):
- `autore_partner_o_ex` = "Partner" + "Ex partner".
- `autore_altro_familiare` = "Altro parente".
- `autore_altri_o_non_identificato` = "Altro conoscente" + "Autore sconosciuto alla vittima" + "Autore non identificato".

Le tre voci sommate danno il totale di ogni anno (controllato).

## Verifica (13 novembre 2026)

- Serie delle donne uccise 2019–2024: PDF e Excel coincidono (111, 116, 119, 126, 117, 116).
- 2024: 62 partner o ex (55 + 7) e 37 altri familiari coincidono fra PDF ed Excel.

## Età, 2021–2024: come è stata costruita

- Classi comuni ai quattro anni: 0–13, 14–17, 18–24, 25–34, 35–44, 45–54, 55–64, 65 e oltre. Il 2021 raggruppa tutte le età da 65 anni in su; gli altri anni dividono 65–74, 75–84, 85 e oltre (2022 e 2023: 85–94 e 95 e più).
- Totali controllati: donne 119 + 126 + 117 + 116 = 478; uomini 184 + 196 + 217 + 211 = 808, di cui 1 di età non indicata (2022), escluso dalle classi.
- Le tavole A2 dei file 2023 e 2024 sono intitolate "Anno 2022", ma i totali sono quelli dell'anno giusto.

## Avvertenze sui dati

- **2002 e 2003:** "ex partner" e "altro conoscente" valgono 0 in tutte le tavole. Probabilmente non erano ancora rilevati: gli ex partner sono forse contati fra i partner o fra gli altri autori. Per questi due anni il gruppo "partner o ex" può essere sottostimato.
- **2022:** la fonte non distingue partner ed ex partner. Il problema non tocca `dati.csv`, che li tiene insieme.
- **2024:** "Autore non identificato" per le donne è indicato con "-"; trattato come 0.
- Le donne uccise da partner o familiari sono la base della stima Istat (99 su 106 nel 2024), ma la serie 2002–2018 **non è una serie di femminicidi stimati**: Istat ha pubblicato la stima solo dal 2019. In pagina va detto così.

## Stranezze del file Excel

- Il file 2024 era scaricato col nome "Anno-2025-Corretto": rinominato. "Corretto" perché Istat ha sostituito le tavole il 26 novembre 2025 (nella A3 i numeri di uomini e donne erano invertiti); questa è la versione corretta.
- La tavola A2 è intitolata "Anno 2022", ma i totali sono quelli del 2024.
- Le tavole A5–A7 sono intitolate "Anni 2002–2023", ma contengono anche il 2024.
- Tavola A1, riga "Isole", donne: totale indicato con "-" anche se le voci valgono 4, 10 e 2.

## Dati disponibili ma non usati

Nell'Excel: regioni e ripartizioni (A1), cittadinanza (A3), tassi per 100mila. Nel PDF: tassi per sesso ed età, dettaglio dei familiari autori, suicidi degli autori, orfani. Esclusi per scelta (13 novembre 2026): territorio, anche per ripartizione (non ritenuto utile); regioni (numeri troppo piccoli); cittadinanza (rischio di alimentare stereotipi).

## Da fare

- [x] Scaricare PDF e tavola Excel in `originali/` (13 novembre 2026).
- [x] Ricontrollare la serie 2019–2024 e annotare pagina e tavola.
- [ ] Verificare la licenza dei dati Istat.
- [ ] Dopo il 25 novembre 2026: aggiungere l'anno 2025 (nuova appendice Excel e stima dei femminicidi); età su 2021–2025; valutare i tassi al posto delle percentuali.

## Attenzione

Il numero di donne uccise secondo Istat (117 nel 2023, 116 nel 2024) non coincide con quello del report del Ministero dell'Interno (119 in entrambi gli anni), pur partendo dalla stessa banca dati. Il ministero pubblica dati "operativi", Istat dati consolidati. Da spiegare in pagina.
