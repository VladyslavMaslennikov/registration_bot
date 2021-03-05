from dateutil import parser
from datetime import datetime


class DateHelper(object):
    @staticmethod
    def check_busy_hours(start: str, end: str):
        start_date = parser.parse(start)
        end_date = parser.parse(end)
        busy_hours = [x for x in range(start_date.hour, end_date.hour)]
        return busy_hours

    @staticmethod
    def return_available_hours(busy_hours: list):
        available_hours = [x for x in range(10, 19)]  # working hours 10:00 - 19:00
        for hour in busy_hours:
            if hour in available_hours:
                available_hours.remove(hour)
        return available_hours

    @staticmethod
    def day_is_correct(date: datetime):
        today = datetime.now()
        if today < date:
            return True
        else:
            return False

    @staticmethod
    def get_date_from_string(date: str):
        decoded_date = parser.parse(date)
        return decoded_date

    @staticmethod
    def get_formatted_date(date: str, hour: int) -> str:
        dt = DateHelper.get_date_from_string(date)
        month = f"{dt.month}" if dt.month > 9 else f"0{dt.month}"
        day = f"{dt.day}" if dt.day > 9 else f"0{dt.day}"
        res = f"{day}.{month}.{dt.year} {hour}:00"
        return res
