param(
    [switch]$Download,
    [switch]$IncludeLarge
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = Join-Path $Root "src"

python -m pip install --upgrade huggingface-hub transformers datasets sentence-transformers torch safetensors
$ArgsList = @("hf-setup")
if ($Download) {
    $ArgsList += "--download"
}
if ($IncludeLarge) {
    $ArgsList += "--include-large"
}
python -m bot.cli @ArgsList
exit $LASTEXITCODE
