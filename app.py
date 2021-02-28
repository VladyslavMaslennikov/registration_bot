from aiogram.utils import executor
from filters.start import on_startup


# add to start_polling on_startup=
async def on_launch(dispatcher):
    await on_startup(dispatcher)


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)
