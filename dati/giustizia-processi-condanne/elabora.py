"""Processi e condanne: ricava dati.csv dalle tavole della pagina Istat "Il percorso giudiziario".

Uso:  python elabora.py
Legge originali/ e scrive dati.csv (UTF-8 con BOM). Solo il dato Italia.

Ogni passo conta un'unità diversa e copre anni diversi (vedi note.md):
- Procure (grafici2018.xlsx, Istat): autori indagati con richiesta di azione penale o archiviazione, 2012-2018;
  motivi dell'archiviazione e tempi, 2018.
- Tribunali (Ministero della Giustizia, DIT): procedimenti iscritti e definiti nelle sezioni dibattimentali,
  e come si sono conclusi, 2021-2023. Le righe non si sommano: uno stesso procedimento può avere più reati.
- Condanne definitive (Istat): condannati con sentenza irrevocabile per reato più grave, 2010-2018 (2018 provvisorio).
- Carcere (Ministero della Giustizia, DAP): detenuti adulti presenti, 2010-2024.
"""
import csv
from pathlib import Path

import openpyxl

QUI = Path(__file__).parent
ORIG = QUI / 'originali'
righe = []
def aggiungi(anno, indicatore, categoria, valore, unita, nota=''):
    righe.append([anno, 'anno', 'Italia', indicatore, categoria, valore, unita, nota])

def apri(nome, foglio):
    return list(openpyxl.load_workbook(ORIG / nome, data_only=True)[foglio].iter_rows(values_only=True))

def numero(x):
    return int(float(x)) if x not in (None, '') else None

# --- Procure, tavola 1: azione penale o archiviazione, 2012-2018 ---------------------------------
PROCURE = {'Stalking': 'stalking', 'Da partner o ex partner': 'stalking_partner_ex',
           'Maltrattamenti in famiglia': 'maltrattamenti', 'Violenza sessuale': 'violenze_sessuali'}
t = apri('grafici2018.xlsx', 'tavola 1')
anni = [(j, c) for j, c in enumerate(t[4]) if isinstance(c, int)]
for r in t:
    if r[0] in PROCURE:
        for j, anno in anni:
            aggiungi(anno, 'indagati_azione_penale', PROCURE[r[0]], numero(r[j]), 'persone', 'procure, tavola 1')
            aggiungi(anno, 'indagati_archiviati', PROCURE[r[0]], numero(r[j + 1]), 'persone', 'procure, tavola 1')

# --- Procure, tavola 4: motivi dell'archiviazione, 2018 -------------------------------------------
MOTIVI = [(1, 'archiviati_nel_merito'), (2, 'archiviati_improcedibilita'), (3, 'archiviati_prescrizione'), (4, 'archiviati_altri_motivi')]
for r in apri('grafici2018.xlsx', 'tavola 4'):
    if r[0] in ('Stalking', 'Maltrattamenti in famiglia', 'Violenza sessuale'):
        for j, ind in MOTIVI:
            aggiungi(2018, ind, PROCURE[r[0]], numero(r[j]) or 0, 'persone', 'procure, tavola 4')

# --- Procure, tavola 2: tempi mediani in giorni, 2018 ---------------------------------------------
for r in apri('grafici2018.xlsx', 'tavola 2'):
    if r[0] in ('Stalking', 'Maltrattamenti in famiglia', 'Violenza sessuale'):
        aggiungi(2018, 'giorni_mediani_azione_penale', PROCURE[r[0]], r[5], 'giorni', 'procure, tavola 2')
        aggiungi(2018, 'giorni_mediani_archiviazione', PROCURE[r[0]], r[8], 'giorni', 'procure, tavola 2')

# --- Tribunali: procedimenti iscritti e definiti, e come si chiudono, 2021-2023 --------------------
ARTICOLI = {'art. 572': 'maltrattamenti', 'art. 612-bis': 'stalking', 'art. 609-bis': 'violenze_sessuali',
            'art. 609-ter': 'violenza_sessuale_aggravata', 'art. 609-octies': 'violenza_sessuale_gruppo',
            'art. 612-ter': 'diffusione_immagini', 'art. 558-bis': 'matrimonio_forzato'}
