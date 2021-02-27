from datetime import datetime, timezone
from helpers.google_api import create_new_event, find_all_events_for_day

from aiogram.utils import executor
from helpers.date_functions import check_busy_hours

if __name__ == '__main__':
    # create_new_event(datetime.now())
    # start = "2021-02-27T11:00:00+02:00"
    # end = "2021-02-27T13:00:00+02:00"
    # print(check_busy_hours(start, end))
    # find_all_events_for_day(datetime.now())
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)
