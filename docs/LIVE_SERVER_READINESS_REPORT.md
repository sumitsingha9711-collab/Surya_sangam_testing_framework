# Live Server Readiness Report

## Project

Surya Sangam Selenium Automation

## Assessment date

2026-07-18

## Executive decision

**Status: NOT READY for production scheduling yet.**

The project is suitable for staging validation. The moved scripts now resolve the project root correctly, and a wrapper smoke test passed. Production use should wait until the operational prerequisites and validation steps below are completed.

## Current evidence

| Check | Result |
|---|---|
| Python runtime | Passed: Python 3.13.7 |
| Selenium | Passed: 4.27.1 |
| Pytest | Passed: 8.3.4 |
| Chrome installed locally | Present |
| Test collection | Passed: 121 tests collected |
| Wrapper smoke test | Passed: 1 test passed, exit code 0 |
| Scheduled task | Not found on the current machine |
| Full live-site suite | Not completed |
| Generated-artifact protection | .gitignore is missing |
| Pytest marker configuration | contact marker is missing |

## Required actions before production

### 1. Prepare a clean deployment directory

Copy only the source and configuration files to the server. Do not deploy generated caches or prior execution artifacts.

Keep:

- conftest.py
- pytest.ini
- requirements.txt
- locators\
- pages\
- tests\
- utils\
- scripts\
- docs\

Do not copy:

- .git\
- .venv\
- __pycache__\
- .pytest_cache\
- logs\
- reports\
- screenshots\

Create writable runtime directories:

~~~powershell
Set-Location 'D:\selenium testing\surya_sangam_test\surya_sangam_testing'
New-Item -ItemType Directory -Force logs,reports,screenshots | Out-Null
~~~

### 2. Add artifact exclusions

Create a .gitignore file containing:

~~~gitignore
.venv/
__pycache__/
.pytest_cache/
*.py[cod]

logs/
reports/
screenshots/

.env
*.log
~~~

This prevents test output, caches, credentials, and local environments from being committed or copied unintentionally.

### 3. Install and verify the server runtime

Run from an elevated PowerShell window:

~~~powershell
Set-Location 'D:\selenium testing\surya_sangam_test\surya_sangam_testing'

py -3.13 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt

python --version
python -c "import selenium, pytest; print(selenium.__version__); print(pytest.__version__)"
~~~

Expected versions:

- Python 3.13.x
- Selenium 4.27.1
- Pytest 8.3.4

### 4. Verify Chrome and Selenium Manager

Chrome must be installed for all users and accessible to the account that runs the scheduled task.

~~~powershell
& .\.venv\Scripts\python.exe -c "from selenium import webdriver; from selenium.webdriver.chrome.options import Options; o=Options(); o.add_argument('--headless=new'); o.add_argument('--no-sandbox'); d=webdriver.Chrome(options=o); print(d.capabilities['browserVersion']); d.quit()"
~~~

If this fails, verify:

- Chrome is installed.
- The server has outbound network access for Selenium Manager.
- The scheduled account can launch Chrome.
- The server security policy permits headless browser execution.

### 5. Configure optional email reporting

Email is optional. If required, configure these environment variables for the scheduled account:

~~~powershell
[Environment]::SetEnvironmentVariable('SMTP_HOST', 'smtp.gmail.com', 'Machine')
[Environment]::SetEnvironmentVariable('SMTP_PORT', '587', 'Machine')
[Environment]::SetEnvironmentVariable('SMTP_USER', 'automation@example.com', 'Machine')
[Environment]::SetEnvironmentVariable('SMTP_PASSWORD', '<use-an-app-password-or-secret>', 'Machine')
[Environment]::SetEnvironmentVariable('SURYA_REPORT_EMAIL_TO', 'recipient@example.com', 'Machine')
~~~

Do not place passwords in scripts, README files, or source control. Prefer a managed secret store when available.

### 6. Correct the pytest marker warning

Add this marker to pytest.ini:

~~~ini
contact: Contact page and contact-form validation tests
~~~

This removes the current PytestUnknownMarkWarning warnings.

### 7. Run a controlled staging smoke test

~~~powershell
Set-Location 'D:\selenium testing\surya_sangam_test\surya_sangam_testing'
& .\.venv\Scripts\Activate.ps1
& .\scripts\run_selenium_tests.ps1 -PytestArguments 'tests/test_homepage.py -x'
~~~

Confirm:

- Exit code is 0.
- A file appears under logs\.
- reports\execution_report.txt is generated.
- Chrome exits after the run.
- No unexpected data is submitted to the live site.

### 8. Run the full suite with business approval

The suite contains contact-form and valid-submission tests. Run these against staging or with approved test data before using them against production.

~~~powershell
& .\scripts\run_selenium_tests.ps1
$LASTEXITCODE
Get-Content .\reports\execution_report.txt
~~~

Do not treat production readiness as confirmed until the full run completes with an accepted result and the failed-test report has been reviewed.

### 9. Register the scheduled task

Run as Administrator:

~~~powershell
Set-Location 'D:\selenium testing\surya_sangam_test\surya_sangam_testing'
& .\scripts\Register-SuryaSangamTask.ps1 -StartTime '02:00'

Get-ScheduledTask -TaskName 'Surya Sangam Selenium Tests'
Start-ScheduledTask -TaskName 'Surya Sangam Selenium Tests'
Start-Sleep -Seconds 10
Get-ScheduledTaskInfo -TaskName 'Surya Sangam Selenium Tests'
~~~

Expected successful result:

- Task exists.
- Task runs under the intended service account or SYSTEM.
- Last task result is 0.
- A new log and report are created.

### 10. Confirm server permissions

The scheduled account needs:

- Read and execute permission for the project and virtual environment.
- Write permission for logs\, reports\, and screenshots\.
- Permission to launch Chrome.
- Network/DNS access to https://www.suryasangam.com/.
- Access to the SMTP service if email reporting is enabled.

## Go-live checklist

Mark each item complete before production scheduling:

- [ ] Clean deployment directory created.
- [ ] .gitignore added.
- [ ] Python and dependencies installed.
- [ ] Chrome launches headlessly under the scheduled account.
- [ ] Selenium Manager works without manual driver installation.
- [ ] Runtime directories are writable.
- [ ] Email configuration tested, if required.
- [ ] contact marker added.
- [ ] Staging smoke test passed.
- [ ] Full suite completed with results reviewed.
- [ ] Scheduled task registered.
- [ ] Scheduled task manually started successfully.
- [ ] Task Scheduler last result is 0.
- [ ] Logs and reports confirmed.
- [ ] Rollback owner and contact identified.

## Rollback procedure

If the scheduled run causes failures or unexpected behavior:

~~~powershell
Disable-ScheduledTask -TaskName 'Surya Sangam Selenium Tests'
Get-ScheduledTaskInfo -TaskName 'Surya Sangam Selenium Tests'
~~~

Preserve the latest files from:

- logs\
- reports\
- screenshots\

After the issue is diagnosed, re-enable the task:

~~~powershell
Enable-ScheduledTask -TaskName 'Surya Sangam Selenium Tests'
~~~

## Final recommendation

Proceed to staging deployment and operational validation. Do not enable unattended production execution until the scheduled task, service-account permissions, headless Chrome check, artifact handling, and full approved test run are complete.
