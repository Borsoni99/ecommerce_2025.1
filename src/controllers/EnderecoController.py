from flask import jsonify, request
from models.Endereco import Endereco
from database.cosmos_connection import CosmosConnection
import uuid

class EnderecoController:
    def __init__(self):
        self.db = CosmosConnection()
        self.container = self.db.get_container('enderecos')

    def create(self):
        try:
            data = request.json
            endereco = Endereco.from_dict(data)
            
            # Generate a unique ID for the document
            document = endereco.to_dict()
            document['id'] = str(uuid.uuid4())
            
            # Create the document in Cosmos DB
            created_item = self.container.create_item(body=document)
            
            return jsonify(created_item), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_all(self):
        try:
            # Query all items
            query = "SELECT * FROM c"
            items = list(self.container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            return jsonify(items), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_by_id(self, id):
        try:
            # Get item by id
            item = self.container.read_item(item=str(id), partition_key=str(id))
            return jsonify(item), 200
        except Exception as e:
            return jsonify({'message': 'Endereço não encontrado'}), 404

    def update(self, id):
        try:
            data = request.json
            endereco = Endereco.from_dict(data)
            
            # First, get the existing item
            try:
                existing_item = self.container.read_item(item=str(id), partition_key=str(id))
            except:
                return jsonify({'message': 'Endereço não encontrado'}), 404
            
            # Update the item with new values
            update_data = endereco.to_dict()
            for key, value in update_data.items():
                if key != 'id':  # Don't update the id
                    existing_item[key] = value
            
            # Replace the item in Cosmos DB
            updated_item = self.container.replace_item(item=str(id), body=existing_item)
            
            return jsonify({'message': 'Endereço atualizado com sucesso'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete(self, id):
        try:
            # Delete the item
            self.container.delete_item(item=str(id), partition_key=str(id))
            return jsonify({'message': 'Endereço deletado com sucesso'}), 200
        except Exception as e:
            return jsonify({'message': 'Endereço não encontrado'}), 404
