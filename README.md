# GBV-Data

Che cosa sappiamo sulla violenza di genere e sui femminicidi in Italia, che cosa non sappiamo, e perché i numeri disponibili non coincidono.

Sito: https://giorgiat91.github.io/gbv-data/

## Com'è fatto

| Cartella | Contenuto |
|---|---|
| `dati/<fonte>/` | `dati.csv` (tabella pulita), `scheda.yaml` (informazioni sulla fonte), `note.md` (come sono stati ricavati i numeri), `originali/` |
| `contenuti/domande.yaml` | Le sei domande, nell'ordine della home, con lo stato (pronta o in lavorazione) |
| `contenuti/fonti.yaml` | Le dodici fonti, con la domanda a cui rispondono e lo stato |
| `contenuti/cambiamenti.yaml` | Gli aggiornamenti del sito: alimenta la pagina «Cosa è cambiato» e il feed RSS |
| `contenuti/domande/` | I testi delle pagine delle domande |
| `src/componenti/` | Gli elementi riusabili della pagina |
| `src/pages/` | Le pagine del sito (il nome della cartella è imposto da Astro) |
| `src/lib/` | Lettura di dati e testi |

I numeri delle pagine vengono letti da `dati/<fonte>/dati.csv` quando il sito viene costruito. Per aggiornare un numero si cambia una riga del CSV, non la pagina.

Dell'Osservatorio di Non Una Di Meno questo archivio contiene solo i totali (`dati/nudm-osservatorio/dati.csv`). I file caso per caso restano fuori: quelli originali contengono nomi e testi di cronaca, e anche le copie senza nomi riportano data, comune ed età, che permettono di riconoscere le persone.

## Come si aggiorna una fonte

1. Salvare il nuovo file della fonte in `dati/<fonte>/originali/`.
2. Aggiornare le righe di `dati/<fonte>/dati.csv` (UTF-8 con BOM).
3. Aggiornare in `scheda.yaml` le date dell'ultimo aggiornamento e dell'ultima verifica.
4. Inviare le modifiche su GitHub: il sito si ricostruisce e si pubblica da solo.

## Come si pubblica una nuova domanda o fonte

1. Fonte: compilare `dati/<fonte>/` (dati.csv, scheda.yaml con il campo `ultimo_dato`, note.md), aggiungere l'infografica e mettere `pronta: true` in `contenuti/fonti.yaml`. La fonte compare da sola nell'archivio, nel calendario e nei dati scaricabili.
2. Domanda: quando la pagina è pronta, mettere `stato: pronta` e `indirizzo:` in `contenuti/domande.yaml`.
3. Aggiungere una voce in cima a `contenuti/cambiamenti.yaml`.

## Lavorare in locale

Serve Node.js (versione LTS).

```
npm install
npm run dev
```

L'anteprima è all'indirizzo che compare nel terminale, di solito http://localhost:4321/gbv-data/

## Fonti

- Istat, Le vittime di omicidio
- Ministero dell'Interno, Omicidi volontari e femminicidi
- Osservatorio nazionale Non Una Di Meno (dati CC BY-SA 4.0)

## Licenze

Da definire.
