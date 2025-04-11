from flask import Flask
from src.controllers.UsuarioController import UsuarioController
from src.controllers.CartaoCreditoController import CartaoCreditoController
from src.controllers.EnderecoController import EnderecoController
from src.controllers.TipoEnderecoController import TipoEnderecoController
from src.controllers.ProdutoController import ProdutoController
from src.database.init_db import init_database
import os

app = Flask(__name__)

# Configure app based on environment
if os.getenv('WEBSITE_SITE_NAME'):  # Running in Azure
    app.config.update(
        DEBUG=False,
        PROPAGATE_EXCEPTIONS=True
    )
else:  # Running locally
    app.config.update(
        DEBUG=True
    )

# Initialize database
try:
    init_database()
except Exception as e:
    app.logger.error(f"Error initializing database: {str(e)}")

# Controllers
try:
    usuario_controller = UsuarioController()
    cartao_controller = CartaoCreditoController()
    endereco_controller = EnderecoController()
    tipo_endereco_controller = TipoEnderecoController()
    produto_controller = ProdutoController()
except Exception as e:
    app.logger.error(f"Error initializing controllers: {str(e)}")

# Add CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Add health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200

# Handle OPTIONS requests
@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    return {'status': 'ok'}, 200

# Rotas para Usuário
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    return usuario_controller.create()

@app.route('/usuarios/completo', methods=['POST'])
def create_usuario_completo():
    return usuario_controller.create_complete()

@app.route('/usuarios', methods=['GET'])
def get_all_usuarios():
    return usuario_controller.get_all()

@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario_by_id(id):
    return usuario_controller.get_by_id(id)

@app.route('/usuarios/completo/<int:id>', methods=['GET'])
def get_usuario_completo_by_id(id):
    return usuario_controller.get_complete_by_id(id)

@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    return usuario_controller.update(id)

@app.route('/usuarios/completo/<int:id>', methods=['PUT'])
def update_usuario_completo(id):
    return usuario_controller.update_complete(id)

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    return usuario_controller.delete(id)

# Rotas para Cartão de Crédito
@app.route('/cartoes', methods=['POST'])
def create_cartao():
    return cartao_controller.create()

@app.route('/cartoes/authorize/usuario/<int:id_usuario>', methods=['POST'])
def authorize_transaction(id_usuario):
    return cartao_controller.authorize_transaction(id_usuario)

@app.route('/cartoes', methods=['GET'])
def get_all_cartoes():
    return cartao_controller.get_all()

@app.route('/cartoes/<int:id>', methods=['GET'])
def get_cartao_by_id(id):
    return cartao_controller.get_by_id(id)

@app.route('/cartoes/<int:id>', methods=['PUT'])
def update_cartao(id):
    return cartao_controller.update(id)

@app.route('/cartoes/<int:id>', methods=['DELETE'])
def delete_cartao(id):
    return cartao_controller.delete(id)

# Rotas para Endereço
@app.route('/enderecos', methods=['POST'])
def create_endereco():
    return endereco_controller.create()

@app.route('/enderecos', methods=['GET'])
def get_all_enderecos():
    return endereco_controller.get_all()

@app.route('/enderecos/<int:id>', methods=['GET'])
def get_endereco_by_id(id):
    return endereco_controller.get_by_id(id)

@app.route('/enderecos/<int:id>', methods=['PUT'])
def update_endereco(id):
    return endereco_controller.update(id)

@app.route('/enderecos/<int:id>', methods=['DELETE'])
def delete_endereco(id):
    return endereco_controller.delete(id)

# Rotas para Tipo de Endereço
@app.route('/tipos-endereco', methods=['POST'])
def create_tipo_endereco():
    return tipo_endereco_controller.create()

@app.route('/tipos-endereco', methods=['GET'])
def get_all_tipos_endereco():
    return tipo_endereco_controller.get_all()

@app.route('/tipos-endereco/<int:id>', methods=['GET'])
def get_tipo_endereco_by_id(id):
    return tipo_endereco_controller.get_by_id(id)

@app.route('/tipos-endereco/<int:id>', methods=['PUT'])
def update_tipo_endereco(id):
    return tipo_endereco_controller.update(id)

@app.route('/tipos-endereco/<int:id>', methods=['DELETE'])
def delete_tipo_endereco(id):
    return tipo_endereco_controller.delete(id)

# Rotas para Produtos (Cosmos DB)
@app.route('/produtos', methods=['POST'])
def create_produto():
    return produto_controller.create()

@app.route('/produtos', methods=['GET'])
def get_all_produtos():
    return produto_controller.get_all()

@app.route('/produtos/<string:id>', methods=['GET'])
def get_produto_by_id(id):
    return produto_controller.get_by_id(id)

@app.route('/produtos/<string:id>', methods=['PUT'])
def update_produto(id):
    return produto_controller.update(id)

@app.route('/produtos/<string:id>', methods=['DELETE'])
def delete_produto(id):
    return produto_controller.delete(id)

@app.route('/produtos/categoria/<string:categoria>', methods=['GET'])
def get_produtos_by_categoria(categoria):
    return produto_controller.get_by_category(categoria)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
