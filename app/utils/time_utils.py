from zoneinfo import ZoneInfo
from datetime import datetime, date, timedelta

LIMA = ZoneInfo('America/Lima')

def peru_now():
    return datetime.now(LIMA).replace(tzinfo=None)

def peru_today():
    return peru_now().date()
