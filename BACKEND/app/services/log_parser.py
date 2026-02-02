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

    # 🔐 Security related logs
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

    # 🖥 Infrastructure related logs
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

    # 📝 Audit & compliance logs
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

    # ⚙️ Application related logs
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



def parse_and_store_logs(
    db: Session,
    file_id: int,
    raw_text: str
):
    """
    Clean → Parse → Categorize → Insert into log_entries
    """
     
    cleaned_lines = clean_log_lines(raw_text)

    for line in cleaned_lines:
        match = LOG_PATTERN.match(line)
        if not match:
            print("❌ REGEX FAILED:", line)
            continue
        print("✅ REGEX MATCHED:", line)

        data = match.groupdict()

        log_time = datetime.strptime(
            data["timestamp"], "%Y-%m-%d %H:%M:%S"
        )

        severity = db.query(LogSeverity).filter(
            LogSeverity.severity_code == data["severity"]
        ).first()

        category_name = classify_log(data["message"])
        category = db.query(LogCategory).filter(
            LogCategory.category_name == category_name
        ).first()

        log_entry = LogEntry(
            file_id=file_id,
            log_timestamp=log_time,
            severity_id=severity.severity_id if severity else None,
            category_id=category.category_id if category else None,
            service_name=data["service"],
            message=data["message"],
            raw_log=line
        )

        db.add(log_entry)

    db.commit()
