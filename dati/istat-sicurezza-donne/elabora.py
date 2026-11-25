"""Indagine Istat sulla sicurezza delle donne: ricava dati.csv per la domanda 1.

Uso:  python elabora.py   (scrive dati.csv, UTF-8 con BOM)
Serve openpyxl (file .xlsx) e xlrd (file .xls del 2006 e del 2014):  pip install openpyxl xlrd

Il file ha due parti.

1. Righe storiche (colonne da «anno» a «nota»), usate dalla pagina attuale e dalla home.
   Restano uguali: i filtri del sito le cercano per anno, periodo, indicatore e categoria.

2. Righe «prevalenza» (indicatore = prevalenza), una per ogni combinazione di:
   popolazione · periodo · forma · autore · dimensione · gruppo.
   Le colonne in più (popolazione, forma, autore, dimensione, gruppo, avvertenza) servono
   ai riquadri 2006, 2014, 2025 e al confronto.

Da dove vengono i numeri della parte 2:
- 2006: originali/2006/tavole5/Violenza_Tavole.xls (tavole 1 e 3), tutte le donne 16-70.
  Gli ultimi 5 anni del 2006 non sono nelle tavole 2006: vengono dal report 2014,
  prospetto 11 (per caratteristiche) e prospetto 8 (per autore), trascritti qui sotto.
- 2014: i CSV della banca dati Istat in originali/2014 (scaricati il 15/11/2026),
  tutte le donne 16-70 e, per cittadinanza, italiane e straniere 16-70.
  Le ripartizioni del 2014 non sono nella banca dati (ci sono le regioni): vengono dal
  report 2014, prospetto 11.
- 2025, nel corso della vita: originali/2025/Tavole-Violenza.xlsx (25/11/2026), tav. 1, italiane e straniere 16-75.
- 2025, ultimi 5 anni:
  italiane 16-70 per autore e caratteristiche: Allegato-tavole-statistiche.xlsx (primi risultati), tavola 3;
  italiane 16-70 senza distinzione di autore: primi risultati, prospetto 5 (trascritto);
  tutte le donne 16-70 e straniere 16-70: report del 25/11/2026, prospetti 9 (per autore) e 11 (per
  caratteristiche), trascritti. Di quei prospetti si usa solo la colonna 2025: i valori 2006 hanno errori.

Popolazioni: tutte_16_70 (2006, 2014, 2025), italiane_16_70 e straniere_16_70 (2014, 2025),
italiane_16_75 e straniere_16_75 (2025, nel corso della vita). Non si confrontano popolazioni diverse.
«Non risponde» resta un gruppo a sé (gruppo = non_risponde), mai zero o dato mancante.
avvertenza = errore_oltre_35 quando Istat segna il valore con * (errore campionario oltre il 35%).
"""
import csv
import re
import sys
from pathlib import Path

import openpyxl
try:
    import xlrd
except ImportError:
    sys.exit('Manca xlrd: installalo con  pip install xlrd')

QUI = Path(__file__).parent
ORIG = QUI / 'originali'
COLONNE = ['anno', 'periodo', 'territorio', 'indicatore', 'categoria', 'valore', 'unita', 'nota',
           'popolazione', 'forma', 'autore', 'dimensione', 'gruppo', 'avvertenza']
righe = []

# ---------------------------------------------------------------------------------------------
# Parte 1: righe storiche (invariate)
# ---------------------------------------------------------------------------------------------
def aggiungi(anno, periodo, indicatore, categoria, valore, unita, nota):
    righe.append(dict(anno=anno, periodo=periodo, territorio='Italia', indicatore=indicatore,
                      categoria=categoria, valore=valore, unita=unita, nota=nota))

P1 = 'report 2025, prospetto 1; italiane 16-75 anni'
for cat, v in [('fisica_o_sessuale', 31.9), ('fisica', 18.8), ('sessuale', 23.4), ('stupro_o_tentato', 5.7), ('stalking', 15.5)]:
    aggiungi(2025, 'nella_vita', 'violenza', cat, v, 'percentuale', P1 + '; colonna Totale')
aggiungi(2025, 'nella_vita', 'violenza', 'fisica_o_sessuale_vittime', 6393143, 'persone', P1 + '; colonna Totale, valore assoluto')
for cat, v in [('fisica_o_sessuale', 12.6), ('psicologica', 17.9), ('economica', 6.6)]:
    aggiungi(2025, 'nella_vita', 'violenza_da_partner_o_ex', cat, v, 'percentuale', P1 + '; % sulle donne con partner attuale o ex')
aggiungi(2025, 'nella_vita', 'violenza_da_non_partner', 'fisica_o_sessuale', 26.5, 'percentuale', P1)
for cat, v in [('qualsiasi_autore', 13.3), ('ex_partner', 19.1), ('partner_attuale', 3.8)]:
    aggiungi(2025, 'nella_vita', 'hanno_denunciato', cat, v, 'percentuale', 'report 2025, pagina 4; % sulle vittime')

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

ws = openpyxl.load_workbook(ORIG / '2025' / 'Allegato-tavole-statistiche.xlsx', data_only=True)['Tavola 4']
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

# ---------------------------------------------------------------------------------------------
# Parte 2: righe «prevalenza»
# ---------------------------------------------------------------------------------------------
visti = set()
def prevalenza(anno, periodo, popolazione, forma, autore, dimensione, gruppo, valore, nota,
               territorio='Italia', avvertenza=''):
    chiave = (anno, periodo, popolazione, forma, autore, dimensione, gruppo)
    if chiave in visti:
        raise SystemExit(f'Riga doppia: {chiave}')
    visti.add(chiave)
    righe.append(dict(anno=anno, periodo=periodo, territorio=territorio, indicatore='prevalenza',
                      categoria=f'{forma}|{autore}|{dimensione}={gruppo}', valore=valore,
                      unita='percentuale', nota=nota, popolazione=popolazione, forma=forma,
                      autore=autore, dimensione=dimensione, gruppo=gruppo, avvertenza=avvertenza))

