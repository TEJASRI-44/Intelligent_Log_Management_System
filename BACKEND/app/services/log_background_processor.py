from sqlalchemy.orm import Session
from app.database import SessionLocal

from app.models.raw_files import RawFile
from app.services.upload_status_service import get_status_id
from app.services.file_reader import read_file_from_appwrite
from app.services.log_parsers.parser_router import parse_logs_by_format


from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.raw_files import RawFile
from app.services.upload_status_service import get_status_id
from app.services.file_reader import read_file_from_appwrite
from app.services.log_parsers.parser_router import parse_logs_by_format
from datetime import datetime

def process_uploaded_file(file_id: int):
    db: Session = SessionLocal()

    try:
        # 1️⃣ Fetch metadata
        raw_file = (
            db.query(RawFile)
            .filter(
                RawFile.file_id == file_id,
                RawFile.is_deleted == False
            )
            .first()
        )

        if not raw_file or not raw_file.storage_path:
            raise Exception("Raw file or storage reference missing")

        # 2️⃣ Mark PROCESSING
        raw_file.status_id = get_status_id(db, "PROCESSING")
        db.commit()

        # 3️⃣ Read from Appwrite
        raw_text = read_file_from_appwrite(raw_file.storage_path)

        if not raw_text.strip():
            raise Exception("File content is empty")

        print("📄 First 3 lines of file:")
        for line in raw_text.splitlines()[:3]:
            print("   ", line)

        # 4️⃣ Parse logs
        inserted_count = parse_logs_by_format(
            db=db,
            file_id=raw_file.file_id,
            format_id=raw_file.format_id,
            raw_text=raw_text
        )

        # 5️⃣ Mark PARSED
        raw_file.status_id = get_status_id(db, "PARSED")
        db.commit()

        print(f"✅ File {file_id} parsed successfully | Logs inserted: {inserted_count}")

    except Exception as e:
        db.rollback()

        try:
            raw_file.status_id = get_status_id(db, "FAILED")
            db.commit()
        except:
            pass

        print("❌ Background processing failed:", str(e))

    finally:
        db.close()
