import xml.etree.ElementTree as ET
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.log_categories import LogCategory
from app.services.log_parser import classify_log
import re
from app.models.environments import Environment

# Extract environment and host from log message
def extract_env_host(message: str):
    env_match = re.search(r'env=([\w-]+)', message)
    host_match = re.search(r'host=([\w.-]+)', message)

    # Use defaults if not present in message
    environment_code = env_match.group(1).upper() if env_match else "LOCAL"
    host = host_match.group(1) if host_match else "unknown-host"

    return environment_code, host


def parse_xml_logs(db: Session, file_id: int, raw_text: str):

    # Try parsing XML content
    try:
        root = ET.fromstring(raw_text.strip())
    except ET.ParseError:
        return {
            "error": "Invalid XML format"
        }

    inserted = 0
    skipped = 0

    # Find all <log> elements
    logs = root.findall("log")
    total_logs = len(logs)

    # Get LOCAL environment as fallback
    local_env = db.query(Environment).filter(
        Environment.environment_code == "LOCAL"
    ).first()

    for log in logs:
        try:
            # Extract values from XML tags
            timestamp_text = log.findtext("timestamp")
            severity = log.findtext("severity")
            service = log.findtext("service")
            message = log.findtext("message")

            # Check required fields
            if not timestamp_text or not severity or not message:
                skipped += 1
                continue

            # Parse timestamp safely
            try:
                timestamp = datetime.fromisoformat(
                    timestamp_text.strip().replace("Z", "+00:00")
                )
            except Exception:
                skipped += 1
                continue

            # Validate severity from DB
            severity = db.query(LogSeverity).filter(
                LogSeverity.severity_code == severity.strip()
            ).first()

            if not severity:
                skipped += 1
                continue

            # Classify category based on message
            category_name = classify_log(message.strip())
            category = db.query(LogCategory).filter(
                LogCategory.category_name == category_name
            ).first()

            # Extract environment and host
            environment_code, host_name = extract_env_host(message.strip())
            environment = db.query(Environment).filter(
                Environment.environment_code == environment_code
            ).first()

            # If environment not found, fallback to LOCAL
            if not environment:
                environment = local_env

            # Create log entry
            entry = LogEntry(
                file_id=file_id,
                log_timestamp=timestamp,
                severity_id=severity.severity_id,
                category_id=category.category_id if category else None,
                environment_id=environment.environment_id if environment else None,
                service_name=service.strip() if service else None,
                host_name=host_name,
                message=message.strip(),
                raw_log=ET.tostring(log, encoding="unicode")
            )

            db.add(entry)
            inserted += 1

        except Exception:
            # Skip this log if any unexpected error occurs
            skipped += 1
            continue

    db.commit()

    # Calculate parsing success percentage
    parsed_percentage = (
        (inserted / (inserted + skipped)) * 100
        if (inserted + skipped) > 0 else 0
    )

    return round(parsed_percentage, 2)