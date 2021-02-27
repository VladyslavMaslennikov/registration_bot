from dateutil import parser


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
