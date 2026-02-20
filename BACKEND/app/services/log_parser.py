import re
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.log_categories import LogCategory


import re
from datetime import datetime

# Main log pattern (standard format: YYYY-MM-DD HH:MM:SS LEVEL service message)
PRIMARY_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<severity>DEBUG|INFO|WARN|ERROR|FATAL)\s+"
    r"(?P<service>\S+)\s+"
    r"(?P<message>.+)"
)

# Alternate format (DD-MM-YYYY)
ALT_PATTERN = re.compile(
    r"(?P<timestamp>\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<severity>\w+)\s+"
    r"(?P<service>\S+)\s+"
    r"(?P<message>.+)"
)

# Pattern for API access logs
ACCESS_LOG_PATTERN = re.compile(
    r"(?P<severity>\w+):\s+"
    r"(?P<client>\S+)\s+-\s+"
    r'"(?P<method>\w+)\s+(?P<path>\S+)\s+HTTP/(?P<http_version>[\d.]+)"\s+'
    r"(?P<status_code>\d+)\s+(?P<status_message>.+)"
)

# Supported severity levels
SUPPORTED_LEVELS = {"DEBUG", "INFO", "WARN", "ERROR", "FATAL"}


def clean_log_lines(raw_text: str) -> list[dict]:
    """
    Convert raw log text into a clean, standardized format:
    {
        "timestamp": ISO8601 string,
        "severity": uppercase severity,
        "service": string,
        "message": string
    }
    """

    normalized_logs = []
    seen = set()  # Used to remove duplicate lines

    for line in raw_text.splitlines():

        line = line.strip()

        # Skip empty or duplicate lines
        if not line or line in seen:
            continue

        seen.add(line)

        log_data = None

        # Try matching primary format
        match = PRIMARY_PATTERN.match(line)
        if match:
            log_data = match.groupdict()

        # Try alternate format
        if not log_data:
            match = ALT_PATTERN.match(line)
            if match:
                log_data = match.groupdict()

        # Try access log format
        if not log_data:
            match = ACCESS_LOG_PATTERN.match(line)
            if match:
                access_data = match.groupdict()
                log_data = {
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    "severity": access_data["severity"].upper(),
                    "service": "api-access",
                    "message": f'{access_data["method"]} {access_data["path"]} '
                               f'Status:{access_data["status_code"]}'
                }

        # If no pattern matched, skip line
        if not log_data:
            continue

        try:
            timestamp_str = log_data["timestamp"]

            # Handle different timestamp formats
            try:
                dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.strptime(timestamp_str, "%d-%m-%Y %H:%M:%S")

            iso_timestamp = dt.isoformat() + "Z"

            # Normalize severity
            severity = log_data["severity"].upper()
            if severity not in SUPPORTED_LEVELS:
                severity = "INFO"

            service = log_data["service"].strip()
            message = log_data["message"].strip()

            # Append normalized log
            normalized_logs.append({
                "timestamp": iso_timestamp,
                "severity": severity,
                "service": service,
                "message": message
            })

        except Exception:
            # Skip if parsing fails
            continue

    return normalized_logs


def classify_log(message: str) -> str:
    """
    Classifies logs into categories based on keywords in the message
    """

    if not message:
        return "UNCATEGORIZED"

    msg = message.lower()

    # Security related logs
    if any(keyword in msg for keyword in [
        "login",
        "authentication",
        "authorization",
        "token",
        "permission",
        "access denied",
        "unauthorized",
        "intrusion",
        "firewall",
        "bruteforce",
        "invalid password"
    ]):
        return "SECURITY"

    # Infrastructure related logs
    if any(keyword in msg for keyword in [
        "cpu",
        "memory",
        "disk",
        "node",
        "container",
        "pod",
        "server",
        "network",
        "latency",
        "throughput",
        "timeout",
        "unreachable"
    ]):
        return "INFRASTRUCTURE"

    # Audit & compliance logs
    if any(keyword in msg for keyword in [
        "audit",
        "compliance",
        "policy",
        "trail",
        "record",
        "change",
        "updated",
        "deleted",
        "created"
    ]):
        return "AUDIT"

    # Application related logs
    if any(keyword in msg for keyword in [
        "exception",
        "error",
        "failed",
        "request",
        "response",
        "null",
        "invalid",
        "crash",
        "stacktrace"
    ]):
        return "APPLICATION"

    # Default category
    return "UNCATEGORIZED"