from aiogram.utils import executor
from filters.start import notify_on_startup


async def on_startup(dispatcher):
    await notify_on_startup(dispatcher)


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
