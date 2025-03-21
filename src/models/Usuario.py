from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional

@dataclass
class Usuario:
    nome: str
    email: str
    dtNascimento: datetime
    CPF: str
    Telefone: str
    id: Optional[int] = field(default=None)

    def to_dict(self):
        data = asdict(self)
        # Converte o datetime para string no formato ISO se existir
        data['dtNascimento'] = self.dtNascimento.isoformat() if self.dtNascimento else None
        return data

    @classmethod
    def from_dict(cls, data: dict):
        # Se o valor de dtNascimento for uma string, converte para datetime
        dt = data.get('dtNascimento')
        if dt and isinstance(dt, str):
            data['dtNascimento'] = datetime.fromisoformat(dt)
        return cls(
            id=data.get('id'),
            nome=data.get('nome'),
            email=data.get('email'),
            dtNascimento=data.get('dtNascimento'),
            CPF=data.get('CPF'),
            Telefone=data.get('Telefone')
        )

