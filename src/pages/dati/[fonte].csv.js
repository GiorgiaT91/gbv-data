// Copia nel sito pubblicato il file dati/<fonte>/dati.csv di ogni fonte pronta,
// all'indirizzo /dati/<fonte>.csv. Il file resta identico all'originale (UTF-8 con BOM).
import fs from 'node:fs';
import path from 'node:path';
import { fontiPronte } from '../../lib/registro.js';

export function getStaticPaths() {
  return fontiPronte().map((f) => ({ params: { fonte: f.id } }));
}

export function GET({ params }) {
  const file = fs.readFileSync(path.join(process.cwd(), 'dati', params.fonte, 'dati.csv'));
  return new Response(file, { headers: { 'Content-Type': 'text/csv; charset=utf-8' } });
}
