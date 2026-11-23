"""
Gera thumbs (900 px) e large (2560 px, lightbox) a partir de assets/IMAGENS.
Saída: assets/thumbs/IMAGENS/<nome>.jpg  e  assets/large/IMAGENS/<nome>.jpg
Uso: py generate_thumbs.py [--force]
"""
from PIL import Image
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'assets', 'IMAGENS')
FORCE = '--force' in sys.argv
JOBS = [('thumbs', 900, 82), ('large', 2560, 88)]

def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        bg = Image.new('RGB', im.size, (33, 26, 18))
        bg.paste(im, mask=im.split()[3])
        return bg
    return im.convert('RGB')

n = 0
for fname in sorted(os.listdir(SRC)):
    stem, ext = os.path.splitext(fname)
    if ext.lower() not in ('.png', '.jpg', '.jpeg', '.webp'):
        continue
    im = None
    for folder, size, q in JOBS:
        out_dir = os.path.join(BASE, 'assets', folder, 'IMAGENS')
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, stem + '.jpg')
        if os.path.exists(out) and not FORCE:
            continue
        if im is None:
            im = flat(Image.open(os.path.join(SRC, fname)))
        c = im.copy()
        c.thumbnail((size, size), Image.LANCZOS)
        c.save(out, 'JPEG', quality=q, optimize=True, progressive=True)
        n += 1
    print('ok', fname)
print('gerados:', n)
