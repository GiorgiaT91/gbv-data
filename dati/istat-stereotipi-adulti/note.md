# GBV-Data — Stereotipi di genere: i dati disponibili

Versione 0.1 — 16 novembre 2026. Ricognizione dei file in `dati/istat-stereotipi/originali/`, controllati uno per uno.

**Regola di lavoro (decisa da Giorgia, 16/11):** si usano i dati così come sono. La loro scarsità è essa stessa un limite del dato e va dichiarata nell'app.

---

## 1. Le tre rilevazioni

| | Adulti 2018 | Adulti 2023 | Ragazze e ragazzi 2023 |
|---|---|---|---|
| Popolazione | 18–74 anni | 18–74 anni | 11–19 anni (alcune domande solo 14–19) |
| Come è stata raccolta | Modulo dentro l'indagine sulle forze di lavoro | Indagine a sé, circa 15.000 persone, maggio–luglio 2023 | Modulo dentro l'indagine "Bambini e ragazzi 2023" |
| Pubblicazioni | Report 25/11/2019 | Primi risultati provvisori 22/11/2023; tavole per età 31/10/2024 | Comunicato 25/07/2025 |
| Dati in tabella | 21 dataset IstatData + appendice con 18 tavole | 4 tavole, solo per età | Nessuna: solo grafici e testo del PDF |
| Stato del dato | Definitivo | Tavole 2024 senza indicazione; i primi risultati sono provvisori | Non indicato |
| Ricchezza | Alta | Bassa | Bassa |

---

## 2. Cosa c'è, tema per tema

Legenda: **T** = in tabella (Excel o CSV); **P** = solo nel PDF (testo o grafico, da trascrivere); — = assente.

| Tema | 2018 adulti | 2023 adulti | 2023 ragazzi |
|---|---|---|---|
| Almeno uno stereotipo sui ruoli | T: sesso, età, titolo, regione | T: età | P: sesso, cittadinanza |
| Singoli stereotipi sui ruoli | T: 5 affermazioni; sesso, età, titolo, regione | T: 9 affermazioni, età. P: sesso (prospetto 1) | P: 4 affermazioni, per ripartizione |
| Almeno uno stereotipo sulla violenza sessuale | T: sesso, età, titolo, regione | T: età | P: solo nel testo |
| Singoli stereotipi sulla violenza sessuale | T: 7 affermazioni; sesso, età, titolo, regione | T: 8 affermazioni, età. P: sesso per 2 affermazioni | P: 3 affermazioni, sesso ed età (14–19), ripartizione |
| Accettabilità della violenza nella coppia | T: 3 comportamenti; sesso, età, titolo, regione | T: 3 comportamenti, età | P: 3 comportamenti, sesso ed età (14–19) |
| Percezione della diffusione della violenza | T: sesso, età, titolo, regione | P: due valori nel testo | — |
| Cause della violenza nella coppia | T: sesso, età, titolo, regione | P: tre valori nel testo | — |
| Consigli a una donna che subisce violenza | T: sesso, età, titolo, regione | — | — |
| Qualità importanti in un uomo e in una donna | — | P: grafico | — |
| Rapporto di coppia (cosa conta, gelosia) | — | — | P: grafico e testo |

---

## 3. Cosa si può confrontare fra 2018 e 2023 (adulti)

Solo le **singole affermazioni presenti in entrambe le edizioni**, sul totale e per età. Va sempre dichiarato che le due rilevazioni sono state condotte in modo diverso.

| Affermazione | 2018 | 2023 |
|---|---|---|
| Per l'uomo è più importante avere successo nel lavoro | 32,5 | 20,4 |
| Gli uomini sono meno adatti alle faccende domestiche | 31,4 | 21,4 |
| È l'uomo che deve provvedere alla famiglia | 27,9 | 17,2 |
| Se il lavoro scarseggia, precedenza agli uomini | 16,1 | 8,2 |
| È l'uomo che prende le decisioni più importanti | 8,8 | 6,3 |
| Le donne che non vogliono un rapporto riescono a evitarlo | 39,3 | 34,5 |
| Le donne possono provocare la violenza con il modo di vestire | 23,9 | 17,2 |
| Se è ubriaca o drogata è almeno in parte responsabile | 15,1 | 10,7 |
| Le accuse di violenza sessuale sono spesso false | 10,3 | 7,9 |
| Le donne dicono no ma intendono sì | 7,2 | 4,5 |
| Le donne serie non vengono violentate | 6,2 | 5,5 |
| Se il marito obbliga la moglie non è violenza | 1,9 | 5,6 ⚠️ |
| Controllo abituale del cellulare o dei social della compagna | 17,7 | 10,1 |
| Schiaffo alla fidanzata perché ha flirtato | 7,4 | 2,3 |
| In una coppia ogni tanto ci scappa uno schiaffo | 6,2 | 4,3 |

Valori: % di persone di 18–74 anni molto o abbastanza d'accordo (ruoli, violenza sessuale) o che ritengono il comportamento accettabile sempre o in alcune circostanze (coppia). Fonti: 2018, IstatData e appendice; 2023, tavole per età di ottobre 2024.

**Non confrontabili:**
- gli indicatori "almeno uno stereotipo" (2018: 58,8% ruoli, 54,6% violenza sessuale, 25,4% coppia; 2023: 53,7%, 48,7%, 14,6%), perché sono calcolati su elenchi di affermazioni diversi;
- ⚠️ "se il marito obbliga… non è violenza": il valore triplica, quindi va verificata la formulazione nei due questionari prima di usarlo.

---

## 4. Avvertenze sui file

- **2018, dataset IstatData:** tutti riferiti al solo 2018. Il file "Opinioni su violenza sessuale – età" (RUOLIGEN_7) contiene anche ripartizioni e regioni.
- **2018:** "decisioni in famiglia" 8,8% è coerente (uomini 10,7%, donne 7,1%). "Faccende domestiche" vale 31,4 nelle tavole e 31,5 nel testo del report: si usa 31,4.
- **2023, tavole per età:** non dicono se sono provvisorie o definitive. Coincidono con i primi risultati, salvo il controllo del cellulare (10,1 contro 10,2). Da citare come "Istat, tavole per età, ottobre 2024".
- **2023, tavola 2, cella B23** (18–29 anni): valore "3,1 (a)" con una nota non spiegata nel file.
- **2023, primi risultati:** una frase sulla diffusione percepita della violenza riporta "nel 2022". Probabilmente è un refuso, da non usare senza verifica.
- **Ragazzi, cartella `2023`:** i file "Bambini e ragazzi" (report del 20/05/2024 e 18 tavole in appendice) non contengono dati sugli stereotipi. Da spostare in una sottocartella di contesto o da togliere.

---

## 5. Limiti da dichiarare nell'app

- Una rilevazione ogni cinque anni circa: 2018, 2023, la prossima nel 2026.
- Il 2018 e il 2023 sono stati rilevati in modo diverso, con elenchi di domande diversi: si confrontano solo le singole affermazioni.
- Del 2023 sono pubbliche solo le tavole per età. Mancano sesso (se non nel PDF), titolo di studio, regione, cause e consigli.
- Per ragazze e ragazzi non esistono tavole: i numeri vanno ricavati dai grafici del comunicato.
- Si misurano opinioni dichiarate, non comportamenti.
