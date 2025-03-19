class Endereco:
    def __init__(self, logradouro: str, complemento: str, bairro: str, cidade: str,
                 estado: str, id_tp_endereco: int, id_usuario: int, id: int = None):
        self.id = id
        self.logradouro = logradouro
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.id_tp_endereco = id_tp_endereco
        self.id_usuario = id_usuario

    def to_dict(self):
        return {
            'id': self.id,
            'logradouro': self.logradouro,
            'complemento': self.complemento,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado,
            'id_tp_endereco': self.id_tp_endereco,
            'id_usuario': self.id_usuario
        }

    @staticmethod
    def from_dict(data: dict):
        return Endereco(
            id=data.get('id'),
            logradouro=data.get('logradouro'),
            complemento=data.get('complemento'),
            bairro=data.get('bairro'),
            cidade=data.get('cidade'),
            estado=data.get('estado'),
            id_tp_endereco=data.get('id_tp_endereco'),
            id_usuario=data.get('id_usuario')
        )
