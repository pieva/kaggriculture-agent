param(
    [ValidateSet("antigravity", "codex", "copilot")]
    [string]$AgentId = "codex",
    [string]$OutputPath = "docs/repository/migration/MIGRATION_INVENTORY_codex.csv"
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

function Get-ExperimentId([string]$path) {
    $match = [regex]::Match($path, '(?i)(?:^|[/_\-])e(0?[1-9]|1[0-7])(?:[/_\-.]|$)')
    if ($match.Success) {
        return ('E{0:D2}' -f [int]$match.Groups[1].Value)
    }
    if ($path -match '(?i)model_spec_c2|foundation|ontology|state_machine|feature_model') {
        return 'FOUNDATION_C2_1'
    }
    return 'CROSS_ROUND'
}

function Get-Ownership([string]$path) {
    if ($path -match '(?i)antigravity') { return 'antigravity' }
    if ($path -match '(?i)copilot') { return 'copilot' }
    if ($path -match '(?i)codex') { return 'codex' }
    return 'common'
}

function Get-Role([string]$path) {
    if ($path -match '(?i)(^|/)submission[^/]*\.py$|/freeze/') { return 'freeze' }
    if ($path -match '(?i)(^|/)prompts?/') { return 'prompt' }
    if ($path -match '(?i)(design|proposal|preregistration)') { return 'design' }
    if ($path -match '(?i)(^|/)configs?/|config\.json$') { return 'config' }
    if ($path -match '(?i)(^|/)(benchmark|replays?)/.*\.json$') { return 'replay' }
    if ($path -match '(?i)(^|/)tests?/|test_.*\.py$') { return 'test' }
    if ($path -match '(?i)(^|/)scripts?/|analy[sz]e.*\.py$|audit.*\.py$') { return 'tool' }
    if ($path -match '(?i)(^|/)src/|\.py$') { return 'source' }
    if ($path -match '(?i)model_spec') { return 'model_spec' }
    if ($path -match '(?i)ontology|state_machine|feature_model|engine_contract') { return 'foundation' }
    if ($path -match '(?i)review|reconciliation|manifest') { return 'governance' }
    if ($path -match '(?i)report|analysis|summary|\.md$') { return 'report' }
    return 'artifact'
}

function Get-EpistemicRole([string]$path, [string]$role) {
    switch ($role) {
        'foundation' { return 'normative' }
        'model_spec' { return 'normative' }
        'design' { return 'design' }
        'prompt' { return 'prompt' }
        'replay' { return 'input' }
        'source' { return 'normative' }
        'config' { return 'freeze' }
        'freeze' { return 'freeze' }
        'report' { return 'report' }
        'governance' { return 'report' }
        'test' { return 'derived' }
        'tool' { return 'derived' }
        default {
            if ($path -match '(?i)\.json$|\.csv$|\.txt$') { return 'derived' }
            return 'report'
        }
    }
}

function Get-ProposedDestination([string]$path) {
    $p = $path -replace '\\', '/'

    if ($p -in @('README.md', 'pyproject.toml', '.gitignore', 'docs/NEW_SESSION.md', 'docs/PROJECT_STATE.md', 'docs/EXPERIMENT_LOG.md')) { return $p }

    if ($p -eq 'docs/repository/REPOSITORY_ARCHITECTURE.md') { return 'docs/repository/REPOSITORY_ARCHITECTURE.md' }
    if ($p -match '^docs/repository/') { return $p }

    if ($p -match '^docs/model/FOUNDATION_C2_1_MANIFEST\.md$') { return 'docs/foundation/FOUNDATION_C2_1_MANIFEST.md' }
    if ($p -match '^docs/model/(ontology|state_machine|feature_model)/(.+)$') { return "docs/foundation/$($Matches[1])/$($Matches[2])" }
    if ($p -match '^docs/model/model_specs/(antigravity|codex|copilot)/(.+)$') { return "docs/model_specs/$($Matches[1])/$($Matches[2])" }
    if ($p -match '^docs/model/model_specs/(.+)$') { return "docs/model_specs/history/$($Matches[1])" }
    if ($p -match '^docs/model/reviews/(.+)$') { return "docs/governance/foundation/$($Matches[1])" }
    if ($p -eq 'docs/model_specs/history/MODEL_SPEC_PRE_C2.md') { return 'docs/model_specs/history/MODEL_SPEC_PRE_C2.md' }

    if ($p -match '^docs/benchmark/(104527555|104541810|104543983|104547425|104564762|104577270|104578185|104586335|104586487)\.json$') {
        return "data/replays/e17-discovery/$($Matches[1]).json"
    }
    if ($p -match '^docs/benchmark/(.+\.json)$') { return "data/replays/reference/$($Matches[1])" }
    if ($p -eq 'data/replays/MANIFEST.md') { return 'data/replays/MANIFEST.md' }
    if ($p -eq 'docs/benchmark/json.txt') { return 'data/replays/legacy_catalog.txt' }
    if ($p -match '^docs/screenshots/(.+)$') { return "data/screenshots/$($Matches[1])" }

    if ($p -match '^docs/experiment_designs/e(\d{1,2})/(.+)$') {
        $n = [int]$Matches[1]
        $tail = $Matches[2]
        if ($n -eq 17) { return "experiments/e17/design/$tail" }
        return ('experiments/archive/e{0:D2}/design/{1}' -f $n, $tail)
    }

    if ($p -match '^docs/prompts/(.+)$') {
        $name = $Matches[1]
        $round = [regex]::Match($name, '(?i)^E(0?[1-9]|1[0-7])(?:[^0-9]|$)')
        if ($round.Success) {
            $n = [int]$round.Groups[1].Value
            if ($n -eq 17) { return "experiments/e17/prompts/common/$name" }
            return ('experiments/archive/e{0:D2}/prompts/{1}' -f $n, $name)
        }
        return "docs/governance/prompts/$name"
    }

    if ($p -match '^docs/versions/(.+)$') {
        $name = $Matches[1]
        $round = [regex]::Match($name, '(?i)^E(0?[1-9]|1[0-6])(?:[^0-9]|$)')
        if ($round.Success) {
            $n = [int]$round.Groups[1].Value
            return ('experiments/archive/e{0:D2}/reports/{1}' -f $n, $name)
        }
        return "docs/governance/history/versions/$name"
    }

    if ($p -match '^results/e17/(antigravity|codex|copilot)/(.+)$') {
        $owner = $Matches[1]
        $tail = $Matches[2]
        if ($tail -match '(?i)(review|feedback|reconciliation).*\.md$') { return "experiments/e17/reviews/$owner/$tail" }
        if ($tail -match '(?i)\.md$') { return "experiments/e17/reports/$owner/$tail" }
        return "experiments/e17/artifacts/discovery/$owner/$tail"
    }
    if ($p -match '^results/e17/(.+)$') {
        $tail = $Matches[1]
        if ($tail -match '(?i)(feedback|review).*\.md$') { return "experiments/e17/reviews/common/$tail" }
        if ($tail -match '(?i)\.md$') { return "experiments/e17/reports/common/$tail" }
        return "experiments/e17/artifacts/discovery/common/$tail"
    }
    if ($p -match '^results/e(0?[1-9]|1[0-6])(?:/|_|\.|$)(.*)$') {
        $n = [int]$Matches[1]
        $tail = $Matches[2]
        if ([string]::IsNullOrWhiteSpace($tail)) { $tail = Split-Path $p -Leaf }
        return ('experiments/archive/e{0:D2}/artifacts/{1}' -f $n, $tail)
    }
    if ($p -match '^results/benchmark/(.+)$') { return "experiments/archive/e12/artifacts/benchmark/$($Matches[1])" }
    if ($p -match '^results/post_e15/(.+)$') { return "experiments/archive/e15/reports/post_e15/$($Matches[1])" }
    if ($p -match '^results/environment/(.+)$') { return "docs/foundation/evidence/environment/$($Matches[1])" }
    if ($p -match '^results/model_spec_c2/(.+)$') { return "docs/governance/history/model_spec_c2/$($Matches[1])" }

    if ($p -match '^configs/e(0?[1-9]|1[0-6])/(.+)$') {
        $n = [int]$Matches[1]
        return ('experiments/archive/e{0:D2}/configs/{1}' -f $n, $Matches[2])
    }
    if ($p -match '^configs/model_spec_c2/(ANTIGRAVITY|CODEX|COPILOT)_(.+)$') {
        return "docs/model_specs/$($Matches[1].ToLowerInvariant())/configs/$($Matches[1])_$($Matches[2])"
    }

    if ($p -match '^scripts/e17/(antigravity|codex|copilot)/(.+)$') { return "experiments/e17/tools/$($Matches[1])/$($Matches[2])" }
    if ($p -match '^scripts/(.+)$') {
        $name = $Matches[1]
        $round = [regex]::Match($name, '(?i)e(0?[1-9]|1[0-6])')
        if ($round.Success) {
            $n = [int]$round.Groups[1].Value
            return ('experiments/archive/e{0:D2}/tools/{1}' -f $n, $name)
        }
        return $p
    }

    if ($p -eq 'src/agricola/strategy/codex/codex_3q_mixed_high_density.py') { return 'src/agricola/strategy/codex/codex_3q_mixed_high_density.py' }
    if ($p -eq 'src/agricola/strategy/codex/codex_v9_routine_data.py') { return 'src/agricola/strategy/codex/codex_v9_routine_data.py' }
    if ($p -match '^src/agricola/e16/(.+)$') { return "experiments/archive/e16/source/agricola/e16/$($Matches[1])" }

    if ($p -match '^tests/test_e(0?[1-9]|1[0-6])_(.+)$') {
        $n = [int]$Matches[1]
        return ('experiments/archive/e{0:D2}/tests/test_e{0:D2}_{1}' -f $n, $Matches[2])
    }

    if ($p -eq 'experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py') { return 'experiments/archive/e15/artifacts/freeze/legacy_submissions/submission.py' }
    if ($p -eq 'experiments/archive/e16/artifacts/freeze/legacy_submissions/submission_antigravity.py') { return 'experiments/archive/e16/artifacts/freeze/legacy_submissions/submission_antigravity.py' }

    return $p
}

$tracked = @{}
git -c core.quotepath=false ls-files | ForEach-Object { $tracked[$_] = $true }
$modified = @{}
git -c core.quotepath=false diff --name-only | ForEach-Object { $modified[$_] = $true }
$untracked = @{}
git -c core.quotepath=false ls-files --others --exclude-standard | ForEach-Object { $untracked[$_] = $true }
$deleted = @{}
git -c core.quotepath=false ls-files --deleted | ForEach-Object { $deleted[$_] = $true }

$all = @($tracked.Keys + $untracked.Keys | Sort-Object -Unique)
$textCorpus = [System.Text.StringBuilder]::new()
foreach ($path in $all) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { continue }
    $item = Get-Item -LiteralPath $path
    if ($item.Length -gt 512KB) { continue }
    if ($path -match '^(results|data)/' -and $item.Extension -in @('.json', '.csv')) { continue }
    if ($item.Extension -notin @('.md', '.py', '.ps1', '.toml', '.json', '.txt')) { continue }
    try { [void]$textCorpus.AppendLine([System.IO.File]::ReadAllText($item.FullName)) } catch { }
}
$corpus = $textCorpus.ToString()