def numero(v):
    """Valore di una cella: (numero, avvertenza) oppure None se la cella è vuota o «-»."""
    if v is None or v == '':
        return None
    if isinstance(v, (int, float)):
        return round(float(v), 2), ''
    s = str(v).strip()
    if s in ('-', ''):
        return None
    avv = 'errore_oltre_35' if s.endswith('*') else ''
    return round(float(s.replace('*', '').replace(',', '.')), 2), avv

# Nomi dei gruppi uguali per i tre anni. La chiave è l'inizio dell'etichetta Istat, in minuscolo.
SEZIONI = {'stato civile': 'stato_civile', "classi di età": 'eta', "eta'": 'eta', 'titolo di studio': 'titolo',
           'titoli di studio': 'titolo', 'condizione professionale': 'condizione',
           'ripartizione': 'ripartizione', 'limitazioni': 'limitazioni'}
GRUPPI = [
    ('nubile', 'nubile'), ('coniugata', 'coniugata'), ('separata', 'separata_divorziata'), ('vedova', 'vedova'),
    ('16-24', '16-24'), ('25-34', '25-34'), ('35-44', '35-44'), ('45-54', '45-54'), ('55-64', '55-64'), ('65-70', '65-70'),
    ('laurea', 'post_secondario'), ('post-secondario', 'post_secondario'), ('diploma superiore', 'superiore'),
    ('secondario superiore', 'superiore'), ('licenza media', 'media'), ('secondario di primo grado', 'media'),
    ('licenza elementare', 'elementare_nessuno'), ('elementare/nessun', 'elementare_nessuno'),
    ('dirigenti', 'dirigenti'), ('direttiv', 'direttive_impiegate'), ('operaie', 'operaie'),
    ('lavoratrici in proprio', 'in_proprio'), ('in cerca', 'in_cerca'), ('casalinghe', 'casalinghe'),
    ('studentesse', 'studentesse'), ('ritirate', 'ritirate'), ('in altra condizione', 'altra'), ('altre inattive', 'altra'),
    ('70-75', '70-75'), ('no limitazioni', 'nessuna'), ('nord ovest', 'nord_ovest'), ('nord-ovest', 'nord_ovest'), ('nord est', 'nord_est'), ('nord-est', 'nord_est'),
    ('centro', 'centro'), ('sud', 'sud'), ('isole', 'isole'),
    ('limitazioni gravi', 'gravi'), ('limitazioni non gravi', 'non_gravi'), ('nessuna limitazione', 'nessuna'),
    ('rifiuta/non risponde', 'non_risponde'),
]
def gruppo_di(etichetta):
    e = re.sub(r'\s+', ' ', str(etichetta)).strip().lower()
    return next((g for k, g in GRUPPI if e.startswith(k)), None)

# --- 2006: Violenza_Tavole.xls ----------------------------------------------------------------
xls06 = xlrd.open_workbook(ORIG / '2006' / 'tavole5' / 'Violenza_Tavole.xls')
FORME = [('violenza fisica o sess', 'fisica_o_sessuale'), ('violenza fisica', 'fisica'),
         ('violenza sessuale', 'sessuale'), ('stupro o tentato', 'stupro_o_tentato')]
def forma_di(etichetta):
    e = str(etichetta).replace('\xa0', ' ').strip().lower()
    return next((f for k, f in FORME if e.startswith(k)), None)

T1 = '2006, Violenza_Tavole.xls, tavola 1; tutte le donne 16-70 anni'
s = xls06.sheet_by_name('tavola 1')
for i in range(s.nrows):
    r = s.row_values(i)
    forma = forma_di(r[0])
    if not forma:
        continue
    for col, periodo, autore in [(2, 'nella_vita', 'qualsiasi'), (3, 'nella_vita', 'partner_o_ex'), (4, 'nella_vita', 'non_partner'),
                                 (6, 'ultimi_12_mesi', 'qualsiasi'), (7, 'ultimi_12_mesi', 'partner_o_ex'), (8, 'ultimi_12_mesi', 'non_partner')]:
        n = numero(r[col])
        if n:
            prevalenza(2006, periodo, 'tutte_16_70', forma, autore, 'totale', 'totale', n[0], T1, avvertenza=n[1])

T3 = '2006, Violenza_Tavole.xls, tavola 3; tutte le donne 16-70 anni'
s = xls06.sheet_by_name('tavola 3')
dim = None
for i in range(s.nrows):
    r = s.row_values(i)
    etichetta = str(r[0]).strip()
    if not etichetta:
        continue
    d = next((v for k, v in SEZIONI.items() if etichetta.lower().startswith(k)), None)
    if d:
        dim = d
        continue
    if etichetta.lower().startswith('totale'):
        continue  # il totale è già nella tavola 1
    g = gruppo_di(etichetta)
    if not (dim and g):
        continue
    for col, forma, periodo in [(1, 'fisica_o_sessuale', 'nella_vita'), (2, 'fisica_o_sessuale', 'ultimi_12_mesi'),
                                (4, 'fisica', 'nella_vita'), (5, 'fisica', 'ultimi_12_mesi'),
                                (7, 'sessuale', 'nella_vita'), (8, 'sessuale', 'ultimi_12_mesi'),
                                (10, 'stupro_o_tentato', 'nella_vita')]:
        n = numero(r[col])
        if n:
            prevalenza(2006, periodo, 'tutte_16_70', forma, 'qualsiasi', dim, g, n[0], T3, avvertenza=n[1])

