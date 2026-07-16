"""Email the generated execution report using SMTP settings from environment."""

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


DEFAULT_SUBJECT = "Surya Sangam Automation Execution Report"


class EmailReportConfigError(ValueError):
    """Raised when required email configuration is missing or invalid."""


def send_report_email(report_path):
    """Send the report file to all configured recipients.

    Required environment variables:
        SMTP_HOST = "smtp.gmail.com"
        SMTP_USER
        SMTP_PASSWORD
        SURYA_REPORT_EMAIL_TO

    Optional environment variables:
        SMTP_PORT (default: 587)
        SMTP_FROM (default: SMTP_USER)
        SMTP_USE_TLS (default: true)
        SURYA_REPORT_EMAIL_CC
        SURYA_REPORT_EMAIL_BCC
        SURYA_REPORT_EMAIL_SUBJECT
    """
    report_path = Path(report_path)
    _validate_report(report_path)

    config = _load_email_config()
    message = _build_message(config, report_path)

    with smtplib.SMTP(config["host"], config["port"]) as smtp:
        if config["use_tls"]:
            smtp.starttls()
        smtp.login(config["username"], config["password"])
        recipients = config["to"] + config["cc"] + config["bcc"]
        smtp.send_message(message, to_addrs=recipients)


def is_email_configured():
    """Return True when the required environment variables are present."""
    required_keys = (
        "SMTP_HOST",
        "SMTP_USER",
        "SMTP_PASSWORD",
        "SURYA_REPORT_EMAIL_TO",
    )
    return all(os.getenv(key) for key in required_keys)


def _load_email_config():
    missing_keys = [
        key
        for key in (
            "SMTP_HOST",
            "SMTP_USER",
            "SMTP_PASSWORD",
            "SURYA_REPORT_EMAIL_TO",
        )
        if not os.getenv(key)
    ]
    if missing_keys:
        raise EmailReportConfigError(
            "Missing email configuration: " + ", ".join(missing_keys)
        )

    try:
        port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError as error:
        raise EmailReportConfigError("SMTP_PORT must be a number.") from error

    recipients = _parse_addresses(os.getenv("SURYA_REPORT_EMAIL_TO", ""))
    if not recipients:
        raise EmailReportConfigError("SURYA_REPORT_EMAIL_TO must include an address.")

    return {
        "host": os.getenv("SMTP_HOST"),
        "port": port,
        "username": os.getenv("SMTP_USER"),
        "password": os.getenv("SMTP_PASSWORD"),
        "sender": os.getenv("SMTP_FROM", os.getenv("SMTP_USER")),
        "to": recipients,
        "cc": _parse_addresses(os.getenv("SURYA_REPORT_EMAIL_CC", "")),
        "bcc": _parse_addresses(os.getenv("SURYA_REPORT_EMAIL_BCC", "")),
        "subject": os.getenv("SURYA_REPORT_EMAIL_SUBJECT", DEFAULT_SUBJECT),
        "use_tls": os.getenv("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes"),
    }


def _build_message(config, report_path):
    message = EmailMessage()
    message["From"] = config["sender"]
    message["To"] = ", ".join(config["to"])
    if config["cc"]:
        message["Cc"] = ", ".join(config["cc"])
    message["Subject"] = config["subject"]
    message.set_content(
        "Hello,\n\n"
        "The Surya Sangam automation run is complete. "
        "Please find the execution report attached.\n\n"
        "Regards,\nAutomation"
    )

    message.add_attachment(
        report_path.read_bytes(),
        maintype="text",
        subtype="plain",
        filename=report_path.name,
    )
    return message


def _parse_addresses(value):
    separators_normalized = value.replace(";", ",")
    return [
        address.strip()
        for address in separators_normalized.split(",")
        if address.strip()
    ]


def _validate_report(report_path):
    if not report_path.exists():
        raise FileNotFoundError(f"Report file not found: {report_path}")
    if not report_path.is_file():
        raise FileNotFoundError(f"Report path is not a file: {report_path}")


if __name__ == "__main__":
    try:
        from utils.report_generator import REPORT_FILE
    except ModuleNotFoundError:
        from report_generator import REPORT_FILE

    send_report_email(REPORT_FILE)
