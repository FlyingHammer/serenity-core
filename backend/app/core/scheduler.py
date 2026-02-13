from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import settings
from app.core.scanner import scan_all
from app.core.settings_store import get_settings
from app.storage.database import SessionLocal

scheduler = BackgroundScheduler()


def start_scheduler():
    def _job():
        db = SessionLocal()
        try:
            scan_all(db, get_settings(db))
        finally:
            db.close()

    scheduler.add_job(_job, "interval", seconds=settings.scheduler_interval_seconds, id="scan_job", replace_existing=True)
    scheduler.start()
