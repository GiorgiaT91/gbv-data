// Elenchi di domande e fonti, letti da contenuti/domande.yaml e contenuti/fonti.yaml.
import { contenuto, scheda } from './dati.js';

export function domande() {
  return contenuto('domande.yaml');
}

export function domanda(id) {
  return domande().find((d) => d.id === Number(id));
}

// Tutte le fonti; per quelle pronte nome, ente e il resto vengono dalla scheda.
export function fonti() {
  return contenuto('fonti.yaml').map((f) => (f.pronta ? { ...f, ...scheda(f.id) } : f));
}

export function fontiPronte() {
  return fonti().filter((f) => f.pronta);
}

export function fonte(id) {
  return fonti().find((f) => f.id === id);
}

// Date nei file .yaml: AAAA-MM-GG (anche come oggetto Date) → "25 novembre 2025".
export function dataIso(d) {
  if (d instanceof Date) return d.toISOString().slice(0, 10);
  return /^\d{4}-\d{2}-\d{2}$/.test(String(d)) ? String(d) : null;
}

export function dataEstesa(d) {
  const iso = dataIso(d);
  if (!iso) return d === 'DA VERIFICARE' ? 'Da verificare' : d;
  return new Date(`${iso}T12:00:00Z`).toLocaleDateString('it-IT', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Europe/Rome' });
}

// Mesi interi trascorsi fra una data e il giorno in cui il sito viene costruito.
export function mesiFa(d, oggi = new Date()) {
  const iso = dataIso(d);
  if (!iso) return null;
  const [a, m, g] = iso.split('-').map(Number);
  let mesi = (oggi.getFullYear() - a) * 12 + (oggi.getMonth() + 1 - m);
  if (oggi.getDate() < g) mesi -= 1;
  return Math.max(0, mesi);
}
