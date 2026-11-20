# Domanda «Cosa non sappiamo ancora?» (messa da parte il 20/11/2026)

Tolta dal sito per ora: è molto tecnica e richiede una conoscenza più approfondita.
Da riprendere quando si decide come rendere il messaggio del vuoto.
Questa cartella è fuori da `src/`, quindi Astro non la pubblica.

## Come rimetterla

1. `cosa-non-sappiamo-ancora.astro` → `src/pages/domande/`
2. `5-cosa-non-sappiamo-ancora.yaml` → `contenuti/domande/`
3. In fondo a `contenuti/domande.yaml`, il blocco:

```yaml
- id: 5
  testo: "Cosa non sappiamo ancora?"
  home:
    etichetta: "I vuoti"
    forma: vuoti
    testo_numero: "Legge 53/2022"
    descrizione: "I dati che la legge prevede, messi a confronto con quelli pubblicati oggi."
    fonte_breve: "Lettura di GBV-Data"
  stato: in-verifica
  modello: lista            # pagina propria: src/pages/domande/cosa-non-sappiamo-ancora.astro
  indirizzo: /domande/cosa-non-sappiamo-ancora/
  fonti: []
```

4. In `src/pages/index.astro`, nello stile: la tessera tratteggiata a tutta larghezza

```css
  .posto.vuoti { grid-column: 1 / -1; }
  .tessera.vuoti { background: var(--grigio); border: 2px dashed var(--grigio-medio); }
  .vuoti .numero { font-size: 36px; color: var(--testo-2); }
```

   e il testo di apertura torna a «Sei domande.».
5. Nella pagina «Quante donne vengono uccise?»: in `contenuti/domande/4-quante-donne-vengono-uccise.yaml`, sotto `limiti`, `collegamento: "Vai a: cosa non sappiamo ancora"`; in `src/pages/domande/quante-donne-vengono-uccise.astro`, dopo l'elenco dei limiti,
   `<a class="prossimamente" href={url('/domande/cosa-non-sappiamo-ancora/')}>{t.limiti.collegamento} →</a>` con lo stile
   `.prossimamente { font-size: 15px; color: var(--limiti-titolo); font-weight: 600; }`.
6. «Il progetto» (`contenuti/pagine/il-progetto.yaml`): «cinque domande» → «sei domande».
