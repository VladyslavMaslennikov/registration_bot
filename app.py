from aiogram.utils import executor

from handlers import dp
from handlers.start_handlers import notify_on_startup


async def on_startup(dispatcher):
    await notify_on_startup(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
