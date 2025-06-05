from flask import jsonify, request
from src.models.Produto import Produto
from src.database.cosmos_connection import CosmosConnection
import uuid

class ProdutoController:
    def __init__(self):
        self.db = CosmosConnection()
        self.container = self.db.get_container('produtos')

    def create(self):
        try:
            data = request.json
            produto = Produto.from_dict(data)
            
            # Gera um ID único para o documento
            document = produto.to_dict()
            document['id'] = str(uuid.uuid4())
            
            # Cria o documento no Cosmos DB
            created_item = self.container.create_item(body=document)
            
            return jsonify(created_item), 201
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def get_all(self):
        try:
            # Consulta todos os itens
            query = "SELECT * FROM c"
            items = list(self.container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            return jsonify(items), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def get_by_id(self, id):
        try:
            # Busca o item por ID usando query
            query = "SELECT * FROM c WHERE c.id = @id"
            params = [{"name": "@id", "value": id}]
            items = list(self.container.query_items(
                query=query,
                parameters=params,
                enable_cross_partition_query=True
            ))
            
            if not items:
                return jsonify({'mensagem': 'Produto não encontrado'}), 404
                
            return jsonify(items[0]), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def get_by_category(self, categoria):
        try:
            # Consulta itens por categoria
            query = "SELECT * FROM c WHERE c.productCategory = @category"
            params = [{"name": "@category", "value": categoria}]
            items = list(self.container.query_items(
                query=query,
                parameters=params,
                enable_cross_partition_query=True
            ))
            return jsonify(items), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def update(self, id):
        try:
            data = request.json
            produto = Produto.from_dict(data)
            
            # Primeiro, verifica se o item existe
            query = "SELECT * FROM c WHERE c.id = @id"
            params = [{"name": "@id", "value": id}]
            items = list(self.container.query_items(
                query=query,
                parameters=params,
                enable_cross_partition_query=True
            ))
            
            if not items:
                return jsonify({'mensagem': 'Produto não encontrado'}), 404
            
            # Prepara o documento atualizado
            existing_item = items[0]
            update_data = produto.to_dict()
            for key, value in update_data.items():
                if key != 'id':  # Não atualiza o id
                    existing_item[key] = value
            
            # Atualiza o documento usando upsert
            updated_item = self.container.upsert_item(body=existing_item)
            
            return jsonify({'mensagem': 'Produto atualizado com sucesso'}), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500

    def delete(self, id):
        try:
            # Primeiro, verifica se o item existe e obtém sua categoria
            query = "SELECT * FROM c WHERE c.id = @id"
            params = [{"name": "@id", "value": id}]
            items = list(self.container.query_items(
                query=query,
                parameters=params,
                enable_cross_partition_query=True
            ))
            
            if not items:
                return jsonify({'mensagem': 'Produto não encontrado'}), 404
            
            # Deleta o item usando o ID e a categoria como partition key
            self.container.delete_item(
                item=id,
                partition_key=items[0]['productCategory']
            )
            return jsonify({'mensagem': 'Produto deletado com sucesso'}), 200
        except Exception as e:
            return jsonify({'erro': str(e)}), 500 