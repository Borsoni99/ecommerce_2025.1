from flask import jsonify, request
from src.models.CartaoCredito import CartaoCredito
from src.database.mysql_connection import MySQLConnection
from app.request.transacao_request import TransacaoRequest
from app.response.transacao_response import TransacaoResponse
from datetime import datetime
import uuid

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

            # Convert database rows to CartaoCredito objects
            cartoes_formatados = []
            for cartao in cartoes:
                # Rename dtExpiracao to dt_expiracao to match the model
                cartao['dt_expiracao'] = cartao.pop('dtExpiracao')
                cartoes_formatados.append(CartaoCredito.from_dict(cartao).to_dict())

            return jsonify(cartoes_formatados), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def get_by_id(self, id):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cartao_credito WHERE id = %s", (id,))
            cartao = cursor.fetchone()

            if cartao:
                # Rename dtExpiracao to dt_expiracao to match the model
                cartao['dt_expiracao'] = cartao.pop('dtExpiracao')
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

    def authorize_transaction(self, id_usuario):
        cursor = None
        try:
            data = request.json
            transacao = TransacaoRequest(**data)

            # Verificar se o usuário existe
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario WHERE id = %s", (id_usuario,))
            usuario = cursor.fetchone()

            if not usuario:
                return jsonify(TransacaoResponse(
                    status="NOT_AUTHORIZED",
                    codigo_autorizacao=None,
                    dt_transacao=datetime.utcnow(),
                    message="Usuário não encontrado"
                ).dict()), 404

            # Buscar o cartão do usuário
            cursor.execute("""
                SELECT * FROM cartao_credito
                WHERE id_usuario_cartao = %s AND numero = %s AND cvv = %s
            """, (id_usuario, transacao.numero, transacao.cvv))
            cartao = cursor.fetchone()

            if not cartao:
                return jsonify(TransacaoResponse(
                    status="NOT_AUTHORIZED",
                    codigo_autorizacao=None,
                    dt_transacao=datetime.utcnow(),
                    message="Cartão não encontrado ou dados inválidos"
                ).dict()), 404

            # Verificar se o cartão está expirado
            dt_expiracao = cartao['dtExpiracao']
            if dt_expiracao < datetime.utcnow():
                return jsonify(TransacaoResponse(
                    status="NOT_AUTHORIZED",
                    codigo_autorizacao=None,
                    dt_transacao=datetime.utcnow(),
                    message="Cartão expirado"
                ).dict()), 400

            # Verificar se a data de expiração informada corresponde à do cartão
            mes, ano = map(int, transacao.dt_expiracao.split("/"))
            validade_informada = datetime(ano, mes, 1)
            if validade_informada.year != dt_expiracao.year or validade_informada.month != dt_expiracao.month:
                return jsonify(TransacaoResponse(
                    status="NOT_AUTHORIZED",
                    codigo_autorizacao=None,
                    dt_transacao=datetime.utcnow(),
                    message="Data de expiração inválida"
                ).dict()), 400

            # Verificar saldo disponível
            if float(cartao['saldo']) < transacao.valor:
                return jsonify(TransacaoResponse(
                    status="NOT_AUTHORIZED",
                    codigo_autorizacao=None,
                    dt_transacao=datetime.utcnow(),
                    message="Saldo insuficiente"
                ).dict()), 400

            # Deduzir o valor da transação do saldo
            novo_saldo = float(cartao['saldo']) - transacao.valor
            cursor.execute("""
                UPDATE cartao_credito
                SET saldo = %s
                WHERE id = %s
            """, (novo_saldo, cartao['id']))

            self.db.connection.commit()

            # Gerar resposta de sucesso
            response = jsonify(TransacaoResponse(
                status="AUTHORIZED",
                codigo_autorizacao=uuid.uuid4(),
                dt_transacao=datetime.utcnow(),
                message="Transação autorizada com sucesso"
            ).dict()), 200

            return response

        except Exception as e:
            self.db.connection.rollback()
            return jsonify({'erro': str(e)}), 500
        finally:
            if cursor:
                cursor.close()
