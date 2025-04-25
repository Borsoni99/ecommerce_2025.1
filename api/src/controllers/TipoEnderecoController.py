from flask import jsonify, request
from src.models.TipoEndereco import TipoEndereco
from src.database.mysql_connection import MySQLConnection

class TipoEnderecoController:
    def __init__(self):
        self.db = MySQLConnection()

    def create(self):
        try:
            data = request.json
            tipo_endereco = TipoEndereco.from_dict(data)
            
            cursor = self.db.connection.cursor()
            sql = "INSERT INTO tipo_endereco (tipo) VALUES (%s)"
            values = (tipo_endereco.tipo,)
            
            cursor.execute(sql, values)
            self.db.connection.commit()
            tipo_endereco.id = cursor.lastrowid
            
            return jsonify(tipo_endereco.to_dict()), 201
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def get_all(self):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tipo_endereco")
            tipos = cursor.fetchall()
            return jsonify([TipoEndereco.from_dict(t).to_dict() for t in tipos]), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def get_by_id(self, id):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tipo_endereco WHERE id = %s", (id,))
            tipo = cursor.fetchone()
            
            if tipo:
                return jsonify(TipoEndereco.from_dict(tipo).to_dict()), 200
            return jsonify({'mensagem': 'Tipo de endereço não encontrado'}), 404
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def update(self, id):
        try:
            data = request.json
            tipo_endereco = TipoEndereco.from_dict(data)
            
            cursor = self.db.connection.cursor()
            sql = "UPDATE tipo_endereco SET tipo = %s WHERE id = %s"
            values = (tipo_endereco.tipo, id)
            
            cursor.execute(sql, values)
            self.db.connection.commit()
            
            if cursor.rowcount > 0:
                return jsonify({'mensagem': 'Tipo de endereço atualizado com sucesso'}), 200
            return jsonify({'mensagem': 'Tipo de endereço não encontrado'}), 404
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def delete(self, id):
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("DELETE FROM tipo_endereco WHERE id = %s", (id,))
            self.db.connection.commit()
            
            if cursor.rowcount > 0:
                return jsonify({'mensagem': 'Tipo de endereço deletado com sucesso'}), 200
            return jsonify({'mensagem': 'Tipo de endereço não encontrado'}), 404
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
