import mysql.connector
from mysql.connector import Error

def init_database():
    try:
        # First, connect without database to create it
        connection = mysql.connector.connect(
            host="ecommerce-ibmec.mysql.database.azure.com",
            user="grupo",
            password="administrador99*"
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce")
            
            # Switch to the ecommerce database
            cursor.execute("USE ecommerce")
            
            # Create tables
            # Usuario table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    dtNascimento DATETIME NOT NULL,
                    CPF VARCHAR(14) NOT NULL,
                    Telefone VARCHAR(20) NOT NULL
                )
            """)
            
            # TipoEndereco table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tipo_endereco (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tipo VARCHAR(50) NOT NULL
                )
            """)
            
            # Endereco table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS endereco (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    logradouro VARCHAR(100) NOT NULL,
                    complemento VARCHAR(100),
                    bairro VARCHAR(50) NOT NULL,
                    cidade VARCHAR(50) NOT NULL,
                    estado CHAR(2) NOT NULL,
                    id_tp_endereco INT NOT NULL,
                    id_usuario INT NOT NULL,
                    FOREIGN KEY (id_tp_endereco) REFERENCES tipo_endereco(id),
                    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
                )
            """)
            
            # CartaoCredito table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cartao_credito (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    numero VARCHAR(16) NOT NULL,
                    dtExpiracao DATETIME NOT NULL,
                    cvv VARCHAR(4) NOT NULL,
                    saldo DECIMAL(10,2) NOT NULL,
                    id_usuario_cartao INT NOT NULL,
                    FOREIGN KEY (id_usuario_cartao) REFERENCES usuario(id)
                )
            """)
            
            connection.commit()
            print("Database and tables created successfully!")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.") 