import json
import re
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.log_categories import LogCategory
from app.services.log_parser import classify_log
from app.services.log_parser import clean_log_lines
from app.models.environments import Environment


LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<severity>DEBUG|INFO|WARN|ERROR|FATAL)\s+"
    r"(?P<service>\S+)\s+"
    r"(?P<message>.+)"
)
def extract_env_host(message: str):
    env_match = re.search(r'env=([\w-]+)', message)
    host_match = re.search(r'host=([\w.-]+)', message)

    environment_code = env_match.group(1).upper() if env_match else "LOCAL"
    host = host_match.group(1) if host_match else "unknown-host"

    return environment_code, host


def parse_text_logs(db: Session, file_id: int, raw_text: str):
    inserted = 0
    skipped=0
    parsed_percentage=0.0
    cleaned_lines = clean_log_lines(raw_text)
    
    for log in  cleaned_lines:
        

        data = log
        timestamp_text =data["timestamp"]
        severity = db.query(LogSeverity).filter(
            LogSeverity.severity_code == data["severity"]
        ).first()

        category_name = classify_log(data["message"])
        category = db.query(LogCategory).filter(
            LogCategory.category_name == category_name
        ).first()
        
        environment_code, host_name = extract_env_host(data["message"])
        environment = db.query(Environment).filter(
            Environment.environment_code == environment_code
        ).first()

        if not environment:
            environment = db.query(Environment).filter(
                Environment.environment_code == "LOCAL"
            ).first()


        entry = LogEntry(
            file_id=file_id,
            log_timestamp = datetime.fromisoformat(
                timestamp_text.strip().replace("Z", "+00:00")
            ),
            severity_id=severity.severity_id if severity else None,
            category_id=category.category_id if category else None,
            environment_id=environment.environment_id if environment else "LOCAL",
            service_name=data["service"],
            host_name=host_name,
            message=data["message"],
            raw_log=json.dumps(log)
        )

        db.add(entry)
        inserted += 1
         

    db.commit()
    parsed_percentage=(inserted/(inserted+skipped))*100 if (inserted+skipped)>0 else 0
    return round(parsed_percentage, 2)
   
