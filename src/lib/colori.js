// Colori dei grafici. Stessi valori del foglio di stile, scritti qui perché
// gli attributi dei disegni SVG non leggono le variabili CSS in modo affidabile.
export const C = {
  accento: '#5A2D82',      // partner o ex; dato principale
  familiare: '#8E6BB3',    // altro familiare; seconda voce
  lilla: '#C4B2D9',        // terza voce chiara
  grigio: '#B5B5AF',       // conoscente; reato estinto
  grigioChiaro: '#DCDCD6', // altre persone; sconosciuto
  uomini: '#8A8A84',
  bianco: '#FFFFFF',
  bordo: '#8A8A84',
  griglia: '#E6E6E1',
  testo: '#16181D',
  testo3: '#55585F',
};

// Colore del testo da scrivere sopra un riempimento.
export function testoSu(colore) {
  return [C.accento, C.familiare].includes(colore) ? C.bianco : C.testo;
}

export function percentuale(n, decimali = 0) {
  return n.toLocaleString('it-IT', { minimumFractionDigits: decimali, maximumFractionDigits: decimali });
}

// Periodi di registrazione del 1522 (e, in generale, fasi di una serie con rotture).
export const PERIODI = {
  precedente: '#8A8A84',  // sistema precedente
  riferimento: '#5A2D82', // periodo di riferimento
  passaggio: '#B4651E',   // passaggio
  nuovo: '#8A4A12',       // nuovo sistema
};

// "41,7%" a partire da una parte e un totale.
export function quota(parte, totale, decimali = 1) {
  return `${percentuale((100 * parte) / totale, decimali)}%`;
}
