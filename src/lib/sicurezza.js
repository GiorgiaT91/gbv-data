// Dati dell'indagine Istat sulla sicurezza delle donne (domanda 1), letti dalle righe «prevalenza» di
// dati/istat-sicurezza-donne/dati.csv (vedi elabora.py). Usato dai riquadri 2006, 2014, 2025 e dal confronto.
import { leggiDati } from './dati.js';

const FONTE = 'istat-sicurezza-donne';

export const FORME = [
  ['fisica_o_sessuale', 'Violenza fisica o sessuale'],
  ['fisica', 'Violenza fisica'],
  ['sessuale', 'Violenza sessuale'],
];

// Le quattro forme, con lo stupro o tentato stupro (usate dai riquadri a classifica).
export const FORME_TUTTE = [...FORME, ['stupro_o_tentato', 'Stupro o tentato stupro']];

export const PERIODI = {
  nella_vita: 'Nel corso della vita',
  ultimi_5_anni: 'Negli ultimi 5 anni',
  ultimi_12_mesi: 'Negli ultimi 12 mesi',
};

// Caratteristiche delle donne: nome e gruppi nell'ordine naturale. «ordina»: nel dettaglio dal valore più alto.
export const DIMENSIONI = {
  eta: { nome: 'Età', gruppi: [['16-24', '16–24 anni'], ['25-34', '25–34 anni'], ['35-44', '35–44 anni'], ['45-54', '45–54 anni'], ['55-64', '55–64 anni'], ['65-70', '65–70 anni'], ['70-75', '70–75 anni']] },
  titolo: { nome: 'Titolo di studio', gruppi: [['elementare_nessuno', 'Elementare o nessuno'], ['media', 'Licenza media'], ['superiore', 'Diploma superiore'], ['post_secondario', 'Laurea, post-secondario']] },
  stato_civile: { nome: 'Stato civile', gruppi: [['nubile', 'Nubile'], ['coniugata', 'Coniugata'], ['separata_divorziata', 'Separata o divorziata'], ['vedova', 'Vedova']] },
  condizione: { nome: 'Condizione professionale', ordina: true, gruppi: [
    ['dirigenti', 'Dirigenti, imprenditrici, libere prof.'], ['direttive_impiegate', 'Direttive, quadri, impiegate'], ['operaie', 'Operaie'],
    ['in_proprio', 'Lavoratrici in proprio'], ['in_cerca', 'In cerca di occupazione'], ['casalinghe', 'Casalinghe'],
    ['studentesse', 'Studentesse'], ['ritirate', 'Ritirate dal lavoro'], ['altra', 'Altra condizione']] },
  limitazioni: { nome: 'Limitazioni nelle attività', gruppi: [['nessuna', 'Nessuna limitazione'], ['non_gravi', 'Limitazioni non gravi'], ['gravi', 'Limitazioni gravi'], ['non_risponde', 'Non risponde']] },
  // Solo 2025 (report del 25/11/2026, prospetto 8 e tavola 9).
  salute: { nome: 'Salute percepita', gruppi: [['bene', 'Bene o molto bene'], ['ne_bene_ne_male', 'Né bene né male'], ['male', 'Male o molto male']] },
  malattie: { nome: 'Malattie croniche', gruppi: [['si', 'Con malattie croniche'], ['no', 'Senza malattie croniche']] },
  // Solo 2025 (prospetto 3): le prime sei cittadinanze straniere residenti e le rifugiate.
  cittadinanza: { nome: 'Cittadinanza', ordina: true, gruppi: [['italiana', 'Italiane'], ['straniera', 'Straniere, tutte'], ['romania', 'Romene'],
    ['ucraina', 'Ucraine'], ['albania', 'Albanesi'], ['marocco', 'Marocchine'], ['cina', 'Cinesi'], ['filippine', 'Filippine'],
    ['altre_straniere', 'Altre cittadinanze straniere'], ['rifugiate', 'Rifugiate']] },
  ripartizione: { nome: 'Area geografica', ordina: true, gruppi: [['nord_ovest', 'Nord-ovest'], ['nord_est', 'Nord-est'], ['centro', 'Centro'], ['sud', 'Sud'], ['isole', 'Isole']] },
  // Regioni: Trentino-Alto Adige è rappresentato dalle due province autonome (come nella mappa).
  regione: { nome: 'Regione', ordina: true, gruppi: [
    ['ITC1', 'Piemonte'], ['ITC2', "Valle d'Aosta"], ['ITC3', 'Liguria'], ['ITC4', 'Lombardia'], ['ITD1', 'Bolzano'], ['ITD2', 'Trento'],
    ['ITD3', 'Veneto'], ['ITD4', 'Friuli-Venezia Giulia'], ['ITD5', 'Emilia-Romagna'], ['ITE1', 'Toscana'], ['ITE2', 'Umbria'],
    ['ITE3', 'Marche'], ['ITE4', 'Lazio'], ['ITF1', 'Abruzzo'], ['ITF2', 'Molise'], ['ITF3', 'Campania'], ['ITF4', 'Puglia'],
    ['ITF5', 'Basilicata'], ['ITF6', 'Calabria'], ['ITG1', 'Sicilia'], ['ITG2', 'Sardegna']] },
};

