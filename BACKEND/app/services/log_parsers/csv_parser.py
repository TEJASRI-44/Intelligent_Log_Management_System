import csv
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.log_categories import LogCategory
from app.services.log_parser import classify_log
from app.services.log_parser import clean_log_lines

def parse_csv_logs(db: Session, file_id: int, raw_text: str):
    cleaned_lines=clean_log_lines(raw_text)
    reader = csv.DictReader(cleaned_lines)
    inserted = 0

    for row in reader:
        severity = db.query(LogSeverity).filter(
            LogSeverity.severity_code == row["level"]
        ).first()

        category_name = classify_log(row["message"])
        category = db.query(LogCategory).filter(
            LogCategory.category_name == category_name
        ).first()

        entry = LogEntry(
            file_id=file_id,
            log_timestamp=datetime.fromisoformat(
                row["timestamp"].replace("Z", "+00:00")
            ),
            severity_id=severity.severity_id if severity else None,
            category_id=category.category_id if category else None,
            service_name=row["service"],
            message=row["message"],
            raw_log=",".join(row.values())
        )

        db.add(entry)
        inserted += 1

    db.commit()
    print(f" CSV logs inserted: {inserted}")
