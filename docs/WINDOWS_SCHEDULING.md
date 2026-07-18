# Windows Server Selenium Scheduling

This project uses Windows Task Scheduler to run Selenium tests daily through `scripts\run_selenium_tests.ps1`.

For the complete live-server procedure, see [LIVE_SERVER_SCHEDULE_SETUP.md](LIVE_SERVER_SCHEDULE_SETUP.md). For command reference, see [POWERSHELL_SCHEDULER_COMMANDS.md](POWERSHELL_SCHEDULER_COMMANDS.md).

## One-time server setup

Run PowerShell as Administrator:

```powershell
Set-Location 'D:\selenium testing\surya_sangam_test\surya_sangam_testing'
py -3.13 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

Install Chrome for all users and confirm that the scheduled account can access the project, virtual environment, Chrome, and runtime folders. Selenium 4.27.1 uses Selenium Manager; a separate chromedriver or webdriver-manager package is not required.

## Manual validation

```powershell
Set-Location 'D:\selenium testing\surya_sangam_test\surya_sangam_testing'
& .\scripts\run_selenium_tests.ps1 -PytestArguments 'tests/test_homepage.py -x'
Get-ChildItem .\logs, .\reports
```

The wrapper creates a timestamped transcript under `logs\` and pytest writes `reports\execution_report.txt`. The wrapper returns pytest's exit code.

## Register the daily task

Registration is a required deployment step; copying the project files alone does not create a scheduled task. Use 24-hour local server time:

```powershell
Set-Location 'D:\selenium testing\surya_sangam_test\surya_sangam_testing'
& .\scripts\Register-SuryaSangamTask.ps1 -StartTime '21:40'
Get-ScheduledTask -TaskName 'Surya Sangam Selenium Tests'
```

The task runs as `SYSTEM`, starts when available after downtime, prevents overlapping instances, permits battery operation, and has a four-hour execution limit. The wrapper sets `SELENIUM_HEADLESS=1`, so no visible Chrome window is expected during scheduled runs.

## Verify and test

```powershell
Get-ScheduledTaskInfo -TaskName 'Surya Sangam Selenium Tests' |
    Select-Object LastRunTime, LastTaskResult, NextRunTime, NumberOfMissedRuns

Start-ScheduledTask -TaskName 'Surya Sangam Selenium Tests'
```

`Ready` means the task is waiting. `Running` means a test run is active. A `LastTaskResult` of `0` or `0x0` indicates success.

## Stop, disable, or remove

```powershell
Stop-ScheduledTask -TaskName 'Surya Sangam Selenium Tests'
Disable-ScheduledTask -TaskName 'Surya Sangam Selenium Tests'
Enable-ScheduledTask -TaskName 'Surya Sangam Selenium Tests'
Unregister-ScheduledTask -TaskName 'Surya Sangam Selenium Tests' -Confirm:$false
```

## GUI equivalent

Create a daily task named `Surya Sangam Selenium Tests`. Use `PowerShell.exe` with these arguments:

```text
-NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "D:\selenium testing\surya_sangam_test\surya_sangam_testing\scripts\run_selenium_tests.ps1"
```

Set the working directory to the project root. Select **Run whether user is logged on or not** and **Run with highest privileges**. Use `SYSTEM` or a dedicated service account with the required project, Chrome, network, and write permissions.

## Validation checklist

- Chrome launches in headless mode under the scheduled account.
- The wrapper creates a log and report.
- `Start-ScheduledTask` completes.
- Task Scheduler reports last result `0x0` for a passing run.
- The account can access the website and SMTP service, if email is enabled.