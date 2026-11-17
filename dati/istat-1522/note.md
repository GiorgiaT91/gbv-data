# Numero 1522 — note

Versione 0.1 — 16 novembre 2026.

## File originali

`originali/2025/` (scaricati il 16/11/2026 dalla pagina Istat "Il numero verde 1522: chi chiama, perché e cosa racconta. Anno 2025", pubblicata il 4/9/2026):

- `Tavole_ITA_REV-19ottobre2026.xlsx` — 17 tavole più la 11-bis, trimestri 2023–2025; revisione del 19/10/2026 (da usare al posto della versione di settembre). La Tavola 5 contiene le chiamate valide giorno per giorno dal 1/1/2018 al 31/12/2025.
- `Nota-metodologica.pdf`, `Glossario.pdf`, `Indice-delle-tavole-statistiche.pdf`.

La cartella si chiama `2025` per la data di pubblicazione, ma contiene dati dal 2018.

Esclusa: la serie provinciale 2013–2024 (dettaglio non necessario; sistema precedente).

## Controlli fatti (16/11/2026)

- Totale chiamate valide 2025: 61.303, coerente con la pagina Istat.
- Tavola 5: somme annuali coerenti con la Tavola 1 (2023: 51.713; 2024: 65.048; 2025: 61.303). La riga "29-feb" va sommata a febbraio (2020: 41; 2024: 200).
- Tavola 5, anni 2018–2022: coincide con i valori pubblicati all'epoca (es. III trim 2022 = 7.177). Non è stata ricostruita con il nuovo sistema.
- Il I trimestre 2025 è coerente con il 2024 su tutti gli indicatori (motivi, denuncia, luogo, dati mancanti).

## I quattro periodi di registrazione (decisione del 16/11/2026)

| Periodo | Sistema | Cosa si usa |
|---|---|---|
| 2018–2022 | Piattaforma precedente | Solo il totale delle chiamate valide (Tavola 5) |
| gen 2023 – mar 2025 | Piattaforma 2022, vecchio gestore | Tutto; periodo di riferimento per il profilo delle vittime (37.430 vittime) |
| apr – giu 2025 | Passaggio di gestore | Tutto, dichiarato come trimestre di passaggio |
| lug – dic 2025 | Nuovo gestore | Tutto, confrontato solo al suo interno (16.958 vittime) |

Regole:
- Il totale delle chiamate attraversa tutti i periodi (Istat: i conteggi a livello di chiamata sono sommabili); la linea si interrompe a gennaio 2023 e ad aprile 2025.
- Il dettaglio su vittime e autori resta dentro ciascun periodo, in percentuale.
- Dove i dati mancanti superano circa metà dei casi (denuncia e luogo da aprile 2025), il riquadro dice "dato non utilizzabile in questo periodo" e spiega perché.
- Vittime: nel periodo lug–dic 2025 si usa il totale "Interlocutore è vittima = Sì" (Tavola 1, nota c), come fanno le tavole 10–17.

## Limiti da dichiarare

1. Conta chiamate, non persone: la stessa persona può chiamare più volte.
2. Racconta solo chi chiama, non la diffusione della violenza.
3. Segue l'attenzione pubblica (campagne, TV, cronaca; picco ogni anno a novembre).
4. Informazioni dichiarate al telefono, non verificabili; molti dati mancanti.
5. Risposte multiple su motivo, tipo di violenza (versione "totale") e autore: le somme possono superare il totale.
6. Rottura di serie nel 2023 (piattaforma) e ad aprile 2025 (gestore).
7. Dal 2025 gli uomini sono esclusi dalle vittime (contati fra le chiamate "fuori target").

## Valori principali (calcolati dalle tavole)

gen 2023 – mar 2025, % sulle 37.430 vittime: autore partner o ex 67,9% (Tavola 15: marito, ex marito, convivente, ex convivente, partner, ex partner); non hanno denunciato 69,4%, hanno denunciato 11,8% (Tavola 14); violenza da anni 53,9% (Tavola 12); in casa 70,6% (Tavola 13); violenza principale fisica 41,7%, psicologica 34,6% (Tavola 11).

lug – dic 2025, % sulle 16.958 vittime: autore partner o ex 60,5% (più risposte); denuncia "non risponde" 50,3%; luogo mancante 48,5%; violenza principale psicologica 37,8%, fisica 25,7%.

Passaggio (Tavola 1, % sulle chiamate valide): informazioni sul servizio 34,0% (gen–mar 2025) → 20,3% (apr–giu) → 1,8% (lug–dic); richiesta di aiuto di una vittima 19,4% → 33,8% → 56,5%.

## Da verificare

- [ ] Quanto del salto 2022→2023 (da 32.430 a 51.713 chiamate valide) dipende dal cambio di piattaforma: gen–ott 2023 +38% sul 2022, prima del picco di nov–dic. Possibile domanda a Istat.
- [ ] Significato delle note "(a)" nelle tavole 11, 15 e 17.
- [ ] Uscita delle tavole trimestrali 2026.

## Mockup

Riga 12 della tela "GBV-Data – Tre mockup della web app": impostazione approvata da Giorgia il 16/11/2026 (solo computer; da affinare sul sito).
