from flask import jsonify, request
from src.models.Pedido import Pedido
from src.models.Usuario import Usuario
from src.models.CartaoCredito import CartaoCredito
from src.database.mysql_connection import MySQLConnection
from datetime import datetime
import requests
import os

class PedidoController:
    def __init__(self):
        self.db = MySQLConnection()

    def buscar_nome_produto(self, id_produto):
        """Busca o nome do produto via API do CosmosDB"""
        try:
            api_base_url = os.environ.get('API_BASE_URL', 'https://ibmec-ecommerce-produtos-thpedu-hpgdamgyc3c4grgx.centralus-01.azurewebsites.net')
            url = f"{api_base_url}/produto/{id_produto}"

            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                produto = response.json()
                return produto.get('nome', f'Produto ID: {id_produto}')
            else:
                return f'Produto ID: {id_produto}'
        except:
            return f'Produto ID: {id_produto}'

    def get_all(self):
        """Buscar todos os pedidos"""
        try:
            # Debug: Log when GET method is called
            print(f"[DEBUG] PedidoController.get_all() called - Method: {request.method}")
            print(f"[DEBUG] Request URL: {request.url}")

            cursor = self.db.connection.cursor(dictionary=True)
            sql = """
                SELECT p.*, u.nome as nome_usuario
                FROM pedido p
                JOIN usuario u ON p.id_usuario = u.id
            """
            cursor.execute(sql)
            pedidos = cursor.fetchall()

            resultado = []
            for p in pedidos:
                nome_produto = self.buscar_nome_produto(p['id_produto'])
                resultado.append({
                    "id": p['id'],
                    "cliente": p['nome_usuario'],
                    "produto": nome_produto,
                    "id_produto": p['id_produto'],
                    "id_cartao": p['id_cartao'],
                    "id_usuario": p['id_usuario'],
                    "data": p['Data'].strftime("%d/%m/%Y"),
                    "valor": p['valor_total'],
                    "status": p['status']
                })

            return jsonify(resultado), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def get_by_id(self, id_pedido):
        """Buscar pedidos por ID"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            sql = """
                SELECT p.*, u.nome as nome_usuario
                FROM pedido p
                JOIN usuario u ON p.id_usuario = u.id
                WHERE p.id = %s
            """
            cursor.execute(sql, (id_pedido,))
            pedido = cursor.fetchone()

            if not pedido:
                return jsonify({"erro": "Pedido não encontrado"}), 404

            nome_produto = self.buscar_nome_produto(pedido['id_produto'])

            return jsonify({
                "id": pedido['id'],
                "cliente": pedido['nome_usuario'],
                "produto": nome_produto,
                "id_produto": pedido['id_produto'],
                "id_cartao": pedido['id_cartao'],
                "id_usuario": pedido['id_usuario'],
                "data": pedido['Data'].strftime("%d/%m/%Y"),
                "valor": pedido['valor_total'],
                "status": pedido['status']
            }), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def get_by_nome_cliente(self, nome_cliente):
        """Buscar pedidos de um cliente por nome"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            sql = """
                SELECT p.*, u.nome as nome_usuario
                FROM pedido p
                JOIN usuario u ON p.id_usuario = u.id
                WHERE u.nome LIKE %s
            """
            cursor.execute(sql, (f"%{nome_cliente}%",))
            pedidos = cursor.fetchall()

            resultado = []
            for p in pedidos:
                nome_produto = self.buscar_nome_produto(p['id_produto'])
                resultado.append({
                    "id": p['id'],
                    "cliente": p['nome_usuario'],
                    "produto": nome_produto,
                    "id_produto": p['id_produto'],
                    "id_cartao": p['id_cartao'],
                    "id_usuario": p['id_usuario'],
                    "data": p['Data'].strftime("%d/%m/%Y"),
                    "valor": p['valor_total'],
                    "status": p['status']
                })

            return jsonify(resultado), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def create_pedido(self):
        """Criar um pedido"""
        return jsonify({"mensagem": "Pedido criado"}), 200

    def update(self, id_pedido):
        """Atualizar um pedido"""
        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Verificar se pedido existe
            cursor.execute("SELECT * FROM pedido WHERE id = %s", (id_pedido,))
            pedido = cursor.fetchone()
            if not pedido:
                return jsonify({"erro": "Pedido não encontrado"}), 404

            data = request.json

            # Validar se usuário existe caso seja fornecido
            if "id_usuario" in data and data["id_usuario"]:
                cursor.execute("SELECT * FROM usuario WHERE id = %s", (data["id_usuario"],))
                usuario = cursor.fetchone()
                if not usuario:
                    return jsonify({"erro": "Usuário não encontrado"}), 404

            # Validar se cartão existe caso seja fornecido
            if "id_cartao" in data and data["id_cartao"]:
                cursor.execute("SELECT * FROM cartao_credito WHERE id = %s", (data["id_cartao"],))
                cartao = cursor.fetchone()
                if not cartao:
                    return jsonify({"erro": "Cartão não encontrado"}), 404

            # Atualizar pedido
            sql = """UPDATE pedido SET
                     Data = %s, id_produto = %s, id_cartao = %s,
                     id_usuario = %s, valor_total = %s, status = %s, atualizado_em = %s
                     WHERE id = %s"""

            data_pedido = datetime.strptime(data["data_pedido"], "%Y-%m-%d") if "data_pedido" in data else pedido['Data']
            values = (
                data_pedido,
                data.get("id_produto", pedido['id_produto']),
                data.get("id_cartao", pedido['id_cartao']),
                data.get("id_usuario", pedido['id_usuario']),
                data.get("valor_total", pedido['valor_total']),
                data.get("status", pedido['status']),
                datetime.now(),
                id_pedido
            )

            cursor.execute(sql, values)
            self.db.connection.commit()

            if cursor.rowcount > 0:
                return jsonify({"mensagem": "Pedido atualizado"}), 200
            return jsonify({"mensagem": "Nenhuma alteração realizada"}), 200
        except Exception as e:
            self.db.connection.rollback()
            return jsonify({'erro': str(e)}), 500

    def delete(self, id_pedido):
        """Deletar um pedido"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("DELETE FROM pedido WHERE id = %s", (id_pedido,))
            self.db.connection.commit()

            if cursor.rowcount > 0:
                return jsonify({"mensagem": "Pedido deletado"}), 200
            return jsonify({"mensagem": "Pedido não encontrado"}), 404
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
