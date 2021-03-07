class Dialog(object):
    welcome_message = """
Привет \U0001F44B. 

Открывай /menu и выбирай что интересует \U0001F60E:
    • Записывайся на сеанс
    • Отменяй запись, если нужно
    • Узнай правила ухода за тату
    • Свяжись со мной, если будут вопросы   
    """
    opening_menu = "Открываю Меню..."
    opening_calendar = "Открываю календарь..."
    pick_date = "Выбери дату"
    you_picked_day = "Ты выбрал"
    pick_hour = "Выбери время"
    you_picked_hour = "Ты выбрал время на"
    enter_phone = ":00. Введи номер телефона"
    pick_another_day = "Пожалуйста, выбери другой день"
    no_available_date = "Нет свободной записи. Пожалуйста, выбери другой день"
    enter_name = "Введи имя и фамилию"
    thanks_for_registration = "Спасибо за регистрацию. Я напишу тебе в ближайшее время."
    name_desc = "Имя и фамилия:"
    phone_desc = "Телефон:"
    date_desc = "Дата записи:"
    already_have_appointment = "К сожалению, ты можешь записаться только на один прием."
    no_appointment_for_you = "Ns не записан на сеанс в ближайшее время."
    cancellation_success = "Запись успешно отменена."
    new_clients_are = "Новые клиенты:"
    no_new_appointments = "Нет новых записей за выбранную дату."
    enter_integer = "Введи целое число."
    enter_day_number_for_statistics = "Введи кол-во дней за которые хочешь увидеть статистику."
    menu_inline_description = "Меню для записи и другая информация"
    tattoo_care_info = """
    1. После нанесения татуировки мастер заклеит работу специализированной пленкой “Супрасорб Ф”
 ✧ Пленку следует носить 5 дней;
 ✧Место под пленкой не должно потеть (исключить физические нагрузки и горячие ванны, открытые водоемы, только душ);
 ✧Не нарушайте целостности пленки (не прокалывайте, ничем не обматывайте)!
 ✧В течение первых суток возможно накопление сукровицы (лимфы) и краски — это нормально.

 2. Через 5 дней после фиксации пленку необходимо снять ✧Подденьте край пленки, зацепите его и максимально оттяните в 
 сторону, сохраняя пленку постоянно растянутой, продолжайте снимать; ✧После удаления пленки промойте татуировку 
 жидким мылом без использования мочалки и другого агрессивного воздействия. 

 3. Последующие две недели после удавления пленки не забывайте мазать татуировку кремами для заживления и ухода.
    """
    my_link = "Мой линк - @Odona"
    # menu options
    book_session = "\U0001F4DD Записаться на сеанс"
    tattoo_care = "\U0001F481 Уход за тату"
    how_to_get = "\U0001F4CD Контакты"
    cancel_session = "\U0001F645 Отменить запись"
    show_calendar_sessions = "\U0001F4C6 Открыть календарь"
