import xml.etree.ElementTree as ET
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.log_categories import LogCategory
from app.services.log_parser import classify_log


def parse_xml_logs(db: Session, file_id: int, raw_text: str):

    try:
        root = ET.fromstring(raw_text.strip())
    except ET.ParseError:
        return {
            "error": "Invalid XML format"
        }

    inserted = 0
    skipped = 0

    logs = root.findall("log")
    total_logs = len(logs)

    for log in logs:
        try:
            timestamp_text = log.findtext("timestamp")
            level = log.findtext("severity")
            service = log.findtext("service")
            message = log.findtext("message")

            # Required fields check
            if not timestamp_text or not level or not message:
                skipped += 1
                continue

            # Timestamp parsing
            try:
                timestamp = datetime.fromisoformat(
                    timestamp_text.strip().replace("Z", "+00:00")
                )
            except Exception:
                skipped += 1
                continue

            # Validate severity
            severity = db.query(LogSeverity).filter(
                LogSeverity.severity_code == level.strip()
            ).first()

            if not severity:
                skipped += 1
                continue

            # Classify category
            category_name = classify_log(message.strip())
            category = db.query(LogCategory).filter(
                LogCategory.category_name == category_name
            ).first()

            entry = LogEntry(
                file_id=file_id,
                log_timestamp=timestamp,
                severity_id=severity.severity_id,
                category_id=category.category_id if category else None,
                service_name=service.strip() if service else None,
                message=message.strip(),
                raw_log=ET.tostring(log, encoding="unicode")
            )

            db.add(entry)
            inserted += 1

        except Exception:
            skipped += 1
            continue

    db.commit()

    parsed_percentage = (
        (inserted / total_logs) * 100 if total_logs > 0 else 0
    )

    return  round(parsed_percentage, 2)
