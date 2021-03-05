import sqlite3
from datetime import datetime, timedelta
from helpers.date_helper import DateHelper


class Database:
    path_to_db = "data/main.db"

    def __int__(self, path="data/main.db"):
        self.path_to_db = path

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchOne=False, fetchAll=False, commit=False):
        connection = self.connection
        cursor = connection.cursor()
        if not parameters:
            parameters = tuple()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchOne:
            data = cursor.fetchone()
        if fetchAll:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table(self):
        sql = """
        CREATE TABLE Clients (
        user_id INTEGER NOT NULL,
        phone TEXT NOT NULL,
        creation_date TEXT NOT NULL,
        registration_date TEXT NOT NULL,
        session_start INTEGER NOT NULL,
        session_end INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        has_deposit INTEGER NOT NULL,
        PRIMARY KEY (user_id)
        );
        """
        return self.execute(sql, commit=True)

    def get_client(self, user_id: int):
        sql = """
        SELECT * FROM Clients WHERE user_id = ?
        """
        parameters = (user_id,)
        return self.execute(sql, parameters=parameters, fetchOne=True)

    def add_client(self, user_id: int, phone: str, creation_date: str,
                   registration_date: str, start: int, end: int, user_name: str, deposit: int):
        user_exists = self.get_client(user_id)
        if user_exists:
            print("Client already exists")
            return False
        else:
            sql = """INSERT INTO Clients(user_id, phone, creation_date, registration_date, session_start, 
            session_end, user_name, has_deposit) VALUES (?, ?, ?, ?, ?, ?, ?, ?) """
            parameters = (user_id, phone, creation_date, registration_date, start, end, user_name, deposit)
            self.execute(sql, parameters=parameters, commit=True)
            return True

    def get_all_clients(self):
        return self.execute("SELECT * FROM Clients", fetchAll=True)

    def delete_the_user(self, user_id: int):
        sql = """
                DELETE FROM Clients WHERE user_id = ?
                """
        parameters = (user_id,)
        self.execute(sql, parameters, commit=True)

    def check_if_user_has_appointment(self, user_id: int):
        clients = self.get_all_clients()
        if not clients:
            return False
        client = list(filter(lambda x: x[0] == user_id, clients))
        if not client:
            return False
        client = client[0]
        session_date = client[3]
        session_start = client[4]
        dt = DateHelper.get_date_from_string(session_date)
        registration_date = datetime(dt.year, dt.month, dt.day, int(session_start))
        current_date = datetime.now()
        if registration_date < current_date:
            self.delete_the_user(user_id)
            return False
        if registration_date > current_date:
            return True
        return False

    def clear_database(self):
        self.execute("DELETE FROM Clients", commit=True)

    def get_newly_registered_clients(self, delta: int):
        clients = self.get_all_clients()
        current_date = datetime.now()
        lower_date = current_date - timedelta(days=delta)
        if not clients:
            return None
        else:
            new_clients = ""
            for client in clients:
                creation_date = DateHelper.get_date_from_string(client[2])
                if lower_date < creation_date < current_date:
                    name = client[6]
                    phone = client[1]
                    dt = DateHelper.get_date_from_string(client[3])

                    month = f"{dt.month}" if dt.month > 9 else f"0{dt.month}"
                    day = f"{dt.day}" if dt.day > 9 else f"0{dt.day}"
                    registered = f"{day}.{month}.{dt.year} {client[4]}:00-{client[5]}:00"
                    client_desc = f"Имя: {name}, телефон: {phone}, дата записи: {registered}\n"
                    print(client_desc)
                    new_clients += client_desc
            return new_clients

    def find_all_events_for_day(self, dt: datetime):
        all_busy_hours = []
        all_clients = self.get_all_clients()
        for client in all_clients:
            date = DateHelper.get_date_from_string(client[3])
            if date.year == dt.year and date.month == dt.month and date.day == dt.day:
                start = client[4]
                end = client[5]
                all_busy_hours + DateHelper.check_busy_hours(start, end)
        print(f"Busy hours for the day: {all_busy_hours}")
        available_hours = DateHelper.return_available_hours(all_busy_hours)
        print(f"Available hours are: {available_hours}")
        return available_hours

    def find_all_events_in_range(self):
        lower = datetime.now()
        upper = datetime(lower.year + 1, lower.month, lower.day)
        all_clients = self.get_all_clients()
        filtered = []
        for client in all_clients:
            date = DateHelper.get_date_from_string(client[3])
            if lower < date < upper:
                filtered.append(client)
        return filtered
