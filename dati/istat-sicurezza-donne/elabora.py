"""Indagine Istat sulla sicurezza delle donne: ricava dati.csv per la domanda 1.

Uso:  python elabora.py   (scrive dati.csv, UTF-8 con BOM)

Fonti:
- 2025, primi risultati (21/11/2025): solo donne italiane. Prospetti 1, 3 e 5 del PDF trascritti qui sotto;
  tavola 4 dell'allegato Excel (Allegato-tavole-statistiche.xlsx) letta dal file.
- 2014 e 2006: prospetto 8 del report 2014 (Violenze_contro_le_donne.pdf), tutte le donne di 16-70 anni.

Attenzione alle popolazioni: "nella vita" = italiane 16-75 anni (2025);
"ultimi 5 anni" = donne 16-70 anni (2006 e 2014 tutte; 2014 e 2025 solo italiane, prospetto 5).
Le due serie degli ultimi 5 anni NON vanno unite in una sola linea.
"""
import csv
from pathlib import Path

import openpyxl

QUI = Path(__file__).parent
righe = []
def aggiungi(anno, periodo, indicatore, categoria, valore, unita, nota):
    righe.append([anno, periodo, 'Italia', indicatore, categoria, valore, unita, nota])

P1 = 'report 2025, prospetto 1; italiane 16-75 anni'
# Nella vita (dai 16 anni), 2025, % sulle donne italiane 16-75 anni (totale) o con partner/ex (coppia)
for cat, v in [('fisica_o_sessuale', 31.9), ('fisica', 18.8), ('sessuale', 23.4), ('stupro_o_tentato', 5.7), ('stalking', 15.5)]:
    aggiungi(2025, 'nella_vita', 'violenza', cat, v, 'percentuale', P1 + '; colonna Totale')
aggiungi(2025, 'nella_vita', 'violenza', 'fisica_o_sessuale_vittime', 6393143, 'persone', P1 + '; colonna Totale, valore assoluto')
for cat, v in [('fisica_o_sessuale', 12.6), ('psicologica', 17.9), ('economica', 6.6)]:
    aggiungi(2025, 'nella_vita', 'violenza_da_partner_o_ex', cat, v, 'percentuale', P1 + '; % sulle donne con partner attuale o ex')
aggiungi(2025, 'nella_vita', 'violenza_da_non_partner', 'fisica_o_sessuale', 26.5, 'percentuale', P1)
# Denuncia, nella vita (report 2025, pagina 4)
for cat, v in [('qualsiasi_autore', 13.3), ('ex_partner', 19.1), ('partner_attuale', 3.8)]:
    aggiungi(2025, 'nella_vita', 'hanno_denunciato', cat, v, 'percentuale', 'report 2025, pagina 4; % sulle vittime')

# Ultimi 5 anni, violenza fisica o sessuale, donne 16-70
P8 = 'report 2014, prospetto 8; tutte le donne 16-70 anni'
aggiungi(2006, 'ultimi_5_anni', 'violenza_tutte', 'fisica_o_sessuale', 13.3, 'percentuale', P8)
aggiungi(2014, 'ultimi_5_anni', 'violenza_tutte', 'fisica_o_sessuale', 11.3, 'percentuale', P8)
P5 = 'report 2025, prospetto 5; italiane 16-70 anni'
ETA = {'16-24': (28.4, 37.6), '25-34': (18.6, 18.2), '35-44': (10.1, 9.5), '45-54': (7.9, 5.4), '55-64': (5.3, 3.4), '65-70': (1.9, 1.6)}
for anno, k in [(2014, 0), (2025, 1)]:
    aggiungi(anno, 'ultimi_5_anni', 'violenza_italiane', 'fisica_o_sessuale', (11.2, 11.0)[k], 'percentuale', P5 + '; riga Totale')
    aggiungi(anno, 'ultimi_5_anni', 'violenza_italiane', 'fisica', (6.8, 6.1)[k], 'percentuale', P5 + '; riga Totale')
    aggiungi(anno, 'ultimi_5_anni', 'violenza_italiane', 'sessuale', (6.4, 7.3)[k], 'percentuale', P5 + '; riga Totale')
    for eta, v in ETA.items():
        aggiungi(anno, 'ultimi_5_anni', 'violenza_italiane', f'fisica_o_sessuale|{eta}', v[k], 'percentuale', P5)
    aggiungi(anno, 'ultimi_5_anni', 'violenza_italiane', 'sessuale|16-24', (17.7, 30.8)[k], 'percentuale', P5)

# Tavola 4 dell'allegato: dopo la violenza (ultimi 5 anni), 2014 e 2025
ws = openpyxl.load_workbook(QUI / 'originali' / '2025' / 'Allegato-tavole-statistiche.xlsx', data_only=True)['Tavola 4']
VOCI = {'Si rivolgono ai centri antiviolenza': 'centro_antiviolenza', 'Ha denunciato': 'denuncia',
        'Considera l\'episodio che ha subito: Un reato': 'considera_reato', 'Non ha parlato con nessuno': 'non_ne_ha_parlato'}
for r in ws.iter_rows(min_row=7, max_row=17, values_only=True):
    nome = str(r[0] or '').strip()
    codice = next((c for k, c in VOCI.items() if nome.startswith(k)), None)
    if not codice:
        continue
    for autore, (c14, c25) in [('partner_o_ex', (1, 2)), ('non_partner', (3, 4))]:
        for anno, col in [(2014, c14), (2025, c25)]:
            v = r[col]
            nota = 'allegato 2025, tavola 4; % sulle vittime degli ultimi 5 anni, italiane 16-70'
            if isinstance(v, str):  # es. "0,8*": errore campionario superiore al 35%
                nota += f'; valore «{v}», errore campionario oltre il 35%'
                v = float(v.replace('*', '').replace(',', '.'))
            aggiungi(anno, 'ultimi_5_anni', f'dopo_la_violenza_{autore}', codice, round(v, 1), 'percentuale', nota)

with open(QUI / 'dati.csv', 'w', encoding='utf-8-sig', newline='') as fh:
    w = csv.writer(fh, lineterminator='\n')
    w.writerow(['anno', 'periodo', 'territorio', 'indicatore', 'categoria', 'valore', 'unita', 'nota'])
    w.writerows(righe)
print(f'{len(righe)} righe scritte in dati.csv')
