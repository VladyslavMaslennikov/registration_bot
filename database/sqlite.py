import sqlite3


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
        user_name TEXT NOT NULL,
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

    def add_client(self, user_id: int, phone: str, creation_date: str, registration_date: str, user_name: str):
        user_exists = self.get_client(user_id)
        if user_exists:
            print("Client already exists")
            return False
        else:
            sql = """
            INSERT INTO Clients(user_id, phone, creation_date, registration_date, user_name) VALUES (?, ?, ?, ?, ?)
            """
            parameters = (user_id, phone, creation_date, registration_date, user_name)
            self.execute(sql, parameters=parameters, commit=True)
            return True

    def get_all_clients(self):
        return self.execute("SELECT phone FROM Clients", fetchAll=True)
