"""Centri antiviolenza: ricava dati.csv dalle tavole Istat-DPO, anno 2024 (pubblicate il 10/03/2026).

Uso:  python elabora.py
Legge originali/2024/ e scrive dati.csv (UTF-8 con BOM). Le percentuali sulle donne le calcola il sito,
tranne la durata della violenza (tavola 10 utenza), che Istat pubblica solo in percentuale.

Fuori, per decisione del 16/11/2026 (note.md): autori, denunce, imputazioni, condanne e
provvedimenti (tavole utenza 13, 15-23) e la tavola utenza 9.
"""
import csv
from pathlib import Path

import openpyxl

QUI = Path(__file__).parent
ORIG = QUI / 'originali' / '2024'
centri = openpyxl.load_workbook(ORIG / 'Tavole-appendice-Centri-Antiviolenza_2024.xlsx', data_only=True)
utenza = openpyxl.load_workbook(ORIG / 'Tavole_Appendice__UtenzaCav_2024.xlsx', data_only=True)

righe = []
def aggiungi(anno, periodo, territorio, indicatore, categoria, valore, unita, nota=''):
    righe.append([anno, periodo, territorio, indicatore, categoria, valore, unita, nota])

NOMI = {"Valle D'Aosta": "Valle d'Aosta", 'Trentino Alto Adige': 'Trentino-Alto Adige'}
SALTA = {'Bolzano-Bozen', 'Trento'}  # si usa la regione, non le due province

# --- Centri: tavola 1 (attivi) e tavola 2 (rispondenti), con tassi per 10 mila donne ----------
for foglio, indicatore in [('Tavola 1', 'centri_attivi'), ('Tavola 2', 'centri_rispondenti')]:
    for r in centri[foglio].iter_rows(min_row=5, values_only=True):
        if not r[0] or str(r[0]).startswith('Fonte') or r[0] in SALTA:
            continue
        luogo = NOMI.get(r[0], r[0])
        aggiungi(2024, 'anno', luogo, indicatore, 'totale', r[1], 'centri', f'tavola {foglio[-1]} centri')
        aggiungi(2024, 'anno', luogo, indicatore, 'per_10mila_donne', round(r[2], 4), 'tasso', f'tavola {foglio[-1]} centri')

# --- Personale: tavola 27 (Italia) -------------------------------------------------------------
for r in centri['Tavola 27'].iter_rows(min_row=3, values_only=True):
    if r[0] == 'Italia':
        aggiungi(2024, 'anno', 'Italia', 'personale', 'totale', r[1], 'persone', 'tavola 27 centri')
        aggiungi(2024, 'anno', 'Italia', 'personale', 'solo_volontario', r[3], 'persone', 'tavola 27 centri')

# --- Donne in percorso -------------------------------------------------------------------------
for r in utenza['Tavola 1'].iter_rows(min_row=5, values_only=True):
    if r[0] == 'Totale':
        aggiungi(2024, 'anno', 'Italia', 'donne_in_percorso', 'totale', r[1], 'persone', 'tavola 1 utenza')
    elif r[0] == 2024:
        aggiungi(2024, 'anno', 'Italia', 'donne_in_percorso', 'iniziato_nel_2024', r[1], 'persone', 'tavola 1 utenza')
for r in utenza['Tavola 2'].iter_rows(min_row=16, max_row=16, values_only=True):
    aggiungi(2024, 'anno', 'Italia', 'donne_in_percorso', 'in_emergenza', r[2], 'persone', 'tavola 2 utenza, riga Totale')

# Tavola 3: a chi si erano rivolte prima del centro (Italia, valori assoluti, più risposte)
t3 = utenza['Tavola 3']
intest = [c for c in next(t3.iter_rows(min_row=3, max_row=3, values_only=True))]
PRIMA = {
    'Parenti, amici, conoscenti, ecc.': 'parenti_amici', 'Forze dell’Ordine': 'forze_ordine',
    'Servizi sociali territoriali': 'servizi_sociali', 'Pronto Soccorso/Ospedale (incluso il ricovero)': 'pronto_soccorso',
    'Avvocato': 'avvocato', 'Psicologo o psichiatra': 'psicologo', '1522': 'numero_1522', 'Altri Centri Antiviolenza': 'altri_centri',
}
riga_italia = next(r for r in t3.iter_rows(min_row=5, max_row=10, values_only=True) if r[0] == 'Italia')
for j, nome in enumerate(intest):
    chiave = str(nome).strip() if nome is not None else ''
    if chiave in PRIMA:
        aggiungi(2024, 'anno', 'Italia', 'rivolta_prima_a', PRIMA[chiave], riga_italia[j], 'persone', 'tavola 3 utenza; più risposte')

