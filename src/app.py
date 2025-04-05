from flask import Flask
from controllers.UsuarioController import UsuarioController
from controllers.CartaoCreditoController import CartaoCreditoController
from controllers.EnderecoController import EnderecoController
from controllers.TipoEnderecoController import TipoEnderecoController
from controllers.ProdutoController import ProdutoController
from database.init_db import init_database

app = Flask(__name__)

# Initialize database
init_database()

# Controllers
usuario_controller = UsuarioController()
cartao_controller = CartaoCreditoController()
endereco_controller = EnderecoController()
tipo_endereco_controller = TipoEnderecoController()
produto_controller = ProdutoController()

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
app.route('/cartoes', methods=['POST'], endpoint='criar_cartao')(cartao_controller.create)
app.route('/cartoes', methods=['GET'], endpoint='listar_cartoes')(cartao_controller.get_all)
app.route('/cartoes/<int:id>', methods=['GET'], endpoint='buscar_cartao')(cartao_controller.get_by_id)
app.route('/cartoes/<int:id>', methods=['PUT'], endpoint='atualizar_cartao')(cartao_controller.update)
app.route('/cartoes/<int:id>', methods=['DELETE'], endpoint='deletar_cartao')(cartao_controller.delete)

# Rotas para Endereço
app.route('/enderecos', methods=['POST'], endpoint='criar_endereco')(endereco_controller.create)
app.route('/enderecos', methods=['GET'], endpoint='listar_enderecos')(endereco_controller.get_all)
app.route('/enderecos/<int:id>', methods=['GET'], endpoint='buscar_endereco')(endereco_controller.get_by_id)
app.route('/enderecos/<int:id>', methods=['PUT'], endpoint='atualizar_endereco')(endereco_controller.update)
app.route('/enderecos/<int:id>', methods=['DELETE'], endpoint='deletar_endereco')(endereco_controller.delete)

# Rotas para Tipo de Endereço
app.route('/tipos-endereco', methods=['POST'], endpoint='criar_tipo_endereco')(tipo_endereco_controller.create)
app.route('/tipos-endereco', methods=['GET'], endpoint='listar_tipos_endereco')(tipo_endereco_controller.get_all)
app.route('/tipos-endereco/<int:id>', methods=['GET'], endpoint='buscar_tipo_endereco')(tipo_endereco_controller.get_by_id)
app.route('/tipos-endereco/<int:id>', methods=['PUT'], endpoint='atualizar_tipo_endereco')(tipo_endereco_controller.update)
app.route('/tipos-endereco/<int:id>', methods=['DELETE'], endpoint='deletar_tipo_endereco')(tipo_endereco_controller.delete)

# Rotas para Produtos (Cosmos DB)
app.route('/produtos', methods=['POST'], endpoint='criar_produto')(produto_controller.create)
app.route('/produtos', methods=['GET'], endpoint='listar_produtos')(produto_controller.get_all)
app.route('/produtos/<string:id>', methods=['GET'], endpoint='buscar_produto')(produto_controller.get_by_id)
app.route('/produtos/<string:id>', methods=['PUT'], endpoint='atualizar_produto')(produto_controller.update)
app.route('/produtos/<string:id>', methods=['DELETE'], endpoint='deletar_produto')(produto_controller.delete)
app.route('/produtos/categoria/<string:categoria>', methods=['GET'], endpoint='buscar_produtos_por_categoria')(produto_controller.get_by_category)

if __name__ == '__main__':
    app.run(debug=True)
