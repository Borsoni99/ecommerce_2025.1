from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

@dataclass
class Usuario:
    nome: str
    email: str
    dtNascimento: datetime
    CPF: str
    Telefone: str
    id: Optional[str] = None

    def to_dict(self):
        data = asdict(self)
        # Convert datetime to ISO format and remove None values
        if self.dtNascimento:
            data['dtNascimento'] = self.dtNascimento.isoformat()
        return {k: v for k, v in data.items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict):
        # Handle datetime conversion
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

