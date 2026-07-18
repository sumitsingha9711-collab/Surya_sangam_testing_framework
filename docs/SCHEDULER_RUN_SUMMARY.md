# Selenium Scheduler Run Summary

When the scheduled task starts, Windows launches PowerShell with the highest privileges under the configured service account or `SYSTEM` account.

1. The wrapper changes to `D:\selenium testing\surya_sangam_test\surya_sangam_testing`.
2. It creates the `logs\` directory and starts a timestamped execution log.
3. It activates the project Python virtual environment.
4. It starts pytest from the project root.
5. Selenium creates a headless Chrome session through Selenium Manager with GPU and sandbox disabled and a 1920Ã—1080 viewport.
6. Tests execute without requiring a logged-in user or display.
7. The pytest session writes the execution report to `reports\execution_report.txt`.
8. Failed browser tests save diagnostic screenshots and artifacts.
9. The wrapper records the completion status and returns pytestâ€™s exit code to Task Scheduler.

Successful runs return exit code `0`. Missing dependencies, browser startup errors, or failed tests produce a non-zero exit code and are recorded in the timestamped file under `logs\`.
