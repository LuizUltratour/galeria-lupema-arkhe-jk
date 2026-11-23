# Galeria — Lupema Arkhê JK

Galeria de imagens (apartamentos 148/168 m² e áreas de lazer) para injeção via script no 3DVista, hospedada no AWS S3.

| Item | URL |
|------|-----|
| Galeria | `https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/LUPEMA/galeria-arkhe-jk/index.html` |
| Script  | `https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/LUPEMA/galeria-arkhe-jk/inject.js` |

**S3:** `s3://skylineip/Tour Virtual/LUPEMA/galeria-arkhe-jk/`
**GitHub:** https://github.com/LuizUltratour/galeria-lupema-arkhe-jk

Uso no 3DVista: carregue `inject.js` e chame `GaleriaImagens(1)` (abrir) / `GaleriaImagens(0)` (fechar).

## Estrutura

```
index.src.html      ← template do layout (editar aqui)
index.html          ← gerado por build_index.py (é o que sobe)
build_index.py      ← lê assets/IMAGENS, classifica e injeta o catálogo no template
generate_thumbs.py  ← gera assets/thumbs (900 px) e assets/large (2560 px) a partir de assets/IMAGENS
inject.js · deploy.ps1
assets/  bg.png, close/voltar/proximo-(normal|pressed).png, IMAGENS/ (originais), thumbs/, large/
```

## Atualizar conteúdo

1. Coloque/atualize os arquivos em `assets/IMAGENS/`.
2. `py generate_thumbs.py` e `py build_index.py` (categorias em `RULES` do build; títulos vêm do nome do arquivo).
3. `./deploy.ps1` (S3) e `git push`.
