[CmdletBinding()]
param(
    [string]$ProjectRoot = '',
    [string]$TaskName = 'Surya Sangam Selenium Tests',
    [string]$StartTime = '21:40'
)

$ErrorActionPreference = 'Stop'
$scriptRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
    $ProjectRoot = $scriptRoot
}
$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot -ErrorAction Stop).Path
$wrapper = Join-Path $ProjectRoot 'scripts\run_selenium_tests.ps1'
if (-not (Test-Path -LiteralPath $wrapper -PathType Leaf)) {
    throw "Wrapper script was not found: $wrapper"
}

$action = New-ScheduledTaskAction -Execute 'PowerShell.exe' -Argument "-NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$wrapper`"" -WorkingDirectory $ProjectRoot
$trigger = New-ScheduledTaskTrigger -Daily -At ([datetime]::ParseExact($StartTime, 'HH:mm', $null))
$principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 4) -MultipleInstances IgnoreNew -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description 'Runs Surya Sangam Selenium tests daily in headless Chrome.' -Force | Out-Null
Write-Host "Registered '$TaskName' to run daily at $StartTime as SYSTEM with highest privileges."
