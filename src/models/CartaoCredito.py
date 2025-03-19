from datetime import datetime

class CartaoCredito:
    def __init__(self, numero: str, dt_expiracao: datetime, cvv: str, saldo: float, id_usuario_cartao: int, id: int = None):
        self.id = id
        self.numero = numero
        self.dt_expiracao = dt_expiracao
        self.cvv = cvv
        self.saldo = saldo
        self.id_usuario_cartao = id_usuario_cartao

    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'dt_expiracao': self.dt_expiracao.isoformat() if self.dt_expiracao else None,
            'cvv': self.cvv,
            'saldo': float(self.saldo),
            'id_usuario_cartao': self.id_usuario_cartao
        }

    @staticmethod
    def from_dict(data: dict):
        return CartaoCredito(
            id=data.get('id'),
            numero=data.get('numero'),
            dt_expiracao=datetime.fromisoformat(data['dt_expiracao']) if data.get('dt_expiracao') else None,
            cvv=data.get('cvv'),
            saldo=float(data.get('saldo', 0)),
            id_usuario_cartao=data.get('id_usuario_cartao')
        )
