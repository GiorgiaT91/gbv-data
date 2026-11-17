"""Numero 1522: ricava dati.csv dalle tavole Istat-DPO (revisione del 19/10/2026).

Uso:  python elabora.py
Legge originali/2025/Tavole_ITA_REV-19ottobre2026.xlsx e scrive dati.csv (UTF-8 con BOM).
Si salvano solo valori assoluti, presi o sommati dalle tavole: le percentuali le calcola il sito.

Periodi di registrazione (note.md):
  gen2023-mar2025  piattaforma 2022, vecchio gestore  (tavole 1, 11-15: colonne 2023 T1 ... 2025 T1)
  apr-giu2025      passaggio di gestore              (2025 T2)
  lug-dic2025      nuovo gestore                     (2025 T3 + T4)
"""
import csv
import datetime as dt
from pathlib import Path

import openpyxl

QUI = Path(__file__).parent
FILE = QUI / 'originali' / '2025' / 'Tavole_ITA_REV-19ottobre2026.xlsx'
wb = openpyxl.load_workbook(FILE, data_only=True)

righe = []
def aggiungi(anno, periodo, indicatore, categoria, valore, unita='persone', nota=''):
    righe.append([anno, periodo, 'Italia', indicatore, categoria, valore, unita, nota])

def num(v):
    return v if isinstance(v, (int, float)) else 0

# --- Tavola 5: chiamate valide da utenti, giorno per giorno, 2018-2025 ---------------------
ws = wb['Tavola 5']
anni = [c for c in next(ws.iter_rows(min_row=3, max_row=3, values_only=True))[1:] if c]
mesi = {a: [0] * 12 for a in anni}
for r in ws.iter_rows(min_row=4, values_only=True):
    giorno = r[0]
    if isinstance(giorno, dt.datetime):
        m = giorno.month
    elif isinstance(giorno, str) and '29' in giorno and 'feb' in giorno:
        m = 2  # la riga "29 -feb" va sommata a febbraio (2020, 2024)
    else:
        continue
    for a, v in zip(anni, r[1:]):
        mesi[a][m - 1] += num(v)
for a in anni:
    for m, v in enumerate(mesi[a], 1):
        aggiungi(a, f'mese-{m:02d}', 'chiamate_valide', 'totale', v, 'chiamate', 'tavola 5')
    aggiungi(a, 'anno', 'chiamate_valide', 'totale', sum(mesi[a]), 'chiamate', 'tavola 5, somma dei giorni')

# --- Tavole trimestrali 2023-2025: colonne B..M = 2023 T1..T4, 2024 T1..T4, 2025 T1..T4 -----
PERIODI = {
    'gen2023-mar2025': range(0, 9),
    'apr-giu2025': range(9, 10),
    'lug-dic2025': range(10, 12),
}

def leggi(nome_foglio, riga_inizio, riga_fine):
    """Restituisce {etichetta: [12 valori]} per le righe indicate."""
    out = {}
    for r in wb[nome_foglio].iter_rows(min_row=riga_inizio, max_row=riga_fine, values_only=True):
        if r[0]:
            out[str(r[0]).strip()] = [num(v) for v in r[1:13]]
    return out

def per_periodo(indicatore, tavola, voci, nota, unita='persone', periodi=PERIODI):
    for periodo, colonne in periodi.items():
        for etichetta, codice in voci.items():
            valori = tavola[etichetta]
            aggiungi(2025, periodo, indicatore, codice, sum(valori[i] for i in colonne), unita, nota)

# Tavola 1: motivi delle chiamate, chiamate valide, vittime
t1 = leggi('Tavola 1', 5, 23)
per_periodo('chiamate_per_motivo', t1, {
    'Richiesta di aiuto vittima di violenza': 'aiuto_vittima_violenza',
    'Informazioni sul servizio 1522': 'informazioni_servizio',
    'Totale chiamate valide': 'totale',
}, 'tavola 1', 'chiamate', {**PERIODI, 'gen-mar2025': range(8, 9)})  # gen-mar 2025: ultimo trimestre del vecchio gestore

# Vittime usate nelle tavole 11-15: fino al I trim 2025 "Totale vittime" (riga 21),
# dal II trim 2025 "Interlocutore è vittima = Sì" (riga 22, nota c), come fanno le tavole 11-15.
vittime = t1['Totale Vittime (b)'][:9] + t1['Totale Vittime (Interlocutore è vittima=Sì) (c)'][9:]
for periodo, colonne in PERIODI.items():
    aggiungi(2025, periodo, 'vittime', 'totale', sum(vittime[i] for i in colonne), 'persone',
             'tavola 1; dal II trim 2025 interlocutore è vittima = sì')

# Tavola 11: violenza principale
t11 = leggi('Tavola 11 e 11bis', 4, 22)
per_periodo('violenza_principale', t11, {
    'Violenza fisica': 'fisica', 'Violenza psicologica': 'psicologica', 'Violenza economica': 'economica',
    'Violenza sessuale': 'sessuale', 'Violenza sessuale minori': 'sessuale_minori',
    'Atti persecutori': 'atti_persecutori', 'Minacce': 'minacce', 'ND': 'nd', 'Totale': 'totale',
}, 'tavola 11')

# Tavola 12: da quanto tempo
t12 = leggi('Tavola 12', 4, 9)
per_periodo('frequenza', t12, {
    'Ripetuti episodi, la violenza durava da anni': 'da_anni',
    'Ripetuti episodi, la violenza durava da mesi': 'da_mesi',
    'Pochi episodi': 'pochi_episodi', 'Un unico episodio': 'unico_episodio',
    'Non risponde': 'non_risponde', 'N.D.': 'nd',
}, 'tavola 12')

# Tavola 13: luogo
t13 = leggi('Tavola 13', 4, 14)
per_periodo('luogo', t13, {
    'La propria casa': 'casa', 'La strada': 'strada', 'Online': 'online',
    'Non Risponde': 'non_risponde', 'N.D.': 'nd', 'Totale': 'totale',
}, 'tavola 13')

# Tavola 14: denuncia
t14 = leggi('Tavola 14', 4, 9)
per_periodo('denuncia', t14, {
    'Vittime che denunciano': 'denunciano', 'Vittime che non denunciano': 'non_denunciano',
    'Vittime che denunciano e poi ritirano la denuncia': 'denunciano_e_ritirano',
    'Non risponde': 'non_risponde', 'N.D.': 'nd', 'Totale': 'totale',
}, 'tavola 14')

# Tavola 15: autore (più risposte possibili, soprattutto dal 2025)
t15 = leggi('Tavola 15', 4, 28)
per_periodo('autore', t15, {
    'Marito / Moglie': 'marito', 'Ex Marito / Ex Moglie': 'ex_marito', 'Convivente': 'convivente',
    'Ex Convivente': 'ex_convivente', 'Partner': 'partner', 'Ex Partner': 'ex_partner',
    'Padre / Madre': 'genitore', 'Figlio / Figlia': 'figlio',
}, 'tavola 15; più autori possibili')

with open(QUI / 'dati.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['anno', 'periodo', 'territorio', 'indicatore', 'categoria', 'valore', 'unita', 'nota'])
    w.writerows(righe)
print(f'{len(righe)} righe scritte in dati.csv')
