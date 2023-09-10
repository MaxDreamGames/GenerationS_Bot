import pyodbc

class Connection:
    con = None
    cursor = None
    def __init__(self, server, database):
        try:
            connection_string = f'DRIVER=SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes'
            self.con = pyodbc.connect(connection_string)
            self.cursor = self.con.cursor()
            print("Connected to database")
        except pyodbc.Error:
            print("Connection error")

    def connect(self, server, database):
        try:
            connection_string = f'DRIVER=SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes'
            self.con = pyodbc.connect(connection_string)
            self.cursor = self.con.cursor()
            print("Connected to database")
        except pyodbc.Error:
            print("Connection error")

    def insert(self, last_name, first_name, country, region, city, school, email, phone, password, personal_number):
        try:
            query = """INSERT INTO Accounts(last_name, first_name, country, region, city, school, email, phone, pass, personal_number)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            values = (last_name, first_name, country, region, city, school, email, phone, password, personal_number)
            self.cursor.execute(query, values)
            self.con.commit()
            print("Insert successful")
        except pyodbc.Error as e:
            print(f"Insert error: {e}")


    def search(self, table, column, value):
        try:
            query = f"SELECT * FROM {table} WHERE {column} = ?"
            self.cursor.execute(query, (value,))
            result = self.cursor.fetchone()
            return result
        except pyodbc.Error as e:
            print(f"Search error: {e}")
            return None

    def request(self, request):
        try:
            self.cursor.execute(request)

            return self.cursor.fetchone()
        except pyodbc.Error as e:
            print(f"Request error: {e}")
            return None

    def insertCountry(self, request):
        try:
            self.cursor.execute(request)
            self.cursor.commit()
        except pyodbc.Error as e:
            print(f"Request error: {e}")

    def select(self, table):
        try:
            cur = self.cursor.execute(f"SELECT * FROM {table}")
            for account in self.cursor.fetchall():
                print(account)
            return cur.fetchall()
        except pyodbc.Error as e:
            print(f"Select error: {e}")
            return None

    def close(self):
        self.cursor.close()
        self.con.close()
#
# if __name__ == '__main__':
#     connection = Connection('DESKTOP-VONE3CS\SQLEXPRESS', 'GenerateS_Database')
#     connection.insert('Doe', 'John', 'USA', 'CA', 'Los Angeles', 'School 123', 'johndoe@example.com', 'password123', '123456')
#     connection.select()
#     connection.close()
