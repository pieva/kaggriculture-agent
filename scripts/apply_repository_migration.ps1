param(
    [string]$ManifestPath = "docs/repository/migration/REPOSITORY_MIGRATION_MANIFEST.csv",
    [ValidateSet("all", "antigravity", "codex", "copilot")]
    [string]$ExecutionOwner = "all"
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$repoPrefix = $repoRoot.TrimEnd('\') + '\'
Set-Location $repoRoot

function Resolve-SafePath([string]$relativePath) {
    if ([System.IO.Path]::IsPathRooted($relativePath)) {
        throw "Manifest path must be relative: $relativePath"
    }
    $full = [System.IO.Path]::GetFullPath((Join-Path $repoRoot ($relativePath -replace '/', '\')))
    if (-not $full.StartsWith($repoPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Path escapes repository: $relativePath -> $full"
    }
    return $full
}

$manifestFull = Resolve-SafePath $ManifestPath
$rows = @(Import-Csv -LiteralPath $manifestFull)
$moveRows = @($rows | Where-Object {
    $_.action -in @('move', 'archive') -and
    ($ExecutionOwner -eq 'all' -or $_.execution_owner -eq $ExecutionOwner)
})

$destinations = $moveRows | Group-Object proposed_destination | Where-Object Count -gt 1
if ($destinations) {
    throw "Destination collision: $($destinations.Name -join ', ')"
}

$moved = 0
$already = 0
$missingDeleted = 0
foreach ($row in $moveRows) {
    $source = Resolve-SafePath $row.source_path
    $destination = Resolve-SafePath $row.proposed_destination

    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
        if (Test-Path -LiteralPath $destination -PathType Leaf) {
            $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $destination).Hash
            if ($actual -ne $row.sha256) {
                throw "Existing destination hash mismatch: $($row.proposed_destination)"
            }
            $already++
            continue
        }
        if ($row.tracked_status -eq 'TRACKED_DELETED') {
            $missingDeleted++
            continue
        }
        throw "Missing migration source: $($row.source_path)"
    }

    $before = (Get-FileHash -Algorithm SHA256 -LiteralPath $source).Hash
    if ($before -ne $row.sha256) {
        throw "Source changed after freeze: $($row.source_path)"
    }

    if (Test-Path -LiteralPath $destination) {
        throw "Destination already exists: $($row.proposed_destination)"
    }
    $parent = Split-Path -Parent $destination
    if (-not $parent.StartsWith($repoPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Unsafe destination parent: $parent"
    }
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    Move-Item -LiteralPath $source -Destination $destination

    $after = (Get-FileHash -Algorithm SHA256 -LiteralPath $destination).Hash
    if ($after -ne $before) {
        throw "Hash changed during move: $($row.source_path)"
    }
    $moved++
}

Write-Output "MANIFEST_ROWS=$($rows.Count)"
Write-Output "EXECUTION_OWNER=$ExecutionOwner"
Write-Output "MOVE_ROWS=$($moveRows.Count)"
Write-Output "MOVED=$moved"
Write-Output "ALREADY_AT_DESTINATION=$already"
Write-Output "PREEXISTING_DELETIONS_SKIPPED=$missingDeleted"
