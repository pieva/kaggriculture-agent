param(
    [string]$ManifestPath = "docs/repository/migration/REPOSITORY_MIGRATION_MANIFEST.csv",
    [string]$AuditPath = "docs/repository/migration/REFERENCE_REWRITE_MANIFEST.csv"
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot
$rows = @(Import-Csv -LiteralPath $ManifestPath | Where-Object {
    $_.action -in @('move', 'archive') -and $_.source_path -ne $_.proposed_destination
})

$replacements = [System.Collections.Generic.List[object]]::new()
foreach ($row in $rows) {
    $replacements.Add([pscustomobject]@{ Old = $row.source_path; New = $row.proposed_destination })
    $oldWindows = $row.source_path -replace '/', '\'
    $newWindows = $row.proposed_destination -replace '/', '\'
    if ($oldWindows -ne $row.source_path) {
        $replacements.Add([pscustomobject]@{ Old = $oldWindows; New = $newWindows })
    }
}
$replacements.Add([pscustomobject]@{
    Old = 'agricola.strategy.codex.codex_3q_mixed_high_density'
    New = 'agricola.strategy.codex.codex_3q_mixed_high_density'
})
$replacements.Add([pscustomobject]@{
    Old = 'agricola.strategy.codex.codex_v9_routine_data'
    New = 'agricola.strategy.codex.codex_v9_routine_data'
})

$extensions = @('.md', '.py', '.ps1', '.toml', '.json', '.txt')
$files = Get-ChildItem -LiteralPath $repoRoot -File -Recurse -ErrorAction SilentlyContinue | Where-Object {
    $_.FullName -notmatch '\\.git\\|\\.venv\\|\\.pytest_cache\\|\\.pytest_temp\\|\\.ruff_cache\\|\\__pycache__\\' -and
    $_.Extension -in $extensions -and
    $_.Length -le 8MB -and
    $_.FullName -notmatch '\\data\\replays\\.*\.json$' -and
    $_.FullName -notmatch '\\artifacts\\.*\.(json|txt)$' -and
    $_.FullName -notmatch '\\freeze\\.*\.py$' -and
    $_.FullName -notlike (Join-Path $repoRoot ($AuditPath -replace '/', '\'))
}

$audit = [System.Collections.Generic.List[object]]::new()
foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    $updated = $content
    $count = 0
    foreach ($replacement in $replacements) {
        if ($updated.Contains($replacement.Old)) {
            $occurrences = ([regex]::Matches($updated, [regex]::Escape($replacement.Old))).Count
            $updated = $updated.Replace($replacement.Old, $replacement.New)
            $count += $occurrences
        }
    }
    if ($updated -ne $content) {
        $before = [Convert]::ToHexString(
            [System.Security.Cryptography.SHA256]::HashData(
                [System.Text.Encoding]::UTF8.GetBytes($content)
            )
        )
        [System.IO.File]::WriteAllText(
            $file.FullName,
            $updated,
            [System.Text.UTF8Encoding]::new($false)
        )
        $after = (Get-FileHash -Algorithm SHA256 -LiteralPath $file.FullName).Hash
        $audit.Add([pscustomobject]@{
            path = ($file.FullName.Substring($repoRoot.Length + 1) -replace '\\', '/')
            replacements = $count
            sha256_before = $before
            sha256_after = $after
        })
    }
}

$auditParent = Split-Path -Parent $AuditPath
New-Item -ItemType Directory -Force -Path $auditParent | Out-Null
$audit | Export-Csv -LiteralPath $AuditPath -NoTypeInformation -Encoding utf8
Write-Output "FILES_CHANGED=$($audit.Count)"
Write-Output "REPLACEMENTS=$((($audit | Measure-Object replacements -Sum).Sum))"
