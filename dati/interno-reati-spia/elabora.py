"""Denunce dei reati spia: ricava dati.csv dalle tavole del Ministero dell'Interno (banca dati SDI-SSD)
diffuse da Istat nella pagina "Il percorso giudiziario", anni 2014-2023, e dalla tavola IstatData
"Delitti violenti" (vittime per sesso, 2024).

Uso:  python elabora.py
Legge originali/ e scrive dati.csv (UTF-8 con BOM). Solo il dato Italia.

- Tavola 1 SDI: delitti denunciati e quota di vittime donne, per reato.
- Tavola 2 SDI: persone denunciate o arrestate, totale e femmine, per reato.
- IstatData DCCV_AUTVITTPS_6: vittime donne dei delitti denunciati, 2023 e 2024 (manca maltrattamenti).
Le cittadinanze e le regioni non sono usate: nelle righe delle regioni 2014-2016 della tavola 1
le percentuali di maltrattamenti e stalking sono scambiate (vedi note.md).
"""
import csv
from pathlib import Path

import openpyxl

QUI = Path(__file__).parent
ORIG = QUI / 'originali'
sdi = openpyxl.load_workbook(ORIG / 'denunce-fonte-SDI-SSD-2014-2023.xlsx', data_only=True)

REATI = {
    'MALTRATTAMENTI CONTRO FAMILIARI O CONVIVENTI': 'maltrattamenti',
    'ATTI PERSECUTORI': 'stalking',
    'PERCOSSE': 'percosse',
    'VIOLENZE SESSUALI': 'violenze_sessuali',
    'OMICIDI VOLONTARI CONSUMATI': 'omicidi',
    'DIFFUSIONE ILLECITA DI IMMAGINI O VIDEO SESSUALMENTE ESPLICITI': 'diffusione_immagini',
    "DEFORMAZIONE DELL'ASPETTO DELLA PERSONA MEDIANTE LESIONI PERMANENTI AL VISO": 'sfregio_viso',
    'COSTRIZIONE O INDUZIONE AL MATRIMONIO': 'matrimonio_forzato',
}

righe = []
def aggiungi(anno, indicatore, categoria, valore, unita, nota=''):
    righe.append([anno, 'anno', 'Italia', indicatore, categoria, valore, unita, nota])

def reato_di(cella):
    if not isinstance(cella, str):
        return None
    testo = ' '.join(cella.split()).upper()
    return next((v for k, v in REATI.items() if testo.startswith(k)), None)

# --- Tavola 1: delitti denunciati e % di vittime donne ------------------------------------------
t1 = list(sdi['tavola 1'].iter_rows(values_only=True))
intest = next(r for r in t1 if r[1] and str(r[1]).startswith('Anno'))
anni = [(j, int(str(c)[-4:])) for j, c in enumerate(intest) if c and str(c).startswith('Anno')]
reato = None
for r in t1:
    nuovo = reato_di(r[0])
    if nuovo:
        reato = nuovo
        continue
    if r[0] == 'ITALIA' and reato:
        for j, anno in anni:
            if isinstance(r[j], (int, float)):
                aggiungi(anno, 'delitti_denunciati', reato, int(r[j]), 'delitti', 'tavola 1 SDI')
                aggiungi(anno, 'quota_vittime_donne', reato, round(100 * r[j + 1], 1), 'percentuale', 'tavola 1 SDI')
        reato = None

# --- Tavola 2: persone denunciate o arrestate -----------------------------------------------------
t2 = list(sdi['tavola 2'].iter_rows(values_only=True))
reato, anni2 = None, []
for r in t2:
    nuovo = reato_di(r[0])
    if nuovo:
        reato = nuovo
        continue
    if reato and r[0] is None and str(r[1]).strip().isdigit():
        # dal 2019 gli anni sono scritti come testo
        anni2 = [(j, int(c)) for j, c in enumerate(r) if c is not None and str(c).strip().isdigit()]
    if r[0] == 'ITALIA' and reato:
        for j, anno in anni2:
            if isinstance(r[j], (int, float)):
                aggiungi(anno, 'persone_denunciate', reato, int(r[j]), 'persone', 'tavola 2 SDI')
                aggiungi(anno, 'persone_denunciate', f'{reato}_femmine', int(r[j + 1]), 'persone', 'tavola 2 SDI')
        reato = None

# --- IstatData: vittime donne 2023-2024 ----------------------------------------------------------
CODICI = {'STALK': 'stalking', 'RAPE': 'violenze_sessuali', 'BLOWS': 'percosse', 'INTENHOM': 'omicidi'}
f = ORIG / 'Delitti violenti, sesso, età - reg. (IT1,73_230_DF_DCCV_AUTVITTPS_6,1.0).csv'
with open(f, encoding='utf-8-sig') as fh:
    for d in csv.DictReader(fh):
        if (d['REF_AREA'] == 'IT' and d['DATA_TYPE'] == 'VICTIM' and d['SEX'] == '2' and d['AGE'] == 'TOTAL'
                and d['TIME_PERIOD'] in ('2023', '2024')):
            aggiungi(int(d['TIME_PERIOD']), 'vittime_donne', CODICI[d['TYPE_CRIME']], int(float(d['OBS_VALUE'])), 'persone', 'IstatData DCCV_AUTVITTPS_6')

righe.sort(key=lambda r: (r[3], r[4], r[0]))
with open(QUI / 'dati.csv', 'w', encoding='utf-8-sig', newline='') as out:
    w = csv.writer(out)
    w.writerow(['anno', 'periodo', 'territorio', 'indicatore', 'categoria', 'valore', 'unita', 'nota'])
    w.writerows(righe)
print(len(righe), 'righe')
