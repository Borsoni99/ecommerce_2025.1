from datetime import datetime

class Usuario:
    def __init__(self, nome: str, email: str, dt_nascimento: datetime, cpf: str, telefone: str, id: int = None):
        self.id = id
        self.nome = nome
        self.email = email
        self.dt_nascimento = dt_nascimento
        self.cpf = cpf
        self.telefone = telefone

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'dt_nascimento': self.dt_nascimento.isoformat() if self.dt_nascimento else None,
            'cpf': self.cpf,
            'telefone': self.telefone
        }

    @staticmethod
    def from_dict(data: dict):
        return Usuario(
        id=data.get('id'),
        nome=data.get('nome'),
        email=data.get('email'),
        dt_nascimento=datetime.fromisoformat(data.get('dt_nascimento')) if data.get('dt_nascimento') else None,
        cpf=data.get('cpf'),
        telefone=data.get('telefone')
    )
