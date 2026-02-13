from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.schemas import AppSettings
from app.storage.models import SettingsRecord


SETTINGS_KEY = "app_settings"


def get_settings(db: Session) -> AppSettings:
    row = db.execute(select(SettingsRecord).where(SettingsRecord.name == SETTINGS_KEY)).scalar_one_or_none()
    if not row:
        default = AppSettings()
        db.add(SettingsRecord(name=SETTINGS_KEY, payload=default.model_dump()))
        db.commit()
        return default
    return AppSettings(**row.payload)


def save_settings(db: Session, settings: AppSettings) -> AppSettings:
    row = db.execute(select(SettingsRecord).where(SettingsRecord.name == SETTINGS_KEY)).scalar_one_or_none()
    if not row:
        row = SettingsRecord(name=SETTINGS_KEY, payload=settings.model_dump())
        db.add(row)
    else:
        row.payload = settings.model_dump()
    db.commit()
    return settings
