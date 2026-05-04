$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = Join-Path $Root "src"

python -m bot.cli self-learning-finalize
exit $LASTEXITCODE
