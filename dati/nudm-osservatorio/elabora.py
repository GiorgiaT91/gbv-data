"""Osservatorio Non Una Di Meno: copie senza dati personali e dati.csv per l'infografica.
Uso: python3 elabora.py  (dalla cartella dati/nudm-osservatorio)
Legge originali/*.csv (scaricati dal sito, mai modificati), scrive pubblicabili/*.csv e dati.csv."""
import csv, glob, os, collections

# Colonne tolte nelle copie pubblicabili: nomi e testi liberi che possono contenere nomi o dettagli personali
DA_TOGLIERE = ['Nome', 'Cognome', 'Nome presunto colpevole', 'Descrizione', 'Altre persone_descrizione',
               'Cosa succede dopo?', 'Disabilità - descrizione dai media """"""""', 'Disabilità/malattia',
               'Giustificazione - descrizione dei media """"""""', 'Giustificazione sui media',
               'Descrizione reato', 'Iter reato']
PARTNER = {'marito', 'moglie', 'partner', 'ex partner', 'ex marito', 'ex moglie', 'compagno', 'fidanzato',
           'ex fidanzato', 'convivente', 'ex convivente'}
FAMILIARI = {'figlio', 'figlia', 'figlie', 'padre', 'madre', 'fratello', 'sorella', 'nipote', 'cugino', 'genero',
             'nuora', 'cognato', 'ex genero', 'suocero', 'zio', 'genitori', 'nonno', 'figliastro', 'patrigno',
             'partner della madre', 'ex partner della madre', 'fidanzato sorella', 'fidanzato della figlia'}
PERIODO = {'2026': '1 gennaio-8 novembre'}  # aggiornare a ogni nuovo download
# Correzioni decise da Giorgia: si usa il valore pubblicato sul sito quando il file ne conta uno in meno
CORREZIONI = {('2023', 'femminicidi'): (107, 'valore del sito; il file ne conta 106'),
              ('2023', 'totale'): (123, 'valore del sito; il file ne conta 122')}

def leggi(f):
    with open(f, encoding='utf-8-sig', newline='') as h:
        return list(csv.DictReader(h))

def genere(x): return (x.get('Genere') or x.get('Note di genere') or '').strip()
def tipo(x): return (x.get('Tipo') or '').strip().lower()
def relazione(x):
    r = (x.get('Relazione con la persona uccisa') or '').strip().lower()
    return 'partner_o_ex' if r in PARTNER else 'altro_familiare' if r in FAMILIARI else 'non_indicata' if r in ('', '-', 'nessuna') else 'altri'
def reato(s):
    s = (s or '').lower()
    if '577-bis' in s or 'femminicidio' in s: return 'reato_femminicidio_art_577bis'
    if 'estinzione' in s: return 'reato_estinto_autore_morto'
    if s.strip() in ('', '-'): return 'reato_non_indicato'
    if 'istigazione' in s: return 'reato_istigazione_al_suicidio'
    if 'preterintenzionale' in s or 'colposo' in s: return 'reato_omicidio_preterintenzionale_o_colposo'
    return 'reato_omicidio_volontario'

righe = []
def add(anno, ind, cat, val, nota=''):
    if ind == 'casi_monitorati' and (anno, cat) in CORREZIONI:
        val, nota = CORREZIONI[(anno, cat)]
    righe.append([anno, PERIODO.get(anno, 'anno'), 'Italia', ind, cat, val, 'persone', nota])

for f in sorted(glob.glob('originali/*.csv')):
    anno = f[-8:-4]
    r = leggi(f)
    # copia pubblicabile
    campi = [c for c in r[0].keys() if c not in DA_TOGLIERE]
    with open(f'pubblicabili/nudm_{anno}.csv', 'w', encoding='utf-8-sig', newline='') as h:
        w = csv.DictWriter(h, fieldnames=campi, extrasaction='ignore', lineterminator='\n'); w.writeheader(); w.writerows(r)
    # conteggi
    fem = [x for x in r if tipo(x) == 'omicidio' and genere(x) == '(F)']
    add(anno, 'casi_monitorati', 'totale', len(r), 'tutte le voci')
    add(anno, 'casi_monitorati', 'femminicidi', len(fem), 'tipo omicidio, vittima donna')
    add(anno, 'casi_monitorati', 'transcidi', sum(1 for x in r if tipo(x) == 'omicidio' and genere(x) == '(trans)'))
    add(anno, 'casi_monitorati', 'suicidi_indotti', sum(1 for x in r if tipo(x) == 'suicidio'), 'donne, persone trans e uomini')
    add(anno, 'casi_monitorati', 'in_accertamento', sum(1 for x in r if tipo(x) == 'in corso di accertamento'))
    altre = sum(1 for x in r if tipo(x) not in ('omicidio', 'suicidio', 'in corso di accertamento')) + \
            sum(1 for x in r if tipo(x) == 'omicidio' and genere(x) not in ('(F)', '(trans)'))
    add(anno, 'casi_monitorati', 'altre_voci', altre, 'persone scomparse, uomini uccisi negli stessi contesti, altro')
    add(anno, 'femminicidi_con_denunce_o_contatti_precedenti', 'totale',
        sum(1 for x in fem if (x.get('Denunce e/o contatti/accesso a CAV o SS') or '').strip().upper() == 'SI'),
        'almeno: denunce o contatti con centri antiviolenza o servizi sociali riportati dai media')
    if 'Reato contestato' in r[0]:
        pe = [x for x in fem if relazione(x) == 'partner_o_ex']
        add(anno, 'femminicidi_da_partner_o_ex', 'totale', len(pe))
        for k, v in sorted(collections.Counter(reato(x['Reato contestato']) for x in pe).items()):
            add(anno, 'femminicidi_da_partner_o_ex', k, v, 'reato contestato secondo i media; può cambiare con le indagini')

import sys
OUT = sys.argv[1] if len(sys.argv) > 1 else 'dati.csv'
with open(OUT, 'w', encoding='utf-8-sig', newline='') as h:
    w = csv.writer(h, lineterminator='\n')
    w.writerow(['anno', 'periodo', 'territorio', 'indicatore', 'categoria', 'valore', 'unita', 'nota'])
    w.writerows(righe)
print(len(righe), 'righe in dati.csv')
