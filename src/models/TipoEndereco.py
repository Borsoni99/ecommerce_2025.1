from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class TipoEndereco:
    tipo: str
    id: Optional[int] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            tipo=data.get('tipo')
        )