F = 'Tavole-Min-Giustizia-DIT-2021_2023-Sez_DIB.xlsx'
for r in apri(F, 'Tab.1 DIB'):
    if r[0] in ARTICOLI:
        for k, anno in enumerate((2021, 2022, 2023)):
            aggiungi(anno, 'procedimenti_iscritti', ARTICOLI[r[0]], r[2 + 2 * k], 'procedimenti', 'tribunali, tab. 1')
            aggiungi(anno, 'procedimenti_definiti', ARTICOLI[r[0]], r[3 + 2 * k], 'procedimenti', 'tribunali, tab. 1')
for r in apri(F, 'Tab.2 Def DIB'):
    for inizio, anno in ((0, 2021), (7, 2022), (13, 2023)):
        if r[inizio] in ARTICOLI:
            reato = ARTICOLI[r[inizio]]
            for k, ind in enumerate(('definiti_condanna', 'definiti_assoluzione', 'definiti_altro')):
                aggiungi(anno, ind, reato, r[inizio + 2 + k], 'procedimenti', 'tribunali, tab. 2; la condanna comprende i patteggiamenti')

# --- Condannati con sentenza irrevocabile, 2010-2018 ----------------------------------------------
def condanne(nome, colonne):
    t = apri(nome, openpyxl.load_workbook(ORIG / nome, read_only=True).sheetnames[0])
    anni_r = next(r for r in t if r[0] == 'Seleziona periodo')
    tot = next(r for r in t if r[0] == 'tutte le voci')
    for reato, (da, a) in colonne.items():
        for j in range(da, a + 1):
            anno = int(str(anni_r[j])[:4])
            aggiungi(anno, 'condannati_definitivi', reato, tot[j], 'persone',
                     'condanne, dato provvisorio' if anno == 2018 else 'condanne')
condanne('Tavola_maltrattamenti_in_famiglia_2010-2018_per_pena_inflitta.xlsx', {'maltrattamenti': (2, 10)})
condanne('Tavola_stalking_2010-2018_per_pena_inflitta.xlsx', {'stalking': (2, 10)})
condanne('Tavola_violenza_sessuale_2010-2018_per_pena_inflitta.xlsx', {'violenza_sessuale_gruppo': (2, 10), 'violenze_sessuali': (11, 19)})

# --- Detenuti adulti presenti, 2010-2024 ----------------------------------------------------------
DETENUTI = {'percosse': 'percosse', 'maltrattamenti in famiglia o verso i fanciulli': 'maltrattamenti',
            'atti persecutori (stalking)': 'stalking', 'delitti di violenza sessuale': 'violenze_sessuali'}
t = apri('DETENUTI-anni-2024-fonte-DAP.xlsx', 'tavola1')
intest_anni = next(r for r in t if r[0] == 'Anno')
sessi = next(r for r in t if r[0] == 'Sesso')
colonne_tot = [(j, int(intest_anni[j - 2])) for j, s in enumerate(sessi) if s == 'totale']
dentro = False  # solo il primo blocco della tavola, i valori assoluti
for r in t:
    if r[0] and str(r[0]).startswith('numero di detenuti') and 'percentuale' not in r[0] and 'per 100' not in r[0]:
        dentro = True
    elif r[0]:
        dentro = False
    if dentro and r[1] in DETENUTI and r[2] == 'Totale':
        for j, anno in colonne_tot:
            aggiungi(anno, 'detenuti', DETENUTI[r[1]], numero(r[j]), 'persone', 'detenuti DAP')

righe.sort(key=lambda r: (r[3], r[4], r[0]))
with open(QUI / 'dati.csv', 'w', encoding='utf-8-sig', newline='') as out:
    w = csv.writer(out)
    w.writerow(['anno', 'periodo', 'territorio', 'indicatore', 'categoria', 'valore', 'unita', 'nota'])
    w.writerows(righe)
print(len(righe), 'righe')
