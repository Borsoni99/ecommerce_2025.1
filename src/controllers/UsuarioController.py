from flask import jsonify, request
from models.Usuario import Usuario
from database.mysql_connection import MySQLConnection

class UsuarioController:
    def __init__(self):
        self.db = MySQLConnection()

    def create(self):
        try:
            data = request.json
            usuario = Usuario.from_dict(data)

            cursor = self.db.connection.cursor()
            sql = """INSERT INTO usuario (nome, email, dtNascimento, CPF, Telefone)
                     VALUES (%s, %s, %s, %s, %s)"""
            values = (usuario.nome, usuario.email, usuario.dtNascimento,
                     usuario.cpf, usuario.Telefone)

            cursor.execute(sql, values)
            self.db.connection.commit()
            usuario.id = cursor.lastrowid

            return jsonify(usuario.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_all(self):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario")
            usuarios = cursor.fetchall()
            return jsonify([Usuario.from_dict(u).to_dict() for u in usuarios]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_by_id(self, id):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario WHERE id = %s", (id,))
            usuario = cursor.fetchone()

            if usuario:
                return jsonify(Usuario.from_dict(usuario).to_dict()), 200
            return jsonify({'message': 'Usuário não encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def update(self, id):
        try:
            data = request.json
            usuario = Usuario.from_dict(data)

            cursor = self.db.connection.cursor()
            sql = """UPDATE usuario SET nome = %s, email = %s, dtNascimento = %s,
                     CPF = %s, Telefone = %s WHERE id = %s"""
            values = (usuario.nome, usuario.email, usuario.dtNascimento,
                     usuario.CPF, usuario.Telefone, id)

            cursor.execute(sql, values)
            self.db.connection.commit()

            if cursor.rowcount > 0:
                return jsonify({'message': 'Usuário atualizado com sucesso'}), 200
            return jsonify({'message': 'Usuário não encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, id):
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("DELETE FROM usuario WHERE id = %s", (id,))
            self.db.connection.commit()

            if cursor.rowcount > 0:
                return jsonify({'message': 'Usuário deletado com sucesso'}), 200
            return jsonify({'message': 'Usuário não encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
