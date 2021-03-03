from filters.admin_filters import ShowStatisticsCommand
from filters.user_filters import CancelCommand, BookSessionCommand, MenuCommand
from loader_model import dp

if __name__ == "filters":
    dp.filters_factory.bind(ShowStatisticsCommand)
    dp.filters_factory.bind(CancelCommand)
    dp.filters_factory.bind(MenuCommand)
