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
    # keep_default_na non esiste in csv: il codice "NA" (non risponde) resta testo, mai mancante
    return list(csv.DictReader(open(f, encoding='utf-8-sig')))

# Regioni (NUTS 2): Trentino-Alto Adige compare con le due province autonome, non come aggregato (ITDA)
REGIONI = {
    'ITC1': 'Piemonte', 'ITC2': "Valle d'Aosta", 'ITC3': 'Liguria', 'ITC4': 'Lombardia',
    'ITD1': 'Provincia di Bolzano', 'ITD2': 'Provincia di Trento', 'ITD3': 'Veneto', 'ITD4': 'Friuli-Venezia Giulia',
    'ITD5': 'Emilia-Romagna', 'ITE1': 'Toscana', 'ITE2': 'Umbria', 'ITE3': 'Marche', 'ITE4': 'Lazio',
    'ITF1': 'Abruzzo', 'ITF2': 'Molise', 'ITF3': 'Campania', 'ITF4': 'Puglia', 'ITF5': 'Basilicata',
    'ITF6': 'Calabria', 'ITG1': 'Sicilia', 'ITG2': 'Sardegna',
}

# ---------------------------------------------------------------- 2018
# Sette temi, ciascuno in tre dataset: per età (e sesso), per titolo di studio (e sesso), per regione (e sesso).
# Colonna "categoria": codice[|gruppo][|sesso]; senza gruppo = tutte le età e titoli; senza sesso = totale.
# Le regioni vanno nella colonna "territorio".
TEMI = [
    # indicatore, dataset (età, titolo, regione), campo della voce, campo del grado, gradi da sommare (None = valore diretto)
    ('almeno_uno', (1, 2, 3), 'STEREOT_GENDROLEPARTNER', None, None),
    ('accordo', (4, 5, 6), 'STEREOT_GENDROLEPARTNER', 'DEGREE_AGREEMENT', ('STRAGR', 'SOMAGR')),          # ruoli
    ('accordo', (7, 8, 9), 'STEREOT_GENDROLEPARTNER', 'DEGREE_AGREEMENT', ('STRAGR', 'SOMAGR')),          # violenza sessuale
    ('accettabile', (10, 11, 12), 'STEREOT_GENDROLEPARTNER', 'DEGREE_ACCEPTABILITY', ('ALWACC', 'ACUNDCIR')),  # coppia
    ('diffusione', (13, 14, 15), 'HOW_COMMON', None, None),          # risposte che sommano a circa 100; NA = non risponde
    ('cause', (16, 17, 18), 'POSSIBLE_CAUSES', None, None),          # più risposte
    ('consigli', (19, 20, 21), 'ADVICE', None, None),                # più risposte; NOANSW = non risponde
]
TOTALI_VOCE = {'ALL', 'TOT'}

for indicatore, (n_eta, n_tit, n_reg), campo, grado, gradi in TEMI:
    acc = {}  # (territorio, categoria) -> [valore, dataset]
    for n, tipo in ((n_eta, 'eta'), (n_tit, 'titolo'), (n_reg, 'regione')):
        for r in sdmx(n):
            if r[campo] in TOTALI_VOCE or (gradi and r[grado] not in gradi):
                continue
            area, eta, tit, sesso = r['REF_AREA'], r['AGE'], r['EDU_LEV_HIGHEST'], r['SEX']
            if tipo == 'regione':
                if area not in REGIONI or eta != 'TOTAL' or tit != 'ALL':
                    continue
                territorio, gruppo = REGIONI[area], ''
            else:
                if area != 'IT':
                    continue
                if tipo == 'eta' and tit == 'ALL':
                    gruppo = '' if eta == 'TOTAL' else f'|{eta}'
                elif tipo == 'titolo' and eta == 'TOTAL' and tit != 'ALL':
                    gruppo = f'|{tit}'
                else:
                    continue
                territorio = 'Italia'
            categoria = r[campo] + gruppo + ('' if sesso == 'T' else f'|{sesso}')
            chiave = (territorio, categoria)
            if chiave in acc and acc[chiave][1] != n:
                continue  # il totale Italia compare sia nel file per età sia in quello per titolo: si tiene il primo
            acc.setdefault(chiave, [0.0, n])[0] += float(r['OBS_VALUE'])
    for (territorio, categoria), (v, n) in acc.items():
        nota = f'IstatData RUOLIGEN_{n}' + (f', somma di {" + ".join(gradi)}' if gradi else '') + ('; più risposte' if indicatore in ('cause', 'consigli') else '')
        righe.append([2018, 'anno', territorio, indicatore, categoria, round(v, 1), 'percentuale', nota])

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
