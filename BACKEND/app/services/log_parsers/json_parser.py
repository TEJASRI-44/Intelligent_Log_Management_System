import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.log_categories import LogCategory
from app.services.log_parser import classify_log

def parse_json_logs(db: Session, file_id: int, raw_text: str):
    inserted = 0
    skipped = 0
    
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON file: {str(e)}")

    # Determine logs structure
    if isinstance(parsed, dict) and "logs" in parsed:
        logs = parsed["logs"]
    elif isinstance(parsed, list):
        logs = parsed
    else:
        raise Exception("Unsupported JSON format. Expected 'logs' array.")

    if not isinstance(logs, list):
        raise Exception("'logs' must be a list")

    total_logs = len(logs)

    for log in logs:

        # Must be dict
        if not isinstance(log, dict):
            skipped += 1
            continue

        # Validate required fields
        if not log.get("timestamp") or not log.get("severity") or not log.get("message"):
            skipped += 1
            continue

        try:
            timestamp = datetime.fromisoformat(
                log.get("timestamp").replace("Z", "+00:00")
            )
        except Exception:
            skipped += 1
            continue

        try:
            severity = db.query(LogSeverity).filter(
                LogSeverity.severity_code == log.get("severity")
            ).first()

            category_name = classify_log(log.get("message"))
            category = db.query(LogCategory).filter(
                LogCategory.category_name == category_name
            ).first()

            entry = LogEntry(
                file_id=file_id,
                log_timestamp=timestamp,
                severity_id=severity.severity_id if severity else None,
                category_id=category.category_id if category else None,
                service_name=log.get("service"),
                message=log.get("message"),
                raw_log=json.dumps(log)
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

    return round(parsed_percentage, 2)
