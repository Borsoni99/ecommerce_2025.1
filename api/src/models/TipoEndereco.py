from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class TipoEndereco:
    tipo: str
    id: Optional[str] = None

    def to_dict(self):
        data = asdict(self)
        # Remove None values as Cosmos DB doesn't handle them well
        return {k: v for k, v in data.items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            tipo=data.get('tipo')
        )
