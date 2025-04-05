import mysql.connector

class MySQLConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="ecommerce-ibmec.mysql.database.azure.com",
            user="grupo",
            password="administrador99*",
            database="ecommerce"
        ) 