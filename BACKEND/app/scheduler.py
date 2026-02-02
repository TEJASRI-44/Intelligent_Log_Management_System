from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.database import SessionLocal
from app.services.log_retention_service import archive_files_by_retention


def run_log_retention():
    db = SessionLocal()
    try:
        count = archive_files_by_retention(db)
        print(f"[LOG RETENTION] Archived {count} files")
    except Exception as e:
        print(f"[LOG RETENTION ERROR] {e}")
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()

    # Run every day at 2:00 AM
    scheduler.add_job(
        run_log_retention,
        CronTrigger(hour=2, minute=0),
        id="log_retention_job",
        replace_existing=True
    )

    scheduler.start()
    print("[SCHEDULER] Log retention scheduler started")
