from filters.admin_filters import ShowUpcomingEventsCommand
from filters.user_filters import CancelCommand, BookSessionCommand, MenuCommand,\
    GetDestinationCommand, GetCareInfoCommand
from loader_model import dp

if __name__ == "filters":
    dp.filters_factory.bind(CancelCommand)
    dp.filters_factory.bind(MenuCommand)
    dp.filters_factory.bind(GetDestinationCommand)
    dp.filters_factory.bind(GetCareInfoCommand)
    dp.filters_factory.bind(ShowUpcomingEventsCommand)