# --- 2006 e 2014, ultimi 5 anni: report 2014 (Violenze_contro_le_donne.pdf), trascritti --------
# Prospetto 11: per caratteristiche, colonne 2006 e 2014, violenza fisica o sessuale / fisica / sessuale.
P11 = 'report 2014 (PDF), prospetto 11; tutte le donne 16-70 anni'
P11_DATI = {  # gruppo: ((fs06, fs14), (f06, f14), (s06, s14))
    'stato_civile': {'nubile': ((25.8, 20.2), (14.3, 12.3), (18.9, 12.1)), 'coniugata': ((7.2, 6.5), (4.4, 4.1), (4.0, 3.3)),
                     'separata_divorziata': ((18.7, 16.3), (13.8, 10.8), (10.3, 9.0)), 'vedova': ((3.2, 4.0), (2.0, 2.3), (1.8, 1.9))},
    'eta': {'16-24': ((31.7, 27.1), (17.2, 16.6), (24.7, 16.7)), '25-34': ((22.1, 18.2), (12.6, 11.3), (15.0, 10.4)),
            '35-44': ((10.9, 10.5), (7.3, 7.1), (6.0, 5.8)), '45-54': ((7.9, 8.0), (4.5, 4.7), (4.4, 4.3)),
            '55-64': ((5.0, 5.4), (2.9, 3.3), (2.7, 2.5)), '65-70': ((2.6, 1.9), (1.2, 1.2), (1.6, 0.9))},
    'titolo': {'post_secondario': ((19.5, 15.1), (11.0, 8.7), (12.6, 8.8)), 'superiore': ((16.1, 12.7), (9.3, 7.9), (10.9, 7.3)),
               'media': ((12.1, 10.6), (7.3, 6.8), (8.0, 5.6)), 'elementare_nessuno': ((3.1, 3.7), (1.7, 2.8), (1.9, 1.9))},
    'condizione': {'dirigenti': ((17.8, 16.3), (12.0, 10.0), (8.6, 8.3)), 'direttive_impiegate': ((14.5, 12.5), (8.5, 8.1), (9.2, 6.7)),
                   'operaie': ((13.0, 11.4), (8.2, 8.1), (8.7, 5.2)), 'in_proprio': ((12.2, 6.1), (6.7, 3.9), (6.9, 3.7)),
                   'in_cerca': ((22.0, 17.3), (12.0, 10.1), (15.8, 10.8)), 'casalinghe': ((5.7, 5.1), (3.4, 2.9), (3.2, 3.0)),
                   'studentesse': ((33.5, 25.9), (18.4, 14.8), (26.2, 16.4)), 'ritirate': ((3.8, 3.5), (2.3, 2.3), (1.9, 1.3)),
                   'altra': ((6.0, 4.8), (3.1, 4.3), (3.7, 2.1))},
    'ripartizione': {'nord_ovest': ((12.9, 10.9), (7.6, 6.3), (8.3, 6.6)), 'nord_est': ((14.2, 10.7), (7.3, 6.5), (9.9, 6.3)),
                     'centro': ((13.8, 12.6), (8.4, 8.8), (9.1, 5.9)), 'sud': ((13.0, 12.3), (7.8, 7.3), (8.4, 7.2)),
                     'isole': ((12.7, 9.0), (7.5, 5.9), (8.9, 5.2))},
}
for dim, gruppi in P11_DATI.items():
    for g, valori in gruppi.items():
        for forma, (v06, v14) in zip(['fisica_o_sessuale', 'fisica', 'sessuale'], valori):
            prevalenza(2006, 'ultimi_5_anni', 'tutte_16_70', forma, 'qualsiasi', dim, g, v06, P11)
            if dim == 'ripartizione':  # il 2014 per le altre caratteristiche viene dalla banca dati
                prevalenza(2014, 'ultimi_5_anni', 'tutte_16_70', forma, 'qualsiasi', dim, g, v14, P11)

# Prospetto 8: per autore, 2006 (il 2014 viene dalla banca dati). Basi: partner attuale = donne con partner,
# ex = donne con un ex, partner o ex = donne con partner attuale o precedente, gli altri = tutte le donne.
P8_2006 = 'report 2014 (PDF), prospetto 8, colonne 2006; tutte le donne 16-70 anni'
for forma, valori in {'fisica_o_sessuale': (4.4, 6.0, 6.6, 4.2, 5.2, 9.0, 13.3), 'fisica': (3.3, 4.6, 5.1, 2.3, 1.2, 3.5, 7.7),
                      'sessuale': (1.6, 2.9, 2.8, 2.5, 4.6, 6.8, 8.9), 'stupro_o_tentato': (0.2, 1.0, 0.7, 0.4, 0.2, 0.6, 1.2)}.items():
    for autore, v in zip(['partner_attuale', 'ex_partner', 'partner_o_ex', 'conoscenti_parenti_amici', 'sconosciuto', 'non_partner', 'qualsiasi'], valori):
        prevalenza(2006, 'ultimi_5_anni', 'tutte_16_70', forma, autore, 'totale', 'totale', v, P8_2006)

# --- 2014: CSV della banca dati Istat -------------------------------------------------------------
NOMI = {}
with open(QUI / 'codici.csv', encoding='utf-8-sig') as fh:
    for r in csv.DictReader(fh):
        NOMI[(r['dimensione'], r['codice'])] = r['etichetta']

