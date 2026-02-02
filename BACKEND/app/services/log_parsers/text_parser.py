import re
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.log_categories import LogCategory
from app.services.log_parser import classify_log

LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<severity>DEBUG|INFO|WARN|ERROR|FATAL)\s+"
    r"(?P<service>\S+)\s+"
    r"(?P<message>.+)"
)

def parse_text_logs(db: Session, file_id: int, raw_text: str):
    inserted = 0

    for line in raw_text.splitlines():
        match = LOG_PATTERN.match(line.strip())
        if not match:
            continue

        data = match.groupdict()

        severity = db.query(LogSeverity).filter(
            LogSeverity.severity_code == data["severity"]
        ).first()

        category_name = classify_log(data["message"])
        category = db.query(LogCategory).filter(
            LogCategory.category_name == category_name
        ).first()

        entry = LogEntry(
            file_id=file_id,
            log_timestamp=datetime.strptime(
                data["timestamp"], "%Y-%m-%d %H:%M:%S"
            ),
            severity_id=severity.severity_id if severity else None,
            category_id=category.category_id if category else None,
            service_name=data["service"],
            message=data["message"],
            raw_log=line
        )

        db.add(entry)
        inserted += 1

    db.commit()
    print(f"✅ TEXT logs inserted: {inserted}")
