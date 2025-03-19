from flask import Flask
from controllers.UsuarioController import UsuarioController
from controllers.CartaoCreditoController import CartaoCreditoController
from controllers.EnderecoController import EnderecoController
from controllers.TipoEnderecoController import TipoEnderecoController

app = Flask(__name__)

# Controllers
usuario_controller = UsuarioController()
cartao_controller = CartaoCreditoController()
endereco_controller = EnderecoController()
tipo_endereco_controller = TipoEnderecoController()

# Rotas para Usuário
app.route('/usuarios', methods=['POST'], endpoint='criar_usuario')(usuario_controller.create)
app.route('/usuarios', methods=['GET'], endpoint='listar_usuarios')(usuario_controller.get_all)
app.route('/usuarios/<int:id>', methods=['GET'], endpoint='buscar_usuario')(usuario_controller.get_by_id)
app.route('/usuarios/<int:id>', methods=['PUT'], endpoint='atualizar_usuario')(usuario_controller.update)
app.route('/usuarios/<int:id>', methods=['DELETE'], endpoint='deletar_usuario')(usuario_controller.delete)

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

if __name__ == '__main__':
    app.run(debug=True)
