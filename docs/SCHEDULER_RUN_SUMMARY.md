# Selenium Scheduler Run Summary

When the scheduled task starts, Windows launches PowerShell under the configured `SYSTEM` or service account.

1. `run_selenium_tests.ps1` resolves the project root and changes to it.
2. It creates `logs\` and starts a timestamped transcript.
3. It locates and activates the project `.venv`.
4. It sets `PYTHONUNBUFFERED=1` and `SELENIUM_HEADLESS=1`.
5. It runs pytest from the project root.
6. Selenium Manager starts headless Chrome with the configured viewport and browser options.
7. Pytest writes `reports\execution_report.txt`.
8. Failed browser tests save screenshots and diagnostic artifacts.
9. The wrapper records pytest's exit code and returns it to Task Scheduler.

A task state of `Ready` means it is waiting for its next trigger; `Running` means the run is active. A successful run returns exit code `0`. Missing dependencies, browser startup errors, network failures, or failed tests produce a non-zero exit code and are recorded in `logs\`.

The scheduled task must be registered once during deployment with:

```powershell
.\scripts\Register-SuryaSangamTask.ps1 -StartTime '21:40'
```