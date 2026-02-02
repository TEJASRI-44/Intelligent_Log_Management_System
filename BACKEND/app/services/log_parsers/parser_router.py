from sqlalchemy.orm import Session

from app.services.log_parsers.text_parser import parse_text_logs
from app.services.log_parsers.csv_parser import parse_csv_logs
from app.services.log_parsers.json_parser import parse_json_logs
from app.services.log_parsers.xml_parser import parse_xml_logs


def parse_logs_by_format(
    db: Session,
    file_id: int,
    format_id: int,
    raw_text: str
) -> int:
    """
    Routes log parsing based on file format
    """

    # format_id mapping
    # 1 = TEXT
    # 2 = JSON
    # 3 = CSV
    # 4 = XML

    if format_id == 1:
        return parse_text_logs(db, file_id, raw_text)

    if format_id == 2:
        return parse_json_logs(db, file_id, raw_text)

    if format_id == 3:
        return parse_csv_logs(db, file_id, raw_text)

    if format_id == 4:
        return parse_xml_logs(db, file_id, raw_text)

    raise Exception(f"Unsupported file format_id: {format_id}")
