<#
  deploy.ps1 — Deploy da galeria Lupema Arkhe JK para o AWS S3.

  Uso:
    ./deploy.ps1            # sync completo + cache-control no HTML/JS
    ./deploy.ps1 -QuickHtml # atualiza só index.html e inject.js (rápido)

  Pré-requisitos: AWS CLI instalado e credenciais (aws configure, regiao sa-east-1).
  Os originais em assets/IMAGENS (~570 MB, nao usados pela pagina) nao sobem; use -Originals para incluir.
#>
param([switch]$QuickHtml, [switch]$Originals)

$ErrorActionPreference = 'Stop'
$Bucket = 's3://skylineip/Tour Virtual/LUPEMA/galeria-arkhe-jk'
$NoCache = 'no-cache,no-store,must-revalidate'
Set-Location -Path $PSScriptRoot

if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
  Write-Host 'ERRO: AWS CLI nao encontrado no PATH.' -ForegroundColor Red
  exit 1
}

function Copy-Html($file) {
  Write-Host "  -> $file" -ForegroundColor Cyan
  aws s3 cp $file "$Bucket/$file" --cache-control $NoCache
}

if ($QuickHtml) {
  Copy-Html 'index.html'
  Copy-Html 'inject.js'
}
else {
  $ex = @('--exclude', '.git/*', '--exclude', '.claude/*', '--exclude', '*.py', '--exclude', '*.ps1',
          '--exclude', '*.md', '--exclude', '.gitattributes', '--exclude', '.gitignore',
          '--exclude', 'index.src.html', '--exclude', '*.pdf', '--exclude', 'Thumbs.db', '--exclude', '*/Thumbs.db')
  if (-not $Originals) { $ex += @('--exclude', 'assets/IMAGENS/*') }
  aws s3 sync . "$Bucket/" @ex --delete
  Copy-Html 'index.html'
  Copy-Html 'inject.js'
}

Write-Host 'Deploy concluido.' -ForegroundColor Green
Write-Host 'https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/LUPEMA/galeria-arkhe-jk/index.html' -ForegroundColor DarkGray
