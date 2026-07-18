# Windows Server Selenium scheduling

Run the following from an elevated PowerShell window on the server. The scheduled task uses the `SYSTEM` service account, so it runs when no user is logged in and requires no stored password.

## One-time setup

```powershell
Set-Location 'D:\selenium testing\surya_sangam_test\surya_sangam_testing'
py -3.13 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

Install Chrome for all users and confirm the service account can access it. Selenium 4.27.1 invokes Selenium Manager automatically; no `chromedriver.exe` or `webdriver-manager` package is required.

## Manual validation

```powershell
Set-Location 'D:\selenium testing\surya_sangam_test\surya_sangam_testing'
& .\scripts\run_selenium_tests.ps1
Get-ChildItem .\logs, .\reports
```

The wrapper returns pytest's exit code, creates a timestamped transcript in `logs\`, and the pytest session writes `reports\execution_report.txt`. A non-zero code indicates a failed or interrupted run.

To run a small smoke test first:

```powershell
& .\scripts\run_selenium_tests.ps1 -PytestArguments 'tests/test_homepage.py -x'
```

## Register the daily task

```powershell
Set-Location 'D:\selenium testing\surya_sangam_test\surya_sangam_testing'
& .\scripts\Register-SuryaSangamTask.ps1 -StartTime '02:00'
Get-ScheduledTask -TaskName 'Surya Sangam Selenium Tests'
Start-ScheduledTask -TaskName 'Surya Sangam Selenium Tests'
Get-WinEvent -LogName 'Microsoft-Windows-TaskScheduler/Operational' -MaxEvents 20
```

The `-StartTime` value is local server time and can be changed without editing the wrapper. The task is configured for highest privileges, starts when available after downtime, allows operation on batteries, stops overlapping runs, and has a four-hour execution limit.

## Task Scheduler GUI equivalent

Create Basic Task â†’ name `Surya Sangam Selenium Tests` â†’ Daily â†’ 2:00 AM â†’ Start a program. Set Program to `PowerShell.exe`; set arguments to `-NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "D:\selenium testing\surya_sangam_test\surya_sangam_testing\scripts\run_selenium_tests.ps1"`; set Start in to `D:\selenium testing\surya_sangam_test\surya_sangam_testing`. In Properties â†’ General select **Run whether user is logged on or not** and **Run with highest privileges**. In Conditions clear the AC-power restriction if required. Use the `SYSTEM` account or a dedicated service account with access to the project, virtual environment, Chrome, and log directories.

## Verification checklist

- `python --version` reports Python 3.13.7 and `python -c "import selenium; print(selenium.__version__)"` reports 4.27.1.
- `python -c "from selenium import webdriver; from selenium.webdriver.chrome.options import Options; o=Options(); o.add_argument('--headless=new'); d=webdriver.Chrome(options=o); print(d.capabilities['browserVersion']); d.quit()"` succeeds. This verifies Selenium Manager and headless Chrome without a display.
- The manual wrapper run creates a log and `reports\execution_report.txt`.
- `Start-ScheduledTask` completes and the task's **Last Run Result** is `0x0` for a passing run.
- The service account has network/DNS access to `https://www.suryasangam.com/` and write permission for `logs\`, `reports\`, and screenshots/artifacts.

## Git cleanup

Generated reports and logs are ignored by `.gitignore`. If generated reports are already tracked, remove them from the index while keeping local files:

```powershell
git rm -r --cached --ignore-unmatch reports reports logs
git add .gitignore
git commit -m "Ignore generated Selenium reports and scheduler logs"
```
