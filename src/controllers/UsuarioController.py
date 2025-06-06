from flask import jsonify, request
from src.models.Usuario import Usuario
from src.models.CartaoCredito import CartaoCredito
from src.models.Endereco import Endereco
from src.database.mysql_connection import MySQLConnection
from src.controllers.CartaoCreditoController import CartaoCreditoController
from src.controllers.EnderecoController import EnderecoController

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
                     usuario.CPF, usuario.Telefone)

            cursor.execute(sql, values)
            self.db.connection.commit()
            usuario.id = cursor.lastrowid

            return jsonify(usuario.to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def create_complete(self):
        """
        Cria um usuário completo com cartão de crédito e endereço em uma única requisição.
        Exemplo de JSON esperado:
        {
            "usuario": {
                "nome": "João Silva",
                "email": "joao@email.com",
                "dtNascimento": "1990-01-01T00:00:00",
                "CPF": "123.456.789-00",
                "Telefone": "(11) 98765-4321"
            },
            "cartao": {
                "numero": "1234567890123456",
                "dt_expiracao": "2025-12-31T00:00:00",
                "cvv": "123",
                "saldo": 5000.00
            },
            "endereco": {
                "logradouro": "Rua das Flores",
                "complemento": "Apto 123",
                "bairro": "Centro",
                "cidade": "São Paulo",
                "estado": "SP",
                "id_tp_endereco": 1
            }
        }
        """
        try:
            data = request.json

            # 1. Criar usuário
            usuario_data = data.get('usuario')
            if not usuario_data:
                return jsonify({'erro': 'Dados do usuário são obrigatórios'}), 400

            usuario = Usuario.from_dict(usuario_data)
            cursor = self.db.connection.cursor()

            # Inserir usuário
            sql_usuario = """INSERT INTO usuario (nome, email, dtNascimento, CPF, Telefone)
                           VALUES (%s, %s, %s, %s, %s)"""
            values_usuario = (usuario.nome, usuario.email, usuario.dtNascimento,
                            usuario.CPF, usuario.Telefone)

            cursor.execute(sql_usuario, values_usuario)
            id_usuario = cursor.lastrowid

            # 2. Criar cartão de crédito
            cartao_data = data.get('cartao')
            if cartao_data:
                cartao_data['id_usuario_cartao'] = id_usuario
                cartao = CartaoCredito.from_dict(cartao_data)

                sql_cartao = """INSERT INTO cartao_credito
                              (numero, dtExpiracao, cvv, saldo, id_usuario_cartao)
                              VALUES (%s, %s, %s, %s, %s)"""
                values_cartao = (cartao.numero, cartao.dt_expiracao, cartao.cvv,
                               cartao.saldo, cartao.id_usuario_cartao)

                cursor.execute(sql_cartao, values_cartao)

            # 3. Criar endereço
            endereco_data = data.get('endereco')
            if endereco_data:
                endereco_data['id_usuario'] = id_usuario
                endereco = Endereco.from_dict(endereco_data)

                sql_endereco = """INSERT INTO endereco
                                (logradouro, complemento, bairro, cidade, estado,
                                 id_tp_endereco, id_usuario)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                values_endereco = (endereco.logradouro, endereco.complemento,
                                 endereco.bairro, endereco.cidade, endereco.estado,
                                 endereco.id_tp_endereco, endereco.id_usuario)

                cursor.execute(sql_endereco, values_endereco)

            # Commit da transação
            self.db.connection.commit()

            # Buscar dados completos do usuário criado
            cursor.execute("""
                SELECT u.*, cc.*, e.*
                FROM usuario u
                LEFT JOIN cartao_credito cc ON u.id = cc.id_usuario_cartao
                LEFT JOIN endereco e ON u.id = e.id_usuario
                WHERE u.id = %s
            """, (id_usuario,))

            result = cursor.fetchone()

            return jsonify({
                'mensagem': 'Usuário criado com sucesso',
                'id': id_usuario,
                'dados': result
            }), 201

        except Exception as e:
            # Em caso de erro, fazer rollback
            self.db.connection.rollback()
            return jsonify({'erro': str(e)}), 500

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

    def get_by_cpf(self, cpf):
        try:
            cursor = self.db.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario WHERE CPF = %s", (cpf,))
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

    def get_complete_by_id(self, id):
        """
        Obtém todas as informações do usuário, incluindo cartões de crédito e endereços.
        """
        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Busca o usuário e seus relacionamentos
            sql = """
                SELECT
                    u.*,
                    cc.id as cartao_id, cc.numero, cc.dtExpiracao, cc.cvv, cc.saldo,
                    e.id as endereco_id, e.logradouro, e.complemento, e.bairro,
                    e.cidade, e.estado, e.id_tp_endereco,
                    te.id as tipo_endereco_id, te.tipo as tipo_endereco
                FROM usuario u
                LEFT JOIN cartao_credito cc ON u.id = cc.id_usuario_cartao
                LEFT JOIN endereco e ON u.id = e.id_usuario
                LEFT JOIN tipo_endereco te ON e.id_tp_endereco = te.id
                WHERE u.id = %s
            """
            cursor.execute(sql, (id,))
            result = cursor.fetchall()

            if not result:
                return jsonify({'mensagem': 'Usuário não encontrado'}), 404

            # Organiza os dados em uma estrutura hierárquica
            usuario_data = {
                'id': result[0]['id'],
                'nome': result[0]['nome'],
                'email': result[0]['email'],
                'dtNascimento': result[0]['dtNascimento'],
                'CPF': result[0]['CPF'],
                'Telefone': result[0]['Telefone'],
                'cartoes': [],
                'enderecos': []
            }

            # Processa cartões e endereços
            cartoes_processados = set()
            enderecos_processados = set()

            for row in result:
                # Adiciona cartão se existir e não foi processado
                if row['cartao_id'] and row['cartao_id'] not in cartoes_processados:
                    cartoes_processados.add(row['cartao_id'])
                    usuario_data['cartoes'].append({
                        'id': row['cartao_id'],
                        'numero': row['numero'],
                        'dtExpiracao': row['dtExpiracao'],
                        'cvv': row['cvv'],
                        'saldo': row['saldo']
                    })

                # Adiciona endereço se existir e não foi processado
                if row['endereco_id'] and row['endereco_id'] not in enderecos_processados:
                    enderecos_processados.add(row['endereco_id'])
                    usuario_data['enderecos'].append({
                        'id': row['endereco_id'],
                        'logradouro': row['logradouro'],
                        'complemento': row['complemento'],
                        'bairro': row['bairro'],
                        'cidade': row['cidade'],
                        'estado': row['estado'],
                        'tipo_endereco': {
                            'id': row['tipo_endereco_id'],
                            'tipo': row['tipo_endereco']
                        }
                    })

            return jsonify(usuario_data), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def update_complete(self, id):
        """
        Atualiza todas as informações do usuário, incluindo cartões e endereços.
        Exemplo de JSON esperado:
        {
            "usuario": {
                "nome": "João Silva",
                "email": "joao@email.com",
                "dtNascimento": "1990-01-01T00:00:00",
                "CPF": "123.456.789-00",
                "Telefone": "(11) 98765-4321"
            },
            "cartoes": [{
                "id": 1,  # opcional, se não fornecido, cria novo
                "numero": "1234567890123456",
                "dt_expiracao": "2025-12-31T00:00:00",
                "cvv": "123",
                "saldo": 5000.00
            }],
            "enderecos": [{
                "id": 1,  # opcional, se não fornecido, cria novo
                "logradouro": "Rua das Flores",
                "complemento": "Apto 123",
                "bairro": "Centro",
                "cidade": "São Paulo",
                "estado": "SP",
                "id_tp_endereco": 1
            }]
        }
        """
        try:
            data = request.json
            cursor = self.db.connection.cursor()

            # 1. Atualiza usuário
            usuario_data = data.get('usuario')
            if not usuario_data:
                return jsonify({'erro': 'Dados do usuário são obrigatórios'}), 400

            usuario = Usuario.from_dict(usuario_data)
            sql_usuario = """UPDATE usuario
                           SET nome = %s, email = %s, dtNascimento = %s,
                               CPF = %s, Telefone = %s
                           WHERE id = %s"""
            values_usuario = (usuario.nome, usuario.email, usuario.dtNascimento,
                            usuario.CPF, usuario.Telefone, id)

            cursor.execute(sql_usuario, values_usuario)
            if cursor.rowcount == 0:
                return jsonify({'erro': 'Usuário não encontrado'}), 404

            # 2. Atualiza cartões
            cartoes_data = data.get('cartoes', [])
            if cartoes_data:
                # Remove cartões antigos não presentes na atualização
                cartoes_ids = [c.get('id') for c in cartoes_data if 'id' in c]
                if cartoes_ids:
                    # Formatação especial para IN com um único ID
                    if len(cartoes_ids) == 1:
                        sql_delete_cartoes = """DELETE FROM cartao_credito
                                              WHERE id_usuario_cartao = %s
                                              AND id != %s"""
                        cursor.execute(sql_delete_cartoes, (id, cartoes_ids[0]))
                    else:
                        sql_delete_cartoes = """DELETE FROM cartao_credito
                                              WHERE id_usuario_cartao = %s
                                              AND id NOT IN %s"""
                        cursor.execute(sql_delete_cartoes, (id, tuple(cartoes_ids)))
                else:
                    cursor.execute("""DELETE FROM cartao_credito
                                    WHERE id_usuario_cartao = %s""", (id,))

                # Atualiza ou cria novos cartões
                for cartao_data in cartoes_data:
                    cartao_data['id_usuario_cartao'] = id
                    cartao = CartaoCredito.from_dict(cartao_data)

                    if 'id' in cartao_data:
                        # Atualiza cartão existente
                        sql_cartao = """UPDATE cartao_credito
                                      SET numero = %s, dtExpiracao = %s, cvv = %s,
                                          saldo = %s
                                      WHERE id = %s AND id_usuario_cartao = %s"""
                        values_cartao = (cartao.numero, cartao.dt_expiracao,
                                       cartao.cvv, cartao.saldo,
                                       cartao_data['id'], id)
                        cursor.execute(sql_cartao, values_cartao)
                    else:
                        # Cria novo cartão
                        sql_cartao = """INSERT INTO cartao_credito
                                      (numero, dtExpiracao, cvv, saldo, id_usuario_cartao)
                                      VALUES (%s, %s, %s, %s, %s)"""
                        values_cartao = (cartao.numero, cartao.dt_expiracao,
                                       cartao.cvv, cartao.saldo, id)
                        cursor.execute(sql_cartao, values_cartao)

            # 3. Atualiza endereços
            enderecos_data = data.get('enderecos', [])
            if enderecos_data:
                # Remove endereços antigos não presentes na atualização
                enderecos_ids = [e.get('id') for e in enderecos_data if 'id' in e]
                if enderecos_ids:
                    # Formatação especial para IN com um único ID
                    if len(enderecos_ids) == 1:
                        sql_delete_enderecos = """DELETE FROM endereco
                                                WHERE id_usuario = %s
                                                AND id != %s"""
                        cursor.execute(sql_delete_enderecos, (id, enderecos_ids[0]))
                    else:
                        sql_delete_enderecos = """DELETE FROM endereco
                                                WHERE id_usuario = %s
                                                AND id NOT IN %s"""
                        cursor.execute(sql_delete_enderecos, (id, tuple(enderecos_ids)))
                else:
                    cursor.execute("""DELETE FROM endereco
                                    WHERE id_usuario = %s""", (id,))

                # Atualiza ou cria novos endereços
                for endereco_data in enderecos_data:
                    endereco_data['id_usuario'] = id
                    endereco = Endereco.from_dict(endereco_data)

                    if 'id' in endereco_data:
                        # Atualiza endereço existente
                        sql_endereco = """UPDATE endereco
                                        SET logradouro = %s, complemento = %s,
                                            bairro = %s, cidade = %s, estado = %s,
                                            id_tp_endereco = %s
                                        WHERE id = %s AND id_usuario = %s"""
                        values_endereco = (endereco.logradouro, endereco.complemento,
                                         endereco.bairro, endereco.cidade,
                                         endereco.estado, endereco.id_tp_endereco,
                                         endereco_data['id'], id)
                        cursor.execute(sql_endereco, values_endereco)
                    else:
                        # Cria novo endereço
                        sql_endereco = """INSERT INTO endereco
                                        (logradouro, complemento, bairro, cidade,
                                         estado, id_tp_endereco, id_usuario)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                        values_endereco = (endereco.logradouro, endereco.complemento,
                                         endereco.bairro, endereco.cidade,
                                         endereco.estado, endereco.id_tp_endereco, id)
                        cursor.execute(sql_endereco, values_endereco)

            # Commit da transação
            self.db.connection.commit()

            # Retorna os dados atualizados
            return self.get_complete_by_id(id)

        except Exception as e:
            # Em caso de erro, faz rollback
            self.db.connection.rollback()
            return jsonify({'erro': str(e)}), 500
