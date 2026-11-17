"""Stereotipi di genere, adulti 18-74 anni: ricava dati.csv dalle rilevazioni Istat 2018 e 2023.

Uso:  python elabora.py   (scrive dati.csv, UTF-8 con BOM)

2018: dataset IstatData in SDMX-CSV (originali/2018/*RUOLIGEN_n*.csv); codici in codici.csv.
      "D'accordo" = molto + abbastanza d'accordo; "accettabile" = sempre + in certe circostanze.
      Le somme coincidono con le tavole dell'appendice (controllato il 16/11/2026).
2023: tavole per età (originali/2023/Tavole-stereotipi-per-eta-2023.xlsx, ottobre 2024);
      per sesso solo il prospetto 1 dei primi risultati provvisori (STAT_TODAY_Stereotipi.pdf, 22/11/2023).

Colonna "categoria": codice dell'affermazione (codici.csv), seguito facoltativamente da "|gruppo":
  |M, |F (sesso), |Y18-29 ... (età), |NP, |LSE, |USE_IF, |CLF_ML (titolo di studio). Senza gruppo = totale.
"""
import csv
import glob
from pathlib import Path

import openpyxl

QUI = Path(__file__).parent
righe = []
def aggiungi(anno, indicatore, categoria, valore, nota):
    righe.append([anno, 'anno', 'Italia', indicatore, categoria, round(valore, 1), 'percentuale', nota])

def sdmx(n):
    f = glob.glob(str(QUI / 'originali' / '2018' / f'*RUOLIGEN_{n},*.csv'))[0]
    return [r for r in csv.DictReader(open(f, encoding='utf-8-sig')) if r['REF_AREA'] == 'IT']

def gruppo(r, campo_extra=None):
    if r['SEX'] != 'T':
        return f"|{r['SEX']}" if r['AGE'] == 'TOTAL' and r['EDU_LEV_HIGHEST'] == 'ALL' else None
    if r['AGE'] != 'TOTAL':
        return f"|{r['AGE']}"
    if r['EDU_LEV_HIGHEST'] != 'ALL':
        return f"|{r['EDU_LEV_HIGHEST']}"
    return ''

# ---------------------------------------------------------------- 2018
# Almeno uno stereotipo: età (1) e titolo di studio (2)
visti = set()
for n in (1, 2):
    for r in sdmx(n):
        g = gruppo(r)
        chiave = (r['STEREOT_GENDROLEPARTNER'], g)
        if g is None or chiave in visti:
            continue
        visti.add(chiave)
        aggiungi(2018, 'almeno_uno', r['STEREOT_GENDROLEPARTNER'] + g, float(r['OBS_VALUE']), f'IstatData RUOLIGEN_{n}')

def somma(n, indicatore, campo, gradi):
    acc = {}
    for r in sdmx(n):
        g = gruppo(r)
        if g is None or r[campo] not in gradi:
            continue
        k = r['STEREOT_GENDROLEPARTNER'] + g
        acc[k] = acc.get(k, 0) + float(r['OBS_VALUE'])
    for k, v in acc.items():
        aggiungi(2018, indicatore, k, v, f'IstatData RUOLIGEN_{n}, somma di {" + ".join(gradi)}')

somma(4, 'accordo', 'DEGREE_AGREEMENT', ('STRAGR', 'SOMAGR'))       # ruoli, per sesso ed età
somma(7, 'accordo', 'DEGREE_AGREEMENT', ('STRAGR', 'SOMAGR'))       # violenza sessuale
somma(10, 'accettabile', 'DEGREE_ACCEPTABILITY', ('ALWACC', 'ACUNDCIR'))  # coppia

# Percezione della diffusione (13), cause (16), consigli (19): totale e per sesso
for r in sdmx(13):
    g = gruppo(r)
    if g in ('', '|M', '|F') and r['HOW_COMMON'] not in ('ALL',):
        aggiungi(2018, 'diffusione', r['HOW_COMMON'] + g, float(r['OBS_VALUE']), 'IstatData RUOLIGEN_13')
for r in sdmx(16):
    g = gruppo(r)
    if g in ('', '|M', '|F') and r['POSSIBLE_CAUSES'] != 'ALL':
        aggiungi(2018, 'cause', r['POSSIBLE_CAUSES'] + g, float(r['OBS_VALUE']), 'IstatData RUOLIGEN_16')
for r in sdmx(19):
    g = gruppo(r)
    if g == '' and r['ADVICE'] != 'TOT':
        aggiungi(2018, 'consigli', r['ADVICE'], float(r['OBS_VALUE']), 'IstatData RUOLIGEN_19; più risposte')

