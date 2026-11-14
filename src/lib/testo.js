// Formattazione minima dei testi scritti nei file .yaml:
// **parola** diventa grassetto. Tutto il resto resta testo semplice.
export function fmt(testo = '') {
  const sicuro = String(testo)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
  return sicuro.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
}
