// Lettura dei dati e dei testi al momento della costruzione del sito.
import fs from 'node:fs';
import path from 'node:path';
import { parse } from 'yaml';

const radice = process.cwd();

function leggiTesto(...parti) {
  return fs.readFileSync(path.join(radice, ...parti), 'utf8').replace(/^﻿/, '');
}

// CSV semplice, con campi fra virgolette.
function analizzaCsv(testo) {
  const righe = [];
  let campo = '';
  let riga = [];
  let virgolette = false;
  for (let i = 0; i < testo.length; i++) {
    const c = testo[i];
    if (virgolette) {
      if (c === '"' && testo[i + 1] === '"') { campo += '"'; i++; }
      else if (c === '"') virgolette = false;
      else campo += c;
    } else if (c === '"') virgolette = true;
    else if (c === ',') { riga.push(campo); campo = ''; }
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && testo[i + 1] === '\n') i++;
      riga.push(campo); campo = '';
      if (riga.some((v) => v !== '')) righe.push(riga);
      riga = [];
    } else campo += c;
  }
  if (campo !== '' || riga.length) { riga.push(campo); righe.push(riga); }
  const [intestazione, ...corpo] = righe;
  return corpo.map((r) => Object.fromEntries(intestazione.map((k, j) => [k.trim(), (r[j] ?? '').trim()])));
}

const cache = new Map();

export function leggiDati(fonte) {
  if (!cache.has(fonte)) {
    const righe = analizzaCsv(leggiTesto('dati', fonte, 'dati.csv'));
    cache.set(fonte, righe.map((r) => ({ ...r, valore: Number(r.valore) })));
  }
  return cache.get(fonte);
}

// Restituisce il valore della riga che corrisponde a tutti i campi del filtro,
// oppure undefined se la riga non c'è (per esempio un dato non ancora pubblicato).
export function valore(fonte, filtro) {
  const riga = leggiDati(fonte).find((r) =>
    Object.entries(filtro).every(([k, v]) => String(r[k]) === String(v)),
  );
  return riga?.valore;
}

// Come valore(), ma ferma la costruzione del sito se il dato manca:
// serve per i numeri che devono esserci sempre.
export function richiesto(fonte, filtro) {
  const v = valore(fonte, filtro);
  if (v === undefined || Number.isNaN(v)) {
    throw new Error(`Dato mancante in dati/${fonte}/dati.csv: ${JSON.stringify(filtro)}`);
  }
  return v;
}

export function scheda(fonte) {
  return parse(leggiTesto('dati', fonte, 'scheda.yaml'));
}

export function contenuto(...parti) {
  return parse(leggiTesto('contenuti', ...parti));
}

export function formatta(n) {
  return new Intl.NumberFormat('it-IT').format(n);
}
