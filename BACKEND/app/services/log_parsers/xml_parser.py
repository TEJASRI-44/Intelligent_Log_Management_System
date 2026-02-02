import xml.etree.ElementTree as ET
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.log_categories import LogCategory
from app.services.log_parser import classify_log

def parse_xml_logs(db: Session, file_id: int, raw_text: str):
    root = ET.fromstring(raw_text)
    inserted = 0

    for log in root.findall("log"):
        severity = db.query(LogSeverity).filter(
            LogSeverity.severity_code == log.findtext("level")
        ).first()

        message = log.findtext("message")
        category_name = classify_log(message)
        category = db.query(LogCategory).filter(
            LogCategory.category_name == category_name
        ).first()

        entry = LogEntry(
            file_id=file_id,
            log_timestamp=datetime.fromisoformat(
                log.findtext("timestamp").replace("Z", "+00:00")
            ),
            severity_id=severity.severity_id if severity else None,
            category_id=category.category_id if category else None,
            service_name=log.findtext("service"),
            message=message,
            raw_log=ET.tostring(log, encoding="unicode")
        )

        db.add(entry)
        inserted += 1

    db.commit()
    print(f"✅ XML logs inserted: {inserted}")
