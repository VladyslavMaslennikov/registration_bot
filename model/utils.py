from loader_model import db
from helpers.date_helper import DateHelper


def get_description(user_id: int):
    client = db.get_client(user_id)
    date = DateHelper.get_formatted_date(client[3], client[4]) + f"-{client[5]}:00"
    phone = client[1]
    name = client[6]
    deposit = "Нет" if client[7] == 0 else "Да"
    res = f"Имя: {name}\nТелефон: {phone}\nДата записи: {date}\nЗалог внесен: {deposit}"
    return res
