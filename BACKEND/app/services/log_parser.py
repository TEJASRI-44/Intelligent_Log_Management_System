import re
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.log_categories import LogCategory


import re
from datetime import datetime


# Format 1:
# 2026-01-13 10:22:31 ERROR auth-service Failed login
PRIMARY_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>DEBUG|INFO|WARN|ERROR|FATAL)\s+"
    r"(?P<service>\S+)\s+"
    r"(?P<message>.+)"
)

# Format 2:
# 13-01-2026 10:22:31 error auth-service Failed login
ALT_PATTERN = re.compile(
    r"(?P<timestamp>\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>\w+)\s+"
    r"(?P<service>\S+)\s+"
    r"(?P<message>.+)"
)


SUPPORTED_LEVELS = {"DEBUG", "INFO", "WARN", "ERROR", "FATAL"}


def clean_log_lines(raw_text: str) -> list[dict]:
    """
    Cleans raw text logs and converts them into
    internal standardized format.

    Internal Standard Format:
    {
        "timestamp": ISO8601 string,
        "level": uppercase severity,
        "service": string,
        "message": string
    }
    """

    normalized_logs = []
    seen = set()

    for line in raw_text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line in seen:
            continue

        seen.add(line)

        log_data = None

        match = PRIMARY_PATTERN.match(line)
        if match:
            log_data = match.groupdict()

        if not log_data:
            match = ALT_PATTERN.match(line)
            if match:
                log_data = match.groupdict()

        if not log_data:
            continue

        try:


            timestamp_str = log_data["timestamp"]

            try:
                dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.strptime(timestamp_str, "%d-%m-%Y %H:%M:%S")

            iso_timestamp = dt.isoformat() + "Z"


            level = log_data["level"].upper()

            if level not in SUPPORTED_LEVELS:
                level = "INFO" 

            service = log_data["service"].strip()

            message = log_data["message"].strip()


            normalized_logs.append({
                "timestamp": iso_timestamp,
                "level": level,
                "service": service,
                "message": message
            })

        except Exception:
            continue

    return normalized_logs



def classify_log(message: str) -> str:
    """
    Classifies logs into categories based on message content
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

    #  Infrastructure related logs
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

    #  Audit & compliance logs
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

    #  Application related logs
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

    return "UNCATEGORIZED"

