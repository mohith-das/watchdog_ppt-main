from config import in_production
from datetime import date, timedelta
import time


if in_production:
    yesterday = date.today() - timedelta(days=1)
else:
    # yesterday = date.today() - timedelta(days=1)
    yesterday = date.today() - timedelta(days=2)
    # yesterday = date.today() - timedelta(days=3)
    # yesterday = date(2021, 3, 31)
    # yesterday = date(2021, 1, 17)
    # yesterday = date(2021, 1, 31)
    # yesterday = date(2021, 3, 7)

sdlw = yesterday - timedelta(days=7)


def get_current_timestamp():
    return int(time.time())


def get_previous_week_start_date_end_date(weekday=6, current_date=date.today()):

    end_date = current_date - timedelta(days=1)
    start_date = end_date - timedelta(days=6)

    while start_date.weekday() != weekday:
        end_date = end_date - timedelta(days=1)
        start_date = end_date - timedelta(days=6)

    return start_date, end_date
