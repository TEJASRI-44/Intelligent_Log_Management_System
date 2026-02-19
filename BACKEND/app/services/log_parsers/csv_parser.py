import csv
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.log_categories import LogCategory
from app.services.log_parser import classify_log
from app.services.log_parser import clean_log_lines
import re
import json
from app.models.environments import Environment
def extract_env_host(message: str):
    env_match = re.search(r'env=([\w-]+)', message)
    host_match = re.search(r'host=([\w.-]+)', message)

    environment_code = env_match.group(1).upper() if env_match else "LOCAL"
    host = host_match.group(1) if host_match else "unknown-host"

    return environment_code, host


def parse_csv_logs(db: Session, file_id: int, raw_text: str):

    cleaned_lines = clean_log_lines(raw_text)
    reader = csv.DictReader(cleaned_lines)

    inserted = 0
    skipped = 0

    rows = list(reader)
    total_logs = len(rows)
    local_env = db.query(Environment).filter(
        Environment.environment_code == "LOCAL"
    ).first()
    for row in rows:
        try:
            timestamp_text = row.get("timestamp")
            level = row.get("severity")
            service = row.get("service")
            message = row.get("message")

            # Required fields check (same pattern as XML)
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
            environment_code, host_name = extract_env_host(message.strip())

           
            environment = db.query(Environment).filter(
                Environment.environment_code == environment_code
            ).first()

            if not environment:
                environment = local_env

            entry = LogEntry(
                file_id=file_id,
                log_timestamp=timestamp,
                severity_id=severity.severity_id,
                category_id=category.category_id if category else None,
                environment_id=environment.environment_id if environment else None,
                service_name=service.strip() if service else None,
                host_name=host_name,
                message=message.strip(),
                raw_log=",".join(row.values())
            )

            db.add(entry)
            inserted += 1

        except Exception:
            skipped += 1
            continue

    db.commit()
    parsed_percentage=(inserted/(inserted+skipped))*100 if (inserted+skipped)>0 else 0
    return round(parsed_percentage, 2)
