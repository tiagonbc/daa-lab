# Monthly update: refresh Norgate data, rebuild results, commit and push the new signals.
# Run after the close on the last trading day of the month (Norgate Data Updater must be running).
# The commit timestamp is the audit trail: each month's signals are published before their returns are known.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
python scripts/run_all.py
if ($LASTEXITCODE -ne 0) { throw "pipeline failed" }
python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw "tests failed" }
git add docs/data README.md
$stamp = Get-Date -Format "yyyy-MM-dd"
git commit -m "Monthly signals and results through $stamp"
git push
