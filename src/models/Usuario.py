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
        return cls(**data)