PERIODO = {'LT': 'nella_vita', 'Y5': 'ultimi_5_anni', 'M12': 'ultimi_12_mesi'}
FORMA = {'PHSEX': 'fisica_o_sessuale', 'PHY': 'fisica', 'SEXVIOL': 'sessuale', 'RAPE_OR_ATT': 'stupro_o_tentato'}
AUTORE = {('CFP', 'CURR_OR_FORM'): 'partner_o_ex', ('CP', 'CURR_P'): 'partner_attuale', ('FP', 'EX_P'): 'ex_partner',
          ('PNP', 'ANY_P_NOP'): 'qualsiasi', ('PNP', 'NOP'): 'non_partner', ('PNP', 'STRANGER'): 'sconosciuto',
          ('PNP', 'RELATIVE'): 'parente', ('PNP', 'FRIEND'): 'amico', ('PNP', 'FAM_FRIEND'): 'amico_di_famiglia',
          ('PNP', 'COLL'): 'collega', ('PNP', 'ACQUAIN'): 'conoscente', ('PNP', 'PER_KNOWN'): 'persona_conosciuta',
          ('PNP', 'NOT_SPEC'): 'non_partner_non_specificato'}
CODICI = {
    'AGE_WOMAN': ('eta', {'Y16-24': '16-24', 'Y25-34': '25-34', 'Y35-44': '35-44', 'Y45-54': '45-54', 'Y55-64': '55-64', 'Y65-70': '65-70'}),
    'EDU_LEV_WOMAN': ('titolo', {'NP': 'elementare_nessuno', 'LSE': 'media', 'USE_IF': 'superiore', 'CLF_ML': 'post_secondario'}),
    'MARITAL_STATUS_WOMAN': ('stato_civile', {'SIN': 'nubile', 'MAR': 'coniugata', 'DIV': 'separata_divorziata', 'WID': 'vedova'}),
    'LABPROF_STATUS_D_WOMAN': ('condizione', {'EXEMPPRO': 'dirigenti', 'MIDMANCO': 'direttive_impiegate', 'BLUCOAP': 'operaie',
                                              'SLFEMPFA': 'in_proprio', 'SEEKJ': 'in_cerca', 'HOUSWI': 'casalinghe', 'STUD': 'studentesse',
                                              'RET': 'ritirate', 'OTHER6': 'altra'}),
    'ACTIVITY_LIMITATION_6M': ('limitazioni', {'SER_LIM': 'gravi', 'SER_NOTLIM': 'non_gravi', 'NO_LIM': 'nessuna', 'NRP': 'non_risponde'}),
}
TOTALI = {'AGE_WOMAN': 'Y16-70', 'EDU_LEV_WOMAN': 'ALL', 'MARITAL_STATUS_WOMAN': 'ALL', 'LABPROF_STATUS_D_WOMAN': 'ALL',
          'ACTIVITY_LIMITATION_6M': 'ALL', 'REF_AREA': 'IT'}
POPOLAZIONE = {'TOTAL': 'tutte_16_70', 'ITL': 'italiane_16_70', 'FRG': 'straniere_16_70'}

def leggi_csv(nome):
    (percorso,) = [p for p in (ORIG / '2014').glob(f'*{nome}*.csv') if 'etichette' not in p.name]
    with open(percorso, encoding='utf-8-sig') as fh:
        return [r for r in csv.DictReader(fh)], percorso.name

def dove(r):
    """La caratteristica della riga: (dimensione, gruppo, territorio), oppure totale."""
    for colonna, (dim, mappa) in CODICI.items():
        if r[colonna] != TOTALI[colonna]:
            return dim, mappa[r[colonna]], 'Italia'
    if r['REF_AREA'] != 'IT':
        return 'regione', r['REF_AREA'], NOMI[('REF_AREA', r['REF_AREA'])]
    return 'totale', 'totale', 'Italia'

# File «Tipo di autore, …»: tutte le donne, tutti gli autori.
for nome in ['Tipo di autore, età', 'Tipo di autore, titolo', 'Tipo di autore, stato civile',
             'Tipo di autore, condizione', 'Tipo di autore e regione']:
    dati, file = leggi_csv(nome)
    for r in dati:
        base, per = r['DATA_TYPE'].replace('W16_70_', '').split('_')
        autore = AUTORE.get((base, r['PERPETRATOR']))
        dim, g, terr = dove(r)
        if dim == 'totale' and nome != 'Tipo di autore, età':
            continue  # il totale si prende una volta sola
        if r['OBS_VALUE'] == '':
            continue
        prevalenza(2014, PERIODO[per], 'tutte_16_70', FORMA[r['TYPE_VIOLENCE']], autore, dim, g,
                   round(float(r['OBS_VALUE']), 2), f'2014, banca dati Istat, {file}', territorio=terr)

# File «Cittadinanza, …»: italiane e straniere (qualsiasi autore); per tutte le donne solo le limitazioni,
# che negli altri file non ci sono.
for nome in ['Cittadinanza, età', 'Cittadinanza, titolo', 'Cittadinanza, stato civile',
             'Cittadinanza, condizione', 'Cittadinanza, presenza di limitazioni']:
    dati, file = leggi_csv(nome)
    for r in dati:
        per = r['DATA_TYPE'].split('_')[-2]
        pop = POPOLAZIONE[r['CITIZENSHIP_WOMAN']]
        dim, g, terr = dove(r)
        if pop == 'tutte_16_70' and dim != 'limitazioni':
            continue
        if dim == 'totale' and nome != 'Cittadinanza, età':
            continue
        if r['OBS_VALUE'] == '':
            continue
        prevalenza(2014, PERIODO[per], pop, FORMA[r['TYPE_VIOLENCE']], 'qualsiasi', dim, g,
                   round(float(r['OBS_VALUE']), 2), f'2014, banca dati Istat, {file}', territorio=terr)

# --- 2025: allegato Excel ----------------------------------------------------------------------
wb25 = openpyxl.load_workbook(ORIG / '2025' / 'Allegato-tavole-statistiche.xlsx', data_only=True)

T1_25 = ('Tavole-Violenza.xlsx (25/11/2026), tav. 1; {} 16-75 anni (partner attuale: % su chi ha un partner; '
         'ex: su chi ha un ex; partner o ex: su chi ha o ha avuto un partner; non partner e qualsiasi: su tutte)')
