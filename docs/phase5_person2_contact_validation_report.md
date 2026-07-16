# Phase 5 — Person 2 Contact Validation Report

This report section contains only Person 2’s validation and security cases. Run it with:

```powershell
pytest -m contact_validation
```

The existing pytest hook writes the execution result to `reports/execution_report.txt`, including failure screenshots and the unique parameter ID.

| Test case IDs | Scenario | Unique input category | Expected result |
|---|---|---|---|
| P2-CNT-VAL-001-* | Invalid email formats | Missing `@`, domain, username; duplicate `@`; whitespace; incomplete domain | Validation feedback; no successful submission |
| P2-CNT-VAL-002-* | Invalid phone values | Short, long, alphabetic, special-character, mixed, empty | Validation feedback or native invalid behavior; no successful submission |
| P2-CNT-VAL-003 | Empty form | No input | Required fields prevent submission; no success message |
| P2-CNT-SEC-004-* | SQL injection handling | Harmless boolean/comment strings | No alert, crash, database error, stack trace, or unauthorized behavior |
| P2-CNT-SEC-005-* | XSS handling | Script, image-handler, and SVG-handler payloads | No alert/script execution; page remains usable without technical errors |
| P2-CNT-VAL-006 | Valid submission | Unique Person 2 contact data | Meaningful success message and no technical error |

## Execution record

Live browser execution was not completed in this workspace because the configured Python launcher points to an inaccessible interpreter (`C:\Users\MSII\AppData\Local\Programs\Python\Python314\python.exe`). No website defect is reported from this blocked run; rerun the scoped command in an environment with the project interpreter and Chrome available.
