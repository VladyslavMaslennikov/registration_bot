from dateutil import parser
from datetime import datetime, timedelta


def check_busy_hours(start: str, end: str):
    start_date = parser.parse(start)
    end_date = parser.parse(end)
    busy_hours = [x for x in range(start_date.hour, end_date.hour)]
    return busy_hours


def return_available_hours(busy_hours: list):
    available_hours = [x for x in range(10, 23)]
    for hour in busy_hours:
        if hour in available_hours:
            available_hours.remove(hour)
    return available_hours


def day_is_correct(date: datetime):
    tomorrow = datetime.now() + timedelta(days=1)
    if tomorrow < date:
        return True
    else:
        return False