t1 = openpyxl.load_workbook(ORIG / '2025' / 'Tavole-Violenza.xlsx', data_only=True)['Tav. 1']
for r in t1.iter_rows(min_row=6, max_row=11, values_only=True):
    forma = forma_di(r[0])
    if not forma:
        continue
    for base, autore in [(1, 'partner_attuale'), (5, 'ex_partner'), (9, 'partner_o_ex'), (13, 'non_partner'), (17, 'qualsiasi')]:
        for k, (pop, chi) in enumerate([('italiane_16_75', 'italiane'), ('straniere_16_75', 'straniere')]):
            n = numero(r[base + 2 * k])
            if n:
                prevalenza(2025, 'nella_vita', pop, forma, autore, 'totale', 'totale', n[0], T1_25.format(chi), avvertenza=n[1])

T3_25 = ('allegato 2025, tavola 3; italiane 16-70 anni; esclusi i rapporti sessuali quando non era in grado di opporsi '
         '(per il confronto con il 2014)')
dim = None
for r in wb25['Tavola 3'].iter_rows(min_row=7, values_only=True):
    etichetta = str(r[0] or '').strip()
    if not etichetta:
        continue
    if etichetta.lower().startswith('numero totale'):
        break
    d = next((v for k, v in SEZIONI.items() if etichetta.lower().startswith(k)), None)
    if d or etichetta.isupper():
        dim = d  # None per le sezioni sulla salute, che non si usano
        continue
    if etichetta.lower() == 'totale':
        dim_g = ('totale', 'totale')
    else:
        g = gruppo_di(etichetta)
        if not (dim and g):
            continue
        dim_g = (dim, g)
    for inizio, forma in [(1, 'fisica_o_sessuale'), (6, 'fisica'), (11, 'sessuale'), (16, 'stupro_o_tentato')]:
        for k, autore in enumerate(['partner_o_ex', 'partner_attuale', 'ex_partner', 'non_partner']):
            n = numero(r[inizio + k])
            if n:
                prevalenza(2025, 'ultimi_5_anni', 'italiane_16_70', forma, autore, *dim_g, n[0], T3_25, avvertenza=n[1])

# --- 2025, ultimi 5 anni, qualsiasi autore: report 2025, prospetto 5 (trascritto, colonna 2025) ----
P5_2025 = {  # gruppo: (fisica o sessuale, fisica, sessuale)
    'stato_civile': {'nubile': (22.4, 11.5, 16.5), 'coniugata': (3.5, 2.3, 1.6), 'separata_divorziata': (10.3, 7.8, 4.7), 'vedova': (0.9, 0.8, 0.1)},
    'eta': {'16-24': (37.6, 18.8, 30.8), '25-34': (18.2, 9.2, 12.2), '35-44': (9.5, 6.1, 4.9), '45-54': (5.4, 4.0, 2.3),
            '55-64': (3.4, 2.2, 1.5), '65-70': (1.6, 1.0, 0.7)},
    'titolo': {'elementare_nessuno': (2.3, 1.6, 1.0), 'media': (8.2, 3.7, 5.8), 'superiore': (12.2, 5.6, 8.2), 'post_secondario': (13.9, 6.5, 8.6)},
    'condizione': {'dirigenti': (11.9, 7.2, 7.1), 'direttive_impiegate': (10.5, 6.1, 6.2), 'operaie': (9.8, 4.6, 7.0),
                   'in_proprio': (3.5, 1.8, 2.0), 'in_cerca': (14.5, 9.6, 9.2), 'casalinghe': (3.7, 2.4, 1.6),
                   'studentesse': (36.2, 18.1, 29.1), 'ritirate': (1.1, 0.7, 0.4), 'altra': (7.4, 4.8, 3.2)},
    'ripartizione': {'nord_ovest': (10.8, 5.6, 7.3), 'nord_est': (12.2, 6.6, 8.2), 'centro': (12.4, 7.7, 7.8),
                     'sud': (10.0, 5.7, 6.9), 'isole': (9.2, 4.7, 5.9)},
    'totale': {'totale': (11.0, 6.1, 7.3)},
}
# Colonna 2014 del prospetto 5, solo per le ripartizioni: la banca dati 2014 non ha le ripartizioni per cittadinanza.
P5_2014_RIPARTIZIONI = {'nord_ovest': (10.6, 5.8, 6.6), 'nord_est': (10.3, 5.9, 6.2), 'centro': (12.7, 8.9, 5.9),
                        'sud': (12.4, 7.2, 7.3), 'isole': (9.0, 5.9, 5.2)}
P5N = 'report 2025 (PDF), prospetto 5, colonna 2025; italiane 16-70 anni'
for dim, gruppi in P5_2025.items():
    for g, valori in gruppi.items():
        for forma, v in zip(['fisica_o_sessuale', 'fisica', 'sessuale'], valori):
            prevalenza(2025, 'ultimi_5_anni', 'italiane_16_70', forma, 'qualsiasi', dim, g, v, P5N)
for g, valori in P5_2014_RIPARTIZIONI.items():
    for forma, v in zip(['fisica_o_sessuale', 'fisica', 'sessuale'], valori):
        prevalenza(2014, 'ultimi_5_anni', 'italiane_16_70', forma, 'qualsiasi', 'ripartizione', g, v,
                   'report 2025 (PDF), prospetto 5, colonna 2014; italiane 16-70 anni')


