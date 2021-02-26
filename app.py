from aiogram.utils import executor

from helpers.google_api import list_events, get_calendar_call_main

if __name__ == '__main__':
    # list_events()
    # get_calendar_call_main()
    from handlers import dp
    executor.start_polling(dp)
