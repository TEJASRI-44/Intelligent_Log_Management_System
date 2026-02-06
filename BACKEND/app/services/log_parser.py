import re
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.log_categories import LogCategory


# Example supported log:
# 2026-01-13 10:22:31 ERROR auth-service Failed login

LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<severity>DEBUG|INFO|WARN|ERROR|FATAL)\s+"
    r"(?P<service>\S+)\s+"
    r"(?P<message>.+)"
)


def clean_log_lines(raw_text: str) -> list[str]:
    """
    Removes empty lines, whitespace, and duplicate lines
    """
    cleaned = []
    seen = set()

    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line in seen:
            continue
        seen.add(line)
        cleaned.append(line)

    return cleaned


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

