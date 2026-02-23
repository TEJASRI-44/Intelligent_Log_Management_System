from sqlalchemy.orm import Session
import json
import csv
import io

from app.services.log_parsers.text_parser import parse_text_logs
from app.services.log_parsers.csv_parser import parse_csv_logs
from app.services.log_parsers.json_parser import parse_json_logs
from app.services.log_parsers.xml_parser import parse_xml_logs


def parse_logs_by_format(
    db: Session,
    file_id: int,
    raw_text: str
) -> int:
    """
    Detects log format based on content and routes to the correct parser.

    Instead of relying on format_id from the database,
    we inspect the raw file content and decide dynamically.
    """

    if not raw_text or not raw_text.strip():
        raise ValueError("Empty log file")

    stripped = raw_text.lstrip()

    # Try JSON Detection ----
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            json.loads(stripped)
            return parse_json_logs(db, file_id, raw_text)
        except json.JSONDecodeError:
            pass  # Not valid JSON, continue checking

    # Try XML Detection ----
    # XML usually starts with <tag>
    if stripped.startswith("<"):
        try:
            import xml.etree.ElementTree as ET
            ET.fromstring(stripped)
            return parse_xml_logs(db, file_id, raw_text)
        except ET.ParseError:
            pass  # Not valid XML

    # Try CSV Detection ----
    # If multiple lines contain commas in consistent pattern
    try:
        sample = io.StringIO(raw_text)
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample.read(1024))
        sample.seek(0)
        reader = csv.reader(sample, dialect)
        rows = list(reader)

        
        if len(rows) > 1:
            column_count = len(rows[0])
            if all(len(row) == column_count for row in rows):
                return parse_csv_logs(db, file_id, raw_text)
    except Exception:
        pass  # Not CSV

    # Fallback to TEXT ----
    # If none of the structured formats match, treat as plain text logs
    return parse_text_logs(db, file_id, raw_text)