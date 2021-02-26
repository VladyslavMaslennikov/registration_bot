from datetime import datetime, timezone

from aiogram.utils import executor


if __name__ == '__main__':
    from helpers.google_api import create_new_event, find_all_events_for_day
    # create_new_event(datetime.now())
    find_all_events_for_day(datetime.now())

    from handlers import dp
    executor.start_polling(dp, skip_updates=True)
