from flask import jsonify, request
from src.models.CartaoCredito import CartaoCredito
from src.database.mysql_connection import MySQLConnection

class CartaoCreditoController:
    def __init__(self):
        self.db = MySQLConnection()

    def create(self):
        try:
            data = request.json
            cartao = CartaoCredito.from_dict(data)
            
            cursor = self.db.connection.cursor()
            sql = """INSERT INTO cartao_credito 
                     (numero, dtExpiracao, cvv, saldo, id_usuario_cartao)
                     VALUES (%s, %s, %s, %s, %s)"""
            values = (cartao.numero, cartao.dt_expiracao, cartao.cvv,
                     cartao.saldo, cartao.id_usuario_cartao)
            
            cursor.execute(sql, values)
            self.db.connection.commit()
            cartao.id = cursor.lastrowid
            
            return jsonify(cartao.to_dict()), 201
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def get_all(self):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cartao_credito")
            cartoes = cursor.fetchall()
            return jsonify([CartaoCredito.from_dict(c).to_dict() for c in cartoes]), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def get_by_id(self, id):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cartao_credito WHERE id = %s", (id,))
            cartao = cursor.fetchone()
            
            if cartao:
                return jsonify(CartaoCredito.from_dict(cartao).to_dict()), 200
            return jsonify({'mensagem': 'Cartão não encontrado'}), 404
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def update(self, id):
        try:
            data = request.json
            cartao = CartaoCredito.from_dict(data)
            
            cursor = self.db.connection.cursor()
            sql = """UPDATE cartao_credito 
                     SET numero = %s, dtExpiracao = %s, cvv = %s, 
                         saldo = %s, id_usuario_cartao = %s 
                     WHERE id = %s"""
            values = (cartao.numero, cartao.dt_expiracao, cartao.cvv,
                     cartao.saldo, cartao.id_usuario_cartao, id)
            
            cursor.execute(sql, values)
            self.db.connection.commit()
            
            if cursor.rowcount > 0:
                return jsonify({'mensagem': 'Cartão atualizado com sucesso'}), 200
            return jsonify({'mensagem': 'Cartão não encontrado'}), 404
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def delete(self, id):
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("DELETE FROM cartao_credito WHERE id = %s", (id,))
            self.db.connection.commit()
            
            if cursor.rowcount > 0:
                return jsonify({'mensagem': 'Cartão deletado com sucesso'}), 200
            return jsonify({'mensagem': 'Cartão não encontrado'}), 404
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
