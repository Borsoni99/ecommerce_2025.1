from flask import jsonify, request
from models.Endereco import Endereco
from database.mysql_connection import MySQLConnection

class EnderecoController:
    def __init__(self):
        self.db = MySQLConnection()

    def create(self):
        try:
            data = request.json
            endereco = Endereco.from_dict(data)

            cursor = self.db.connection.cursor()
            sql = """INSERT INTO endereco (logradouro, complemento, bairro, cidade, estado,
                     id_tp_endereco, id_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (endereco.logradouro, endereco.complemento, endereco.bairro,
                     endereco.cidade, endereco.estado, endereco.id_tp_endereco,
                     endereco.id_usuario)

            cursor.execute(sql, values)
            self.db.connection.commit()
            endereco.id = cursor.lastrowid

            return jsonify(endereco.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_all(self):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM endereco")
            enderecos = cursor.fetchall()
            return jsonify([Endereco.from_dict(e).to_dict() for e in enderecos]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_by_id(self, id):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM endereco WHERE id = %s", (id,))
            endereco = cursor.fetchone()

            if endereco:
                return jsonify(Endereco.from_dict(endereco).to_dict()), 200
            return jsonify({'message': 'Endereço não encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def update(self, id):
        try:
            data = request.json
            endereco = Endereco.from_dict(data)

            cursor = self.db.connection.cursor()
            sql = """UPDATE endereco SET logradouro = %s, complemento = %s, bairro = %s,
                     cidade = %s, estado = %s, id_tp_endereco = %s, id_usuario = %s
                     WHERE id = %s"""
            values = (endereco.logradouro, endereco.complemento, endereco.bairro,
                     endereco.cidade, endereco.estado, endereco.id_tp_endereco,
                     endereco.id_usuario, id)

            cursor.execute(sql, values)
            self.db.connection.commit()

            if cursor.rowcount > 0:
                return jsonify({'message': 'Endereço atualizado com sucesso'}), 200
            return jsonify({'message': 'Endereço não encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, id):
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("DELETE FROM endereco WHERE id = %s", (id,))
            self.db.connection.commit()

            if cursor.rowcount > 0:
                return jsonify({'message': 'Endereço deletado com sucesso'}), 200
            return jsonify({'message': 'Endereço não encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
