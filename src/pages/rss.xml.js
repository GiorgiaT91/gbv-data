// Feed RSS di "Cosa è cambiato", costruito da contenuti/cambiamenti.yaml.
import { contenuto } from '../lib/dati.js';
import { dataIso } from '../lib/registro.js';
import { url } from '../lib/url.js';

const xml = (s = '') => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

export function GET() {
  const assoluto = (p) => new URL(url(p), import.meta.env.SITE).href;
  const voci = contenuto('cambiamenti.yaml')
    .map((v) => ({ ...v, iso: dataIso(v.data) }))
    .sort((a, b) => b.iso.localeCompare(a.iso));
  const elementi = voci.map((v) => {
    const link = assoluto(v.indirizzo ?? '/cosa-e-cambiato/');
    return `    <item>
      <title>${xml(v.titolo)}</title>
      <link>${xml(link)}</link>
      <guid isPermaLink="false">gbv-data-${v.iso}-${xml(v.titolo)}</guid>
      <pubDate>${new Date(`${v.iso}T12:00:00Z`).toUTCString()}</pubDate>
      ${v.testo ? `<description>${xml(v.testo)}</description>` : ''}
    </item>`;
  }).join('\n');
  const corpo = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>GBV-Data · Cosa è cambiato</title>
    <link>${xml(assoluto('/cosa-e-cambiato/'))}</link>
    <description>Gli aggiornamenti di GBV-Data: dati sulla violenza di genere e sui femminicidi in Italia.</description>
    <language>it</language>
${elementi}
  </channel>
</rss>
`;
  return new Response(corpo, { headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' } });
}
