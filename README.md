# Modern Galeria — Lupema Arkhê JK

Galeria de imagens (apartamentos 148/168 m² e áreas de lazer) para injeção via script no 3DVista, hospedada no AWS S3.

**Projeto:** Lupema — Arkhê JK
**Tema:** marrom escuro + areia (`#211A12` / `#E9DBCE`), baseado em `assets/bg.png` e nos botões

---

## URLs de produção

| Arquivo | URL |
|---------|-----|
| Galeria | `https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/LUPEMA/galeria-arkhe-jk/index.html` |
| Script  | `https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/LUPEMA/galeria-arkhe-jk/inject.js` |

**S3 path:** `s3://skylineip/Tour Virtual/LUPEMA/galeria-arkhe-jk/`
**GitHub:** https://github.com/LuizUltratour/galeria-lupema-arkhe-jk.git

---

## Estrutura de arquivos

```
galeria/  (Lupema / Arkhê JK)
├── index.src.html          ← template do layout (editar aqui)
├── index.html              ← gerado por build_index.py (é o que sobe; auto-suficiente)
├── build_index.py          ← lê assets/IMAGENS, classifica e injeta o catálogo no template
├── generate_thumbs.py      ← gera thumbs (900 px) e large (2560 px) a partir de assets/IMAGENS
├── inject.js               ← loader leve para injeção no 3DVista
├── deploy.ps1              ← deploy para o S3 (Windows; sync)
└── assets/
    ├── IMAGENS/            ← originais (só disco/S3 com -Originals; gitignored)
    ├── thumbs/IMAGENS/     ← miniaturas da grade (.jpg, gerado)
    ├── large/IMAGENS/      ← versões ~2560 px do visualizador (.jpg, gerado)
    ├── bg.png              ← imagem de fundo
    └── close-*, voltar-*, proximo-*.png ← botões (normal / pressed), exibidos em 45×45 px
```

> O S3 é case-sensitive: nomes de arquivo em `assets/IMAGENS/` definem os caminhos de `thumbs/` e `large/` (mesmo nome, extensão `.jpg`).

---

## Categorias da galeria

| Categoria | Subcategorias |
|-----------|---------------|
| Apartamentos | 148 m² · 168 m² |
| Lazer | Piscina & Esportes · Wellness · Social & Gourmet · Família & Pet |

A classificação é feita pelo prefixo do nome do arquivo (lista `RULES` em `build_index.py`); o título exibido vem do nome do arquivo.

---

## Atualizar conteúdo

1. Coloque/atualize os arquivos em `assets/IMAGENS/`.
2. `py generate_thumbs.py` (use `--force` para regenerar tudo) e `py build_index.py`.
3. `./deploy.ps1` (S3) e `git push`.

---

## Deploy AWS S3

> **Windows:** use `./deploy.ps1` (sync completo + `cache-control` no HTML/JS).
> Requer **AWS CLI** e credenciais (`aws configure`, região `sa-east-1`).

```powershell
./deploy.ps1             # sync completo (sem os originais de assets/IMAGENS)
./deploy.ps1 -Originals  # inclui os originais (~570 MB)
./deploy.ps1 -QuickHtml  # só index.html e inject.js
```

Equivalente manual:

```bash
aws s3 sync . "s3://skylineip/Tour Virtual/LUPEMA/galeria-arkhe-jk/" \
  --exclude ".git/*" --exclude ".claude/*" --exclude "*.py" --exclude "*.ps1" \
  --exclude "*.md" --exclude "index.src.html" --exclude "assets/IMAGENS/*" --delete

aws s3 cp index.html "s3://skylineip/Tour Virtual/LUPEMA/galeria-arkhe-jk/index.html" \
  --cache-control "no-cache,no-store,must-revalidate"
aws s3 cp inject.js "s3://skylineip/Tour Virtual/LUPEMA/galeria-arkhe-jk/inject.js" \
  --cache-control "no-cache,no-store,must-revalidate"
```

> **`--cache-control "no-cache,no-store,must-revalidate"`** — essencial para o browser nunca servir uma versão cacheada do script ou da galeria.

---

## Integração 3DVista

### Passo 1 — Loader (colocar no JavaScript global do projeto)

```js
(function(){
  var s = document.createElement('script');
  s.src = 'https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/LUPEMA/galeria-arkhe-jk/inject.js?v=' + Date.now();
  document.head.appendChild(s);
})();
```

> **`?v=` + `Date.now()`** — cache-busting: força o browser a baixar sempre a versão mais recente do script.

### Passo 2 — Acionar nos hotspots/botões

```js
// Abre a galeria de imagens
GaleriaImagens(1);

// Fecha a galeria de imagens
GaleriaImagens(0);
```

O botão de fechar da galeria envia `postMessage({action:'closeGallery'})` ao 3DVista, que o `inject.js` já trata.

> Plantas, vídeos, 360° e diferenciais não fazem parte desta versão (os assets não existem no projeto atual); `GaleriaPlantas`, `AbrirGaleriaVideos`, `Galeria360` e `AbrirDiferenciais` foram removidos do `inject.js`.

---

## Cores e tipografia

| Token CSS | Valor | Papel |
|-----------|-------|-------|
| `--bg` | `#211A12` | Fundo (cor do `bg.png`) |
| `--panel-2` | `#3F372E` | Botões em estado normal |
| `--sand` | `#E9DBCE` | Texto, destaque e botões pressionados |
| Fonte títulos | Cormorant Garamond | — |
| Fonte UI | Inter | — |