# --- 2025, ultimi 5 anni, tutte le donne e straniere 16-70: report 25/11/2026, prospetti 9 e 11 (trascritti) ---
# Solo la colonna 2025: i valori 2006 di questi prospetti hanno errori (titolo di studio invertito nel prospetto 11;
# partner stupro o tentato 2,0 e ex partner sessuale 1,6 nel prospetto 9). Il 2006 viene sempre dai nostri dati.
P11_2025 = {  # gruppo: (fisica o sessuale, fisica, sessuale)
    'stato_civile': {'nubile': (21.3, 11.1, 15.5), 'coniugata': (3.8, 2.4, 1.7), 'separata_divorziata': (9.9, 7.5, 4.6), 'vedova': (0.9, 0.9, 0.2)},
    'eta': {'16-24': (36.1, 17.9, 29.7), '25-34': (17.3, 8.7, 11.5), '35-44': (9.3, 6.2, 4.7), '45-54': (5.2, 3.8, 2.1),
            '55-64': (3.4, 2.2, 1.5), '65-70': (1.6, 1.1, 0.6)},
    'titolo': {'elementare_nessuno': (3.0, 2.2, 1.4), 'media': (8.1, 4.9, 5.6), 'superiore': (11.7, 6.5, 7.8), 'post_secondario': (13.4, 7.1, 8.3)},
    'condizione': {'dirigenti': (11.3, 6.9, 6.8), 'direttive_impiegate': (10.4, 6.0, 6.2), 'operaie': (8.9, 5.1, 5.4),
                   'in_proprio': (4.0, 2.4, 2.6), 'in_cerca': (14.3, 8.9, 9.5), 'casalinghe': (3.5, 2.3, 1.6),
                   'studentesse': (35.1, 17.5, 28.3), 'ritirate': (1.2, 0.8, 0.4), 'altra': (7.9, 5.4, 3.0)},
    'ripartizione': {'nord_ovest': (10.5, 5.5, 7.2), 'nord_est': (11.8, 6.6, 7.7), 'centro': (11.9, 7.5, 7.4),
                     'sud': (9.5, 5.4, 6.5), 'isole': (8.9, 4.6, 5.7)},
}
P11N = 'report 25/11/2026 (PDF), prospetto 11, colonna 2025; tutte le donne 16-70 anni'
for dim, gruppi in P11_2025.items():
    for g, valori in gruppi.items():
        for forma, v in zip(['fisica_o_sessuale', 'fisica', 'sessuale'], valori):
            prevalenza(2025, 'ultimi_5_anni', 'tutte_16_70', forma, 'qualsiasi', dim, g, v, P11N)

P9_2025 = {  # popolazione: autore: (fisica o sessuale, fisica, sessuale, stupro o tentato)
    'tutte_16_70': {'partner_attuale': (1.8, 1.3, 0.6, 0.2), 'ex_partner': (4.4, 3.0, 2.3, 1.0), 'partner_o_ex': (3.9, 2.8, 1.8, 0.6),
                    'non_partner': (8.3, 3.9, 5.9, 0.7), 'qualsiasi': (10.6, 6.0, 7.0, 1.3)},
    'straniere_16_70': {'partner_attuale': (2.9, 2.3, 1.1, 0.4), 'ex_partner': (2.5, 2.3, 1.1, 0.2), 'partner_o_ex': (3.5, 2.9, 1.4, 0.4),
                        'non_partner': (4.4, 2.1, 3.1, 0.6), 'qualsiasi': (7.3, 4.6, 4.2, 1.0)},
}
for pop, autori in P9_2025.items():
    chi = 'tutte le donne' if pop.startswith('tutte') else 'straniere'
    for autore, valori in autori.items():
        for forma, v in zip(['fisica_o_sessuale', 'fisica', 'sessuale', 'stupro_o_tentato'], valori):
            prevalenza(2025, 'ultimi_5_anni', pop, forma, autore, 'totale', 'totale', v,
                       f'report 25/11/2026 (PDF), prospetto 9, colonna 2025; {chi} 16-70 anni')

# --- 2025, report del 25/11/2026: prospetti 1, 3 e 8 (trascritti) e tavola 9 (Excel) -------------------------------
FORME4 = ['fisica_o_sessuale', 'fisica', 'sessuale', 'stupro_o_tentato']
# Prospetto 1: tutte le donne di 16-75 anni, tre periodi, per autore. Nota (a) del prospetto: i valori fra 0,0 e 0,2
# hanno errore campionario oltre il 35%.
P1_2025 = {
    'nella_vita': {'partner_attuale': (3.0, 2.4, 1.1, 0.3), 'ex_partner': (18.7, 15.6, 8.7, 4.7), 'partner_o_ex': (12.6, 10.5, 5.6, 2.9),
                   'non_partner': (25.9, 12.3, 20.2, 3.7), 'qualsiasi': (31.5, 18.9, 22.8, 5.9)},
    'ultimi_5_anni': {'partner_attuale': (1.7, 1.3, 0.6, 0.2), 'ex_partner': (4.1, 2.9, 2.3, 1.1), 'partner_o_ex': (3.6, 2.6, 1.7, 0.7),
                      'non_partner': (7.7, 3.6, 5.6, 0.7), 'qualsiasi': (9.9, 5.6, 6.5, 1.4)},
    'ultimi_12_mesi': {'partner_attuale': (0.7, 0.5, 0.3, 0.1), 'ex_partner': (0.9, 0.6, 0.5, 0.2), 'partner_o_ex': (1.1, 0.7, 0.5, 0.1),
                       'non_partner': (3.1, 1.5, 2.2, 0.2), 'qualsiasi': (3.9, 2.1, 2.5, 0.3)},
}
for periodo, autori in P1_2025.items():
    for autore, valori in autori.items():
        for forma, v in zip(FORME4, valori):
            prevalenza(2025, periodo, 'tutte_16_75', forma, autore, 'totale', 'totale', v,
                       'report 25/11/2026 (PDF), prospetto 1; tutte le donne 16-75 anni',
                       avvertenza='errore_oltre_35' if v <= 0.2 else '')

