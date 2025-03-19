import mysql.connector
from mysql.connector import Error

class MySQLConnection:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='ibmec-cloud-mall',
                user='root',
                password='admin'
            )
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()