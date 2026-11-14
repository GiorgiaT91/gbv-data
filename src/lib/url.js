// Costruisce un indirizzo interno tenendo conto della sottocartella /gbv-data/ di GitHub Pages.
export function url(percorso = '') {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return `${base}/${percorso.replace(/^\//, '')}`;
}
