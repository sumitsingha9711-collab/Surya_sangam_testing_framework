"""Plain text execution report generation for pytest results."""

import platform
from datetime import datetime
from pathlib import Path

import selenium


REPORT_DIR = Path(__file__).resolve().parents[1] / "reports"
REPORT_FILE = REPORT_DIR / "execution_report.txt"


class ReportGenerator:
    """Builds a text report from pytest execution data."""

    def __init__(self, website_url, browser):
        """Initialize report metadata."""
        self.website_url = website_url
        self.browser = browser
        self.start_time = datetime.now()
        self.test_results = []
        self._seen_results = {}

    def add_result(self, result):
        """Add a single pytest result dictionary while keeping unique logs."""
        result_key = self._build_result_key(result)
        existing_index = self._seen_results.get(result_key)

        if existing_index is None:
            self._seen_results[result_key] = len(self.test_results)
            self.test_results.append(result)
        else:
            self.test_results[existing_index] = result

    def generate(self):
        """Write the execution report to the reports directory."""
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        total = len(self.test_results)
        passed = self._count_by_status("PASS")
        failed = self._count_by_status("FAIL")
        skipped = self._count_by_status("SKIP")
        pass_percentage = (passed / total * 100) if total else 0
        fail_percentage = (failed / total * 100) if total else 0

        lines = [
            "=======================================",
            "Surya Sangam Automation Report",
            "=======================================",
            f"Execution Date: {self.start_time.strftime('%Y-%m-%d')}",
            f"Execution Time: {self.start_time.strftime('%H:%M:%S')}",
            f"Browser: {self.browser}",
            f"Python Version: {platform.python_version()}",
            f"Selenium Version: {selenium.__version__}",
            f"Website URL: {self.website_url}",
            f"Total Test Cases: {total}",
            f"Passed: {passed}",
            f"Failed: {failed}",
            f"Skipped: {skipped}",
            f"Pass Percentage: {pass_percentage:.2f}%",
            f"Fail Percentage: {fail_percentage:.2f}%",
            f"Execution Duration: {duration:.2f} sec",
            "",
            "=======================================",
            "Result Summary By Area",
            "=======================================",
        ]
        lines.extend(self._format_category_summary())
        lines.extend(
            [
                "",
                "=======================================",
                "Executed Test Cases",
                "=======================================",
            ]
        )

        for index, result in enumerate(self.test_results, start=1):
            lines.extend(self._format_test_result(index, result))

        lines.extend(
            [
                "=======================================",
                "Summary",
                "=======================================",
                f"Total: {total}",
                f"Passed: {passed}",
                f"Failed: {failed}",
                f"Pass Percentage: {pass_percentage:.2f}%",
                f"Fail Percentage: {fail_percentage:.2f}%",
                "",
                "=======================================",
                "Recommendations",
                "=======================================",
            ]
        )
        lines.extend(self._recommendations())

        REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
        return REPORT_FILE

    def _build_result_key(self, result):
        return (
            result.get("name", ""),
            result.get("category", "General"),
            result.get("status", ""),
            result.get("reason", ""),
            result.get("screenshot", ""),
        )

    def _count_by_status(self, status):
        return sum(1 for result in self.test_results if result["status"] == status)

    def _format_test_result(self, index, result):
        lines = [
            f"TC{index:03d} - {result['name']}",
            f"Area: {result.get('category', 'General')}",
            result["status"],
            f"Duration: {result['duration']:.2f} sec",
        ]
        if result.get("reason"):
            lines.extend(["Problem Details:", result["reason"]])
        if result.get("screenshot"):
            lines.extend(
                [
                    "Screenshot Evidence:",
                    result["screenshot"],
                    "Open this image to see the exact browser state at failure.",
                ]
            )
        lines.extend(["---", ""])
        return lines

    def _format_category_summary(self):
        if not self.test_results:
            return ["No tests were executed."]

        categories = sorted(
            {result.get("category", "General") for result in self.test_results}
        )
        lines = []
        for category in categories:
            category_results = [
                result
                for result in self.test_results
                if result.get("category", "General") == category
            ]
            total = len(category_results)
            passed = sum(1 for result in category_results if result["status"] == "PASS")
            failed = sum(1 for result in category_results if result["status"] == "FAIL")
            skipped = sum(1 for result in category_results if result["status"] == "SKIP")
            lines.append(
                f"{category}: Total={total}, Passed={passed}, "
                f"Failed={failed}, Skipped={skipped}"
            )
        return lines

    def _recommendations(self):
        failed_tests = [
            result for result in self.test_results if result["status"] == "FAIL"
        ]
        if not failed_tests:
            return ["All site checks passed. Continue adding tests for deeper flows."]

        recommendations = []
        for result in failed_tests:
            recommendations.append(
                f"- Review '{result['name']}' and validate the related page "
                "element, link, or application behavior."
            )
            if result.get("screenshot"):
                recommendations.append(
                    "  Screenshot evidence is listed directly under the failed "
                    f"test: {result['screenshot']}."
                )
        return recommendations
