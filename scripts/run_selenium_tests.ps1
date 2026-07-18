[CmdletBinding()]
param(
    [string]$ProjectRoot = '',
    [string]$PythonExecutable = '',
    [string]$PytestArguments = ''
)

$ErrorActionPreference = 'Stop'
$exitCode = 1
$transcriptStarted = $false

try {
    if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
        $ProjectRoot = Split-Path -Parent $PSScriptRoot
    }

    $ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot -ErrorAction Stop).Path
    if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) {
        throw "Project root was not found: $ProjectRoot"
    }

    $logDirectory = Join-Path $ProjectRoot 'logs'
    New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
    $logFile = Join-Path $logDirectory ("selenium_{0:yyyyMMdd_HHmmss}.log" -f (Get-Date))
    Start-Transcript -Path $logFile -Append | Out-Null
    $transcriptStarted = $true

    Write-Host "[$(Get-Date -Format o)] Selenium run started"
    Set-Location -LiteralPath $ProjectRoot

    $venvCandidates = @(
        (Join-Path $ProjectRoot '.venv'),
        (Join-Path (Split-Path -Parent $ProjectRoot) 'surya_sangam_testing\.venv')
    )
    $venv = $venvCandidates | Where-Object { Test-Path -LiteralPath (Join-Path $_ 'Scripts\Activate.ps1') } | Select-Object -First 1
    if ([string]::IsNullOrWhiteSpace($venv)) {
        $venv = Join-Path $ProjectRoot '.venv'
    }
    $activate = Join-Path $venv 'Scripts\Activate.ps1'
    if (-not (Test-Path -LiteralPath $activate -PathType Leaf)) {
        throw "Python virtual environment is missing: $venv. Create it with: py -3.13 -m venv .venv"
    }
    & $activate

    if ([string]::IsNullOrWhiteSpace($PythonExecutable)) {
        $PythonExecutable = Join-Path $venv 'Scripts\python.exe'
    }
    if (-not (Test-Path -LiteralPath $PythonExecutable -PathType Leaf)) {
        throw "Python executable was not found: $PythonExecutable"
    }

    $testRoot = $ProjectRoot
    $pytestConfig = Join-Path $ProjectRoot 'pytest.ini'
    if (-not (Test-Path -LiteralPath $pytestConfig -PathType Leaf)) {
        throw "pytest configuration was not found: $pytestConfig"
    }
    Set-Location -LiteralPath $testRoot
    $env:PYTHONUNBUFFERED = '1'

    $arguments = @('-m', 'pytest', '-c', $pytestConfig)
    if (-not [string]::IsNullOrWhiteSpace($PytestArguments)) {
        $arguments += $PytestArguments -split '\s+'
    }
    Write-Host "[$(Get-Date -Format o)] Running: $PythonExecutable $($arguments -join ' ')"
    & $PythonExecutable @arguments
    $exitCode = $LASTEXITCODE
    Write-Host "[$(Get-Date -Format o)] Pytest completed with exit code $exitCode"
}
catch {
    $exitCode = 1
    Write-Error "[$(Get-Date -Format o)] Selenium run failed: $($_.Exception.Message)"
}
finally {
    if ($transcriptStarted) {
        Write-Host "[$(Get-Date -Format o)] Selenium run finished"
        Stop-Transcript | Out-Null
    }
}

exit $exitCode
