class TipoEndereco:
    def __init__(self, tipo: str, id: int = None):
        self.id = id
        self.tipo = tipo

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo
        }

    @staticmethod
    def from_dict(data: dict):
        return TipoEndereco(
            id=data.get('id'),
            tipo=data.get('tipo')
        )