$rows = foreach ($path in $all) {
    $exists = Test-Path -LiteralPath $path -PathType Leaf
    if ($exists) {
        $sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
    } elseif ($tracked.ContainsKey($path)) {
        $tmp = git show "HEAD:$path" 2>$null
        if ($LASTEXITCODE -eq 0) {
            $bytes = [System.Text.Encoding]::UTF8.GetBytes(($tmp -join "`n") + "`n")
            $sha = [Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData($bytes))
        } else { $sha = 'UNAVAILABLE' }
    } else { $sha = 'UNAVAILABLE' }

    if ($deleted.ContainsKey($path)) { $status = 'TRACKED_DELETED' }
    elseif ($untracked.ContainsKey($path)) { $status = 'UNTRACKED' }
    elseif ($modified.ContainsKey($path)) { $status = 'TRACKED_MODIFIED' }
    else { $status = 'TRACKED_PRESENT' }

    $role = Get-Role $path
    $destination = Get-ProposedDestination $path
    if ($status -eq 'TRACKED_DELETED') { $action = 'candidate_delete' }
    elseif ($destination -eq $path) { $action = 'keep' }
    elseif ($destination -match '(?i)/archive/') { $action = 'archive' }
    else { $action = 'move' }

    $referenceCount = if ($corpus.Contains($path)) { 'FOUND' } else { 'NONE_FOUND' }

    [pscustomobject]@{
        source_path = $path
        sha256 = $sha
        tracked_status = $status
        artifact_role = $role
        experiment_id = Get-ExperimentId $path
        ownership = Get-Ownership $path
        epistemic_role = Get-EpistemicRole $path $role
        proposed_destination = $destination
        action = $action
        references_found = $referenceCount
        notes = if ($status -eq 'TRACKED_DELETED') { 'Deletion pre-existing at migration start; do not restore without owner direction.' } elseif ($destination -eq $path) { 'Canonical or cross-round path retained.' } else { 'Proposed structural move; content hash must remain unchanged.' }
    }
}

$parent = Split-Path -Parent $OutputPath
New-Item -ItemType Directory -Force -Path $parent | Out-Null
$rows | Export-Csv -LiteralPath $OutputPath -NoTypeInformation -Encoding utf8
Write-Output "WROTE=$OutputPath"
Write-Output "ROWS=$($rows.Count)"
Write-Output "MOVES=$(@($rows | Where-Object action -eq 'move').Count)"
Write-Output "ARCHIVES=$(@($rows | Where-Object action -eq 'archive').Count)"
Write-Output "KEEPS=$(@($rows | Where-Object action -eq 'keep').Count)"
Write-Output "CANDIDATE_DELETE=$(@($rows | Where-Object action -eq 'candidate_delete').Count)"
