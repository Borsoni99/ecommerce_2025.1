from flask import Flask, request, jsonify
from src.controllers.UsuarioController import UsuarioController
from src.controllers.CartaoCreditoController import CartaoCreditoController
from src.controllers.EnderecoController import EnderecoController
from src.controllers.TipoEnderecoController import TipoEnderecoController
from src.controllers.ProdutoController import ProdutoController
from src.controllers.PedidoController import PedidoController
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
# Initialize controllers individually to avoid failure cascade
usuario_controller = None
cartao_controller = None
endereco_controller = None
tipo_endereco_controller = None
produto_controller = None
pedido_controller = None

try:
    usuario_controller = UsuarioController()
    app.logger.info("UsuarioController initialized successfully")
except Exception as e:
    app.logger.error(f"Error initializing UsuarioController: {str(e)}")

try:
    cartao_controller = CartaoCreditoController()
    app.logger.info("CartaoCreditoController initialized successfully")
except Exception as e:
    app.logger.error(f"Error initializing CartaoCreditoController: {str(e)}")

try:
    endereco_controller = EnderecoController()
    app.logger.info("EnderecoController initialized successfully")
except Exception as e:
    app.logger.error(f"Error initializing EnderecoController: {str(e)}")

try:
    tipo_endereco_controller = TipoEnderecoController()
    app.logger.info("TipoEnderecoController initialized successfully")
except Exception as e:
    app.logger.error(f"Error initializing TipoEnderecoController: {str(e)}")

try:
    produto_controller = ProdutoController()
    app.logger.info("ProdutoController initialized successfully")
except Exception as e:
    app.logger.error(f"Error initializing ProdutoController: {str(e)}")

try:
    pedido_controller = PedidoController()
    app.logger.info("PedidoController initialized successfully")
except Exception as e:
    app.logger.error(f"Error initializing PedidoController: {str(e)}")

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

# Rotas para Pedidos
# Rotas específicas primeiro para evitar conflitos
@app.route('/pedidos/nome/<string:nome_cliente>', methods=['GET'])
def get_pedidos_by_nome_cliente(nome_cliente):
    return pedido_controller.get_by_nome_cliente(nome_cliente)

@app.route('/pedidos/<int:id_pedido>', methods=['GET'])
def get_pedido_by_id(id_pedido):
    return pedido_controller.get_by_id(id_pedido)

@app.route('/pedidos/<int:id_pedido>', methods=['PUT'])
def update_pedido(id_pedido):
    return pedido_controller.update(id_pedido)

@app.route('/pedidos/<int:id_pedido>', methods=['DELETE'])
def delete_pedido(id_pedido):
    return pedido_controller.delete(id_pedido)

@app.route('/pedidos', methods=['POST', 'GET'])
def handle_pedidos():
    if request.method == 'POST':
        return pedido_controller.create()
    elif request.method == 'GET':
        return pedido_controller.get_all()

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

@app.route('/usuarios/cpf/<string:cpf>', methods=['GET'])
def get_usuario_by_cpf(cpf):
    return usuario_controller.get_by_cpf(cpf)

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

@app.route('/cartoes/numero/<string:numero>', methods=['GET'])
def get_cartao_by_numero(numero):
    return cartao_controller.get_by_numero(numero)

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

@app.route('/produtos/nome/<string:nome>', methods=['GET'])
def get_produtos_by_nome(nome):
    return produto_controller.get_by_name(nome)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