# Prospetto 8: nel corso della vita, qualsiasi autore, per caratteristiche; tutte, italiane, straniere (16-75).
# Per gruppo: (tutte: fis. o sess., fisica, sessuale, stupro o tentato; italiane: idem; straniere: idem).
P8_2025 = {
    'stato_civile': {'nubile': (40.4, 23.3, 30.9, 7.8, 41.8, 23.8, 32.3, 7.7, 26.7, 18.2, 18.2, 8.5),
                     'coniugata': (23.9, 13.5, 16.9, 3.8, 23.8, 12.9, 17.1, 3.6, 25.5, 18.5, 15.6, 5.2),
                     'separata_divorziata': (48.2, 37.1, 31.7, 12.0, 48.3, 37.3, 31.5, 11.7, 47.9, 34.1, 33.9, 15.3),
                     'vedova': (19.6, 13.5, 13.4, 3.7, 19.0, 12.7, 13.1, 3.4, 26.7, 22.6, 16.8, 7.1)},
    'eta': {'16-24': (39.8, 19.9, 33.0, 8.2, 41.4, 20.8, 34.2, 8.5, 19.9, 8.5, 18.1, 3.7),
            '25-34': (41.3, 24.3, 31.4, 8.9, 43.4, 25.5, 33.4, 9.1, 28.1, 17.0, 19.6, 7.1),
            '35-44': (37.5, 24.1, 26.4, 7.3, 38.6, 24.3, 27.2, 6.8, 31.2, 23.0, 22.1, 10.6),
            '45-54': (30.6, 20.2, 20.6, 5.4, 31.1, 20.0, 21.5, 5.4, 27.3, 22.0, 13.5, 5.5),
            '55-64': (28.0, 17.0, 20.0, 4.4, 27.9, 16.5, 20.2, 4.3, 28.4, 22.5, 17.5, 6.3),
            '65-70': (19.1, 11.0, 13.4, 3.4, 19.1, 10.8, 13.5, 3.3, 19.3, 14.4, 10.7, 5.8),
            '70-75': (17.6, 9.2, 11.8, 2.4, 17.4, 9.0, 11.6, 2.2, 23.4, 14.8, 17.9, 8.2)},
    'titolo': {'elementare_nessuno': (12.1, 9.2, 5.6, 1.9, 10.0, 7.6, 4.6, 1.3, 25.9, 20.5, 12.2, 5.6),
               'media': (23.4, 15.2, 15.9, 4.8, 22.9, 14.5, 16.0, 4.5, 28.0, 22.4, 15.6, 7.7),
               'superiore': (34.7, 21.0, 25.3, 6.5, 35.8, 21.3, 26.3, 6.4, 26.4, 18.1, 17.5, 7.3),
               'post_secondario': (42.0, 22.7, 32.8, 7.2, 42.9, 23.0, 33.3, 7.3, 30.3, 18.7, 25.3, 6.1)},
    'condizione': {'dirigenti': (42.4, 26.5, 31.6, 8.2, 43.3, 26.9, 32.3, 7.7, 25.8, 19.3, 20.1, 16.3),
                   'direttive_impiegate': (37.1, 21.7, 27.6, 5.9, 37.6, 21.9, 27.9, 6.0, 26.6, 15.3, 21.3, 4.0),
                   'operaie': (29.7, 20.4, 19.3, 6.3, 29.7, 18.9, 20.3, 5.1, 29.6, 22.7, 17.6, 8.2),
                   'in_proprio': (30.2, 18.2, 22.0, 5.3, 27.4, 15.1, 20.8, 3.4, 37.2, 26.1, 25.1, 10.1),
                   'in_cerca': (42.6, 30.0, 29.4, 11.2, 43.9, 31.3, 29.9, 11.6, 33.9, 22.0, 26.2, 8.7),
                   'casalinghe': (20.2, 12.9, 13.4, 4.0, 20.1, 12.5, 13.8, 4.0, 20.8, 15.9, 9.9, 3.6),
                   'studentesse': (39.2, 19.9, 32.0, 8.1, 40.5, 20.6, 33.0, 8.4, 19.4, 9.6, 17.0, 3.4),
                   'ritirate': (21.2, 11.1, 15.4, 3.5, 21.2, 11.0, 15.4, 3.3, 20.3, 15.6, 13.5, 9.0),
                   'altra': (34.7, 26.5, 22.5, 8.3, 34.1, 25.4, 21.9, 6.9, 43.4, 42.0, 30.3, 28.2)},
    'salute': {'bene': (31.3, 18.2, 22.8, 5.4, 31.9, 18.2, 23.5, 5.3, 26.3, 18.5, 16.6, 6.4),
               'ne_bene_ne_male': (30.3, 20.1, 21.8, 6.7, 30.2, 19.7, 21.8, 6.3, 31.5, 23.8, 21.7, 10.6),
               'male': (38.6, 26.4, 27.6, 10.4, 38.8, 26.4, 27.6, 10.6, 35.8, 26.2, 27.7, 7.8)},
    'malattie': {'si': (37.3, 23.4, 27.8, 7.9, 37.1, 23.0, 27.6, 7.6, 44.9, 34.5, 33.8, 18.0),
                 'no': (29.3, 17.3, 21.1, 5.1, 29.8, 17.1, 21.7, 5.0, 25.7, 18.1, 16.2, 6.0)},
    'limitazioni': {'gravi': (39.3, 25.1, 29.1, 9.6, 39.4, 24.9, 29.4, 9.3, 37.2, 29.2, 24.6, 15.3),
                    'non_gravi': (34.6, 23.6, 25.6, 8.2, 34.3, 22.9, 25.3, 7.9, 38.4, 31.4, 29.2, 11.3),
                    'nessuna': (30.7, 17.9, 22.2, 5.4, 31.2, 17.9, 22.9, 5.2, 25.8, 17.9, 16.1, 6.4)},
}
for dim, gruppi in P8_2025.items():
    for g, valori in gruppi.items():
        for k, (pop, chi) in enumerate([('tutte_16_75', 'tutte le donne'), ('italiane_16_75', 'italiane'), ('straniere_16_75', 'straniere')]):
            for forma, v in zip(FORME4, valori[4 * k:4 * k + 4]):
                prevalenza(2025, 'nella_vita', pop, forma, 'qualsiasi', dim, g, v,
                           f'report 25/11/2026 (PDF), prospetto 8; {chi} 16-75 anni')