# Tavola 8: violenze subite (riga Totale, valori assoluti, più risposte)
t8 = utenza['Tavola 8']
tipi = list(next(t8.iter_rows(min_row=4, max_row=4, values_only=True)))
VIOL = ['fisica', 'minaccia', 'stupro_tentato_stupro', 'altra_violenza_sessuale', 'stalking', 'psicologica', 'economica']
totale8 = next(r for r in t8.iter_rows(min_row=6, values_only=True) if r[0] == 'Totale')
for j, codice in enumerate(VIOL, start=1):
    aggiungi(2024, 'anno', 'Italia', 'violenza_subita', codice, totale8[j], 'persone', f'tavola 8 utenza; colonna «{str(tipi[j])[:30]}»; più risposte')

# Tavola 10: durata della violenza (riga Totale, valori percentuali)
t10 = utenza['Tavola 10']
DUR = ['1_6_mesi', '6_mesi_1_anno', '1_5_anni', 'piu_5_anni', 'singolo_episodio', 'non_indicato']
totale10 = next(r for r in t10.iter_rows(min_row=7, values_only=True) if r[0] == 'Totale')
for j, codice in enumerate(DUR, start=1):
    aggiungi(2024, 'anno', 'Italia', 'durata_violenza', codice, round(totale10[j], 2), 'percentuale', 'tavola 10 utenza')

# --- Valori dal testo del report 2024 (Centri-antiviolenza_Istat-DPO_Anno-2024.pdf, pagine 1-3) --
REPORT = 'report 2024, testo'
aggiungi(2024, 'anno', 'Italia', 'donne_che_contattano', 'totale', 61370, 'persone', REPORT)
for luogo, v in [('Italia', 169), ('Nord-ovest', 241), ('Nord-est', 238), ('Sud', 72)]:
    aggiungi(2024, 'anno', luogo, 'donne_che_contattano', 'per_centro_rispondente', v, 'persone', REPORT)
aggiungi(2017, 'anno', 'Italia', 'personale', 'quota_volontario', 56.1, 'percentuale', REPORT)

# --- Serie dalle edizioni precedenti (tabella "Serie ricostruita" in note.md) --------------------
SERIE = {  # anno: (centri attivi, centri rispondenti, donne che hanno contattato)
    2017: (281, None, None), 2018: (302, 257, 49394), 2019: (340, 281, None), 2020: (350, 263, 54609),
    2021: (373, 307, 56349), 2022: (385, 349, 60751), 2023: (404, 363, 61514),
}
for anno, (att, risp, cont) in SERIE.items():
    aggiungi(anno, 'anno', 'Italia', 'centri_attivi', 'totale', att, 'centri', 'edizioni precedenti, vedi note.md')
    if risp:
        aggiungi(anno, 'anno', 'Italia', 'centri_rispondenti', 'totale', risp, 'centri', 'edizioni precedenti, vedi note.md')
    if cont:
        aggiungi(anno, 'anno', 'Italia', 'donne_che_contattano', 'totale', cont, 'persone', 'edizioni precedenti, vedi note.md')
# Donne in percorso negli stessi centri (report 2024, pagina con nota 8)
for anno, v in [(2022, 26000), (2023, 31700)]:
    aggiungi(anno, 'anno', 'Italia', 'donne_in_percorso', 'centri_costanti', v, 'persone', 'report 2024, pagina 9; valori arrotondati da Istat')
aggiungi(2024, 'anno', 'Italia', 'donne_in_percorso', 'centri_costanti', 36408 - 850, 'persone',
         'ricavato: 36.408 meno le 850 donne in centri nuovi o non rispondenti nel 2023 (report 2024, nota 8)')

with open(QUI / 'dati.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['anno', 'periodo', 'territorio', 'indicatore', 'categoria', 'valore', 'unita', 'nota'])
    w.writerows(righe)
print(f'{len(righe)} righe scritte in dati.csv')
