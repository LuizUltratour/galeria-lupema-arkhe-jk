"""Gera index.html a partir de index.src.html + arquivos de assets/IMAGENS.
Uso: py build_index.py   (depois de generate_thumbs.py)"""
import os, re, json, unicodedata
BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'assets', 'IMAGENS')

def norm(s): return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().upper()

RULES = [  # (regex sobre nome normalizado, categoria, sub)
    (r'^148', 'apartamentos', 'a148'),
    (r'^168', 'apartamentos', 'a168'),
    (r'^(PISCINA|DET PISCINA|QUADRA|DETALHE GOL)', 'lazer', 'piscina'),
    (r'^(FITNESS|EXTERNO FITNESS|SAUNA|WELLNESS|ZEN|VEST)', 'lazer', 'wellness'),
    (r'^(FAMILY|KIDS|TEEN|PLAYGROUND|ESPACO PET|BIKE WASH|WC FAMILY)', 'lazer', 'familia'),
    (r'^(SALAO|COZINHA|LAVABO|GOURMET|VARANDA|DET VARANDA|WINE BAR|COWORKING)', 'lazer', 'social'),
]
SMALL = {'DE', 'DA', 'DO', 'E', 'NA'}
FIX = {'JK': 'JK', 'WC': 'WC', 'VEST.': 'Vestiário', 'DET': 'Detalhe', 'GOL': 'Gol'}

def title(stem):
    s = re.sub(r'\s*\(\d+\)', '', stem)            # remove "(2)"
    s = re.sub(r'^\d+\s*-\s*', '', s)               # remove prefixo "148 - "
    out = []
    for w in s.split():
        u = w.upper()
        if u in FIX: out.append(FIX[u])
        elif u in SMALL: out.append(w.lower())
        elif w.isdigit(): out.append(w)
        else: out.append(w[0].upper() + w[1:].lower())
    return ' '.join(out)

def nkey(s): return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', norm(s))]

items = []
for f in sorted(os.listdir(SRC), key=lambda f: nkey(os.path.splitext(f)[0])):
    stem, ext = os.path.splitext(f)
    if ext.lower() not in ('.png', '.jpg', '.jpeg', '.webp'): continue
    n = norm(stem)
    for rx, cat, sub in RULES:
        if re.match(rx, n):
            t = title(stem)
            items.append([stem, t, cat, sub]); break
    else:
        print('SEM CATEGORIA:', f)

# imagens "wide" (destaque) a cada 7 itens dentro de cada sub, para ritmo visual
cnt = {}
for it in items:
    k = it[3]; cnt[k] = cnt.get(k, 0) + 1
    if cnt[k] % 7 == 1: it.append(1)

html = open(os.path.join(BASE, 'index.src.html'), encoding='utf-8').read()
html = html.replace('/*ITEMS*/[]', json.dumps(items, ensure_ascii=False, indent=0).replace('\n', ''))
open(os.path.join(BASE, 'index.html'), 'w', encoding='utf-8').write(html)
print(len(items), 'itens')