# ---------------------------------------------------------------- 2023
wb = openpyxl.load_workbook(QUI / 'originali' / '2023' / 'Tavole-stereotipi-per-eta-2023.xlsx', data_only=True)
ETA = {'18-29': 'Y18-29', '30-44': 'Y30-44', '45-59': 'Y45-59', '60-74': 'Y60-74', 'Totale': None}

def numero(v):
    if isinstance(v, (int, float)):
        return float(v), ''
    testo = str(v).strip()           # es. "3,1 (a)" nella tavola 2
    return float(testo.split()[0].replace(',', '.')), f'valore scritto come «{testo}» nella tavola'

# Tavola 1: almeno uno stereotipo, per età
codici_t1 = ['TRGENROL', 'ONEBEHP', 'STEVIOSEX']
for r in wb['Tav.1'].iter_rows(min_row=5, max_row=9, values_only=True):
    eta = str(r[0]).strip()
    if eta in ETA:
        for codice, v in zip(codici_t1, r[1:4]):
            val, nota = numero(v)
            aggiungi(2023, 'almeno_uno', codice + (f'|{ETA[eta]}' if ETA[eta] else ''), val, ('tavola 1; ' + nota).strip('; '))

# Tavole 2-4: una affermazione per blocco; la prima colonna numerica è "d'accordo" o "accettabile"
AFFERMAZIONI = {
    'IN CONDIZIONI DI SCARSITÀ': 'PRIOMEN', 'PROVVEDERE ALLE NECESSITÀ': 'MPRFAM', 'PRENDERE LE DECISIONI': 'MTAKEDE',
    'FACCENDE DOMESTICHE': 'MLESHOUS', 'AVERE SUCCESSO NEL LAVORO': 'MISUCWOR', 'PER ESSERE COMPLETA': 'WCOMPFIG',
    'BUONA MOGLIE': 'GOODWIFE', 'MATERIE SCIENTIFICHE': 'BOYSSTEM', 'COMPITO DELLE MADRI': 'MOTHCARE',
    'SCHIAFFEGGIA': 'SLGIROC', 'CI SCAPPA UNO SCHIAFFO': 'NSMOCC', 'CONTROLLA ABITUALMENTE': 'HABCONTR',
    'MODO DI VESTIRE': 'WPROVSEX', 'RIESCONO AD EVITARLO': 'WABLAVO', 'DONNE SERIE': 'SEWNRAP',
    'OBBLIGA LA MOGLIE': 'HUSFNVIO', 'DICONO NO': 'WOFSREM', 'UBRIACA': 'WSVADRE', 'ACCUSE DI VIOLENZA': 'OACVIF',
    'ACCETTA UN INVITO': 'PARTYINV',
}
for foglio, indicatore in [('Tav.2', 'accordo'), ('Tav.3', 'accettabile'), ('Tav.4', 'accordo')]:
    codice = None
    for r in wb[foglio].iter_rows(min_row=4, values_only=True):
        if r[0] and str(r[0]).strip() == 'ETÀ' and r[1]:
            codice = next((c for k, c in AFFERMAZIONI.items() if k in str(r[1]).upper()), None)
            if codice is None:
                raise SystemExit(f'Affermazione non riconosciuta: {r[1]}')
            continue
        eta = str(r[0]).strip() if r[0] else ''
        if codice and eta in ETA and r[1] is not None:
            val, nota = numero(r[1])
            aggiungi(2023, indicatore, codice + (f'|{ETA[eta]}' if ETA[eta] else ''), val, (f'tavola {foglio[-1]}; ' + nota).strip('; '))

# Per sesso: prospetto 1 dei primi risultati 2023 (dati provvisori), trascritto dal PDF
PROSPETTO_1 = {  # codice: (maschi, femmine)
    'MLESHOUS': (24.6, 18.3), 'WCOMPFIG': (24.2, 17.7), 'MISUCWOR': (20.0, 20.7), 'MOTHCARE': (19.6, 20.7),
    'MPRFAM': (23.0, 11.5), 'BOYSSTEM': (13.2, 9.8), 'PRIOMEN': (10.5, 6.0), 'GOODWIFE': (8.1, 4.9), 'MTAKEDE': (8.7, 3.9),
}
for codice, (m, f) in PROSPETTO_1.items():
    aggiungi(2023, 'accordo', f'{codice}|M', m, 'primi risultati 22/11/2023, prospetto 1, dati provvisori')
    aggiungi(2023, 'accordo', f'{codice}|F', f, 'primi risultati 22/11/2023, prospetto 1, dati provvisori')

with open(QUI / 'dati.csv', 'w', encoding='utf-8-sig', newline='') as fh:
    w = csv.writer(fh, lineterminator='\n')
    w.writerow(['anno', 'periodo', 'territorio', 'indicatore', 'categoria', 'valore', 'unita', 'nota'])
    w.writerows(righe)
print(f'{len(righe)} righe scritte in dati.csv')
