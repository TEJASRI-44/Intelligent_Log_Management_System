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

# Extract environment and host from log message
def extract_env_host(message: str):
    env_match = re.search(r'env=([\w-]+)', message)
    host_match = re.search(r'host=([\w.-]+)', message)

    # Default to LOCAL and unknown-host if not found
    environment_code = env_match.group(1).upper() if env_match else "LOCAL"
    host = host_match.group(1) if host_match else "unknown-host"

    return environment_code, host


def parse_csv_logs(db: Session, file_id: int, raw_text: str):

    inserted = 0
    skipped = 0

    # Read CSV content line by line
    reader = csv.DictReader(raw_text.splitlines())

    # Get LOCAL environment as fallback
    local_env = db.query(Environment).filter(
        Environment.environment_code == "LOCAL"
    ).first()

    for row in reader:
        try:
            # Extract required fields from CSV row
            timestamp_text = (row.get("timestamp") or "").strip()
            severity_value = (row.get("severity") or "").strip().upper()
            service = (row.get("service") or "").strip()
            message = (row.get("message") or "").strip()

            # Skip if required fields are missing
            if not timestamp_text or not severity_value or not message:
                skipped += 1
                continue

            # Convert timestamp to datetime
            try:
                timestamp = datetime.fromisoformat(
                    timestamp_text.replace("Z", "+00:00")
                )
            except Exception:
                skipped += 1
                continue

            # Normalize some severity values
            severity_mapping = {
                "WARNING": "WARN",
                "CRITICAL": "ERROR"
            }

            severity_value = severity_mapping.get(severity_value, severity_value)

            # Fetch severity from DB
            severity = db.query(LogSeverity).filter(
                LogSeverity.severity_code.ilike(severity_value)
            ).first()

            if not severity:
                skipped += 1
                continue

            # Classify log category based on message
            category_name = classify_log(message)
            category = db.query(LogCategory).filter(
                LogCategory.category_name == category_name
            ).first()

            # Create category if it does not exist
            if not category:
                category = LogCategory(category_name=category_name)
                db.add(category)
                db.commit()
                db.refresh(category)

            # Extract environment and host
            environment_code, host_name = extract_env_host(message)

            environment = db.query(Environment).filter(
                Environment.environment_code == environment_code
            ).first()

            # If environment not found, use LOCAL
            if not environment:
                environment = local_env

            # Create new log entry
            entry = LogEntry(
                file_id=file_id,
                log_timestamp=timestamp,
                severity_id=severity.severity_id,
                category_id=category.category_id if category else None,
                environment_id=environment.environment_id if environment else None,
                service_name=service,
                host_name=host_name,
                message=message,
                raw_log=",".join(row.values())
            )

            db.add(entry)
            inserted += 1

        except Exception as e:
            # If any unexpected error happens, skip that row
            print("CSV PARSE ERROR:", e)
            skipped += 1

    db.commit()

    # Calculate parsing success percentage
    total = inserted + skipped
    parsed_percentage = (inserted / total) * 100 if total > 0 else 0

    return round(parsed_percentage, 2)