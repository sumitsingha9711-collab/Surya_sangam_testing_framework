# PowerShell Scheduler Commands

Use **PowerShell as Administrator** for task registration, stopping, and removal.

## 1. Open the project folder

```powershell
cd "D:\selenium testing\surya_sangam_test\surya_sangam_testing"
```

## 2. Register the daily schedule

Replace `21:40` with the desired time in 24-hour format. The time uses the live server's local timezone.

```powershell
.\scripts\Register-SuryaSangamTask.ps1 -StartTime "21:40"
```

The task name is:

```text
Surya Sangam Selenium Tests
```

Registration must be performed once after deployment. The task then runs automatically every day.

## 3. Verify the task

```powershell
Get-ScheduledTask -TaskName "Surya Sangam Selenium Tests" |
    Select-Object TaskName, State

Get-ScheduledTaskInfo -TaskName "Surya Sangam Selenium Tests" |
    Select-Object LastRunTime, LastTaskResult, NextRunTime, NumberOfMissedRuns
```

Task states:

- `Ready`: registered and waiting for the next scheduled time.
- `Running`: the test run is currently active.
- `Disabled`: the schedule is turned off.

A `LastTaskResult` of `0` or `0x0` means the previous run completed successfully.

## 4. Start the task immediately

Use this when testing the setup without waiting for the scheduled time:

```powershell
Start-ScheduledTask -TaskName "Surya Sangam Selenium Tests"
```

## 5. Monitor the running task

Check its state:

```powershell
Get-ScheduledTask -TaskName "Surya Sangam Selenium Tests" |
    Select-Object TaskName, State
```

Watch the newest test log:

```powershell
$log = Get-ChildItem .\logs\selenium_*.log |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

Get-Content $log.FullName -Wait
```

Press `Ctrl+C` only to stop viewing the log. It does not stop the test.

Logs are stored in:

```text
D:\selenium testing\surya_sangam_test\surya_sangam_testing\logs\
```

## 6. Stop a currently running task

```powershell
Stop-ScheduledTask -TaskName "Surya Sangam Selenium Tests"
```

Check that it stopped:

```powershell
Get-ScheduledTask -TaskName "Surya Sangam Selenium Tests" |
    Select-Object TaskName, State
```

## 7. Disable future automatic runs

This keeps the task but prevents it from running automatically:

```powershell
Disable-ScheduledTask -TaskName "Surya Sangam Selenium Tests"
```

Re-enable it later:

```powershell
Enable-ScheduledTask -TaskName "Surya Sangam Selenium Tests"
```

## 8. Remove the schedule completely

This stops future runs and deletes the task from Task Scheduler:

```powershell
Unregister-ScheduledTask `
    -TaskName "Surya Sangam Selenium Tests" `
    -Confirm:$false
```

Verify removal:

```powershell
Get-ScheduledTask -TaskName "Surya Sangam Selenium Tests"
```

If PowerShell reports that no task was found, the schedule has been removed.

## 9. Change the scheduled time

Run the registration command again with the new time. The registration script updates the existing task:

```powershell
.\scripts\Register-SuryaSangamTask.ps1 -StartTime "22:00"
```

Check the server clock before troubleshooting timing issues:

```powershell
Get-Date
Get-TimeZone
```

If the configured time has already passed today, the next automatic run will be tomorrow.