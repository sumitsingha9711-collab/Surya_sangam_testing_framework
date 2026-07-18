# Live Server Scheduled Test Setup

This guide configures Windows Task Scheduler to run the Surya Sangam Selenium tests automatically every day at a specified time.

## 1. Server prerequisites

Install or verify the following on the live server:

- Google Chrome is installed for all users.
- The project is copied to:

```text
D:\selenium testing\surya_sangam_test\surya_sangam_testing
```

- The project virtual environment exists at `.venv`.
- Python, pytest, Selenium, and the required packages are installed in `.venv`.
- The server has network access to the website and SMTP server if email reporting is enabled.

Check the project environment from an elevated PowerShell window:

```powershell
cd "D:\selenium testing\surya_sangam_test\surya_sangam_testing"
.\.venv\Scripts\python.exe -c "import pytest, selenium; print(pytest.__version__); print(selenium.__version__)"
```

## 2. Configure email reporting (optional)

The scheduled task runs as `SYSTEM`. User-level environment variables are not automatically available to it, so configure the variables at the machine level or load them securely through the deployment process.

For Gmail, use an App Password rather than the normal account password:

```powershell
[Environment]::SetEnvironmentVariable('SMTP_HOST', 'smtp.gmail.com', 'Machine')
[Environment]::SetEnvironmentVariable('SMTP_PORT', '587', 'Machine')
[Environment]::SetEnvironmentVariable('SMTP_USER', 'automation@example.com', 'Machine')
[Environment]::SetEnvironmentVariable('SMTP_PASSWORD', '<app-password>', 'Machine')
[Environment]::SetEnvironmentVariable('SURYA_REPORT_EMAIL_TO', 'recipient@example.com', 'Machine')
```

Optional settings:

```powershell
[Environment]::SetEnvironmentVariable('SMTP_FROM', 'automation@example.com', 'Machine')
[Environment]::SetEnvironmentVariable('SURYA_REPORT_EMAIL_CC', '', 'Machine')
[Environment]::SetEnvironmentVariable('SURYA_REPORT_EMAIL_BCC', '', 'Machine')
[Environment]::SetEnvironmentVariable('SMTP_USE_TLS', 'true', 'Machine')
```

Use SMTP port `587` with TLS. Do not store real passwords in source control.

## 3. Register the daily task

Open PowerShell **as Administrator**, change to the project folder, and register the task. Replace `21:40` with the desired 24-hour local server time:

```powershell
cd "D:\selenium testing\surya_sangam_test\surya_sangam_testing"
.\scripts\Register-SuryaSangamTask.ps1 -StartTime "21:40"
```

The task is registered as:

```text
Surya Sangam Selenium Tests
```

The task runs daily as `SYSTEM`, starts when the server becomes available, and uses headless Chrome because scheduled tasks do not have an interactive desktop.

## 4. Verify registration

```powershell
Get-ScheduledTask -TaskName "Surya Sangam Selenium Tests"
Get-ScheduledTaskInfo -TaskName "Surya Sangam Selenium Tests" |
    Select-Object LastRunTime, LastTaskResult, NextRunTime, NumberOfMissedRuns
```

Confirm that `NextRunTime` shows the expected date and time. The time uses the live server's timezone, not the timezone of the deployment computer.

## 5. Test immediately without waiting for the schedule

Start the registered task manually:

```powershell
Start-ScheduledTask -TaskName "Surya Sangam Selenium Tests"
```

Wait for it to finish, then check the result:

```powershell
Get-ScheduledTaskInfo -TaskName "Surya Sangam Selenium Tests" |
    Select-Object LastRunTime, LastTaskResult
```

A successful Windows task result is usually `0` or `0x0`. A non-zero result means the test process failed or was interrupted.

## 6. Find test output

The wrapper writes timestamped logs to:

```text
D:\selenium testing\surya_sangam_test\surya_sangam_testing\logs\
```

Pytest reports are written to:

```text
D:\selenium testing\surya_sangam_test\surya_sangam_testing\reports\
```

Failure screenshots and other artifacts are stored below the reports artifacts folder.

## 7. Important deployment behavior

Copying the project to the live server does not create a scheduled task. The registration command in section 3 must be run once with administrator privileges during deployment.

After registration, the task persists across normal reboots and runs automatically every day at the configured time. If the configured time has already passed today, the first automatic run is tomorrow.

## 8. Troubleshooting

### Task does not exist

Run the registration command from an elevated PowerShell window and verify the task name:

```powershell
Get-ScheduledTask -TaskName "Surya Sangam Selenium Tests"
```

### Task exists but does not run

Check the last result and logs:

```powershell
Get-ScheduledTaskInfo -TaskName "Surya Sangam Selenium Tests"
Get-ChildItem .\logs | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

### Chrome fails under the scheduled task

The scheduled wrapper sets `SELENIUM_HEADLESS=1`. Verify that Chrome is installed for all users and that the project `.venv` exists.

### Email is not sent

Verify SMTP variables in the machine environment. The scheduled `SYSTEM` account cannot use environment variables configured only for your interactive user account.

### Schedule time is incorrect

Check the server timezone:

```powershell
Get-TimeZone
Get-Date
```

The trigger uses the server's local timezone.

## 9. Update or remove the task

To change the schedule, run the registration command again with the new time. The script uses `-Force` and updates the existing task:

```powershell
.\scripts\Register-SuryaSangamTask.ps1 -StartTime "22:00"
```

To remove the task:

```powershell
Unregister-ScheduledTask -TaskName "Surya Sangam Selenium Tests" -Confirm:$false
```