let indice;
function cerca(anno, popolazione, periodo, forma, autore, dimensione, gruppo) {
  if (!indice) {
    indice = new Map();
    for (const r of leggiDati(FONTE)) {
      if (r.indicatore !== 'prevalenza') continue;
      indice.set([r.anno, r.popolazione, r.periodo, r.forma, r.autore, r.dimensione, r.gruppo].join('#'), r);
    }
  }
  return indice.get([anno, popolazione, periodo, forma, autore, dimensione, gruppo].join('#'));
}

// Valore che deve esserci: se manca, la costruzione del sito si ferma.
export function prev(anno, popolazione, periodo, forma, { autore = 'qualsiasi', dimensione = 'totale', gruppo = 'totale' } = {}) {
  const r = cerca(anno, popolazione, periodo, forma, autore, dimensione, gruppo);
  if (!r || Number.isNaN(r.valore)) {
    throw new Error(`Dato mancante in dati/${FONTE}/dati.csv: ${[anno, popolazione, periodo, forma, autore, dimensione, gruppo].join(' · ')}`);
  }
  return r.valore;
}

// Come prev(), ma con l'avvertenza di Istat (errore campionario oltre il 35%) e undefined se il valore non c'è.
export function cella(anno, popolazione, periodo, forma, dimensione, gruppo, autore = 'qualsiasi') {
  const r = cerca(anno, popolazione, periodo, forma, autore, dimensione, gruppo);
  return r ? { v: r.valore, a: r.avvertenza === 'errore_oltre_35' } : undefined;
}

// Dati del quadro delle differenze: periodo → { totale, dimensioni: dim → [{ g, nome, fisica_o_sessuale: {v,a}, … }] }
export function datiQuadro(anno, popolazione, periodi, dimensioni) {
  const out = {};
  for (const p of periodi) {
    const totale = Object.fromEntries(FORME.map(([f]) => [f, prev(anno, popolazione, p, f)]));
    const dims = {};
    for (const d of dimensioni) {
      dims[d] = DIMENSIONI[d].gruppi.map(([g, nome]) => {
        const riga = { g, nome };
        for (const [f] of FORME) riga[f] = cella(anno, popolazione, p, f, d, g);
        return riga;
      }).filter((riga) => FORME.some(([f]) => riga[f]));
      if (!dims[d].length) throw new Error(`Nessun dato per ${anno} ${popolazione} ${p} ${d}`);
    }
    out[p] = { totale, dimensioni: dims };
  }
  return out;
}

// Distanza fra il gruppo più alto e il più basso, con i loro nomi.
export function distanza(righe, forma) {
  const r = righe.filter((x) => x[forma]);
  if (!r.length) return undefined;
  let alto = r[0], basso = r[0];
  for (const x of r) {
    if (x[forma].v > alto[forma].v) alto = x;
    if (x[forma].v < basso[forma].v) basso = x;
  }
  return { punti: alto[forma].v - basso[forma].v, alto: alto.nome, basso: basso.nome };
}

// Gradino della scala (soglie in punti: meno di 5, 5-10, 10-20, 20-30, 30 e più), come negli stereotipi.
export const gradino = (punti) => (punti < 5 ? 1 : punti < 10 ? 2 : punti < 20 ? 3 : punti < 30 ? 4 : 5);

export const virgola = (n, decimali = 1) => n.toLocaleString('it-IT', { minimumFractionDigits: decimali, maximumFractionDigits: decimali });
export const perc = (n) => `${virgola(n)}%`;