# Prospetto 3: nel corso della vita per cittadinanza (prime sei cittadinanze straniere e rifugiate), 16-75 anni.
NAZ = ['italiana', 'straniera', 'romania', 'ucraina', 'albania', 'marocco', 'cina', 'filippine', 'altre_straniere', 'rifugiate']
P3_2025 = {  # autore: forma: valori nelle colonne di NAZ (la prima colonna del prospetto, italiane e straniere, è il totale)
    'partner_o_ex': {'fisica_o_sessuale': (12.6, 12.1, 19.2, 15.9, 10.2, 9.6, 6.6, 8.1, 9.0, 19.0), 'fisica': (10.6, 9.7, 14.6, 12.9, 7.5, 9.2, 4.0, 5.6, 7.8, 15.7),
                     'sessuale': (5.6, 5.6, 8.4, 9.0, 5.5, 4.8, 4.8, 5.1, 3.7, 8.1), 'stupro_o_tentato': (2.9, 3.0, 4.1, 4.1, 3.8, 2.7, 0.8, 3.4, 2.3, 4.6)},
    'non_partner': {'fisica_o_sessuale': (26.5, 20.6, 21.4, 22.2, 18.2, 10.4, 19.0, 27.0, 20.9, 35.4), 'fisica': (12.2, 13.1, 10.7, 16.5, 10.7, 7.5, 12.6, 15.5, 14.2, 29.9),
                    'sessuale': (20.8, 14.7, 15.9, 12.4, 10.8, 4.6, 11.4, 19.0, 16.3, 22.8), 'stupro_o_tentato': (3.5, 5.0, 5.4, 3.9, 4.1, 0.2, 4.9, 7.3, 5.4, 13.6)},
    'qualsiasi': {'fisica_o_sessuale': (31.9, 27.4, 32.7, 30.0, 24.4, 17.9, 21.8, 30.6, 25.9, 44.9), 'fisica': (18.8, 19.6, 21.9, 23.4, 16.2, 14.9, 14.5, 19.0, 18.9, 39.8),
                  'sessuale': (23.4, 17.8, 21.3, 17.6, 14.4, 8.5, 13.1, 20.9, 17.9, 26.0), 'stupro_o_tentato': (5.7, 7.1, 8.7, 6.7, 7.1, 2.5, 5.5, 9.7, 6.7, 17.0)},
}
for autore, forme in P3_2025.items():
    for forma, valori in forme.items():
        for g, v in zip(NAZ, valori):
            prevalenza(2025, 'nella_vita', 'tutte_16_75', forma, autore, 'cittadinanza', g, v,
                       'report 25/11/2026 (PDF), prospetto 3; donne 16-75 anni della stessa cittadinanza')

# Tavola 9: nel corso della vita, non partner e partner o ex partner, per caratteristiche; tutte le donne 16-75.
SEZ9 = {'stato civile': 'stato_civile', 'età': 'eta', 'titolo di studio': 'titolo', 'condizione professionale': 'condizione',
        'salute autopercepita': 'salute', 'malattie croniche': 'malattie', 'limitazioni': 'limitazioni'}
GR9 = {'salute': {'bene o molto bene': 'bene', 'nè bene nè male': 'ne_bene_ne_male', 'né bene né male': 'ne_bene_ne_male', 'male o molto male': 'male'},
       'malattie': {'sì': 'si', 'no': 'no'}, 'eta': {'70-75': '70-75'}}
T9N = ('Tavole-Violenza.xlsx (25/11/2026), tav. 9; tutte le donne 16-75 anni (Istat scrive «per 100 donne» '
       'anche per partner o ex partner, senza dire se la base sono le donne con un partner attuale o precedente)')
t9 = openpyxl.load_workbook(ORIG / '2025' / 'Tavole-Violenza.xlsx', data_only=True)['Tav. 9']
dim = None
for r in t9.iter_rows(min_row=4, values_only=True):
    et = re.sub(r'\s+', ' ', str(r[0] or '').replace('\xa0', ' ')).strip()
    if not et or et.upper() == 'TOTALE' or et.startswith('Fonte'):
        if et.startswith('Fonte'):
            break
        continue
    d = next((v for k, v in SEZ9.items() if et.lower().startswith(k)), None) if et.isupper() else None
    if d:
        dim = d
        continue
    g = GR9.get(dim, {}).get(et.lower()) or gruppo_di(et)
    if not (dim and g):
        raise SystemExit(f'Tavola 9: gruppo non riconosciuto {et!r}')
    for inizio, autore in [(1, 'non_partner'), (5, 'partner_o_ex')]:
        for k, forma in enumerate(FORME4):
            n = numero(r[inizio + k])
            if n:
                prevalenza(2025, 'nella_vita', 'tutte_16_75', forma, autore, dim, g, n[0], T9N, avvertenza=n[1])

# ---------------------------------------------------------------------------------------------
with open(QUI / 'dati.csv', 'w', encoding='utf-8-sig', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=COLONNE, lineterminator='\n', restval='')
    w.writeheader()
    w.writerows(righe)
print(f'{len(righe)} righe scritte in dati.csv')
