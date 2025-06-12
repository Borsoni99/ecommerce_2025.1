from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional

@dataclass
class Pedido:
    valor_total: float
    id_usuario: int
    Data: datetime
    id_cartao: int
    id_produto: str
    id: Optional[int] = field(default=None)
    status: str
    criado_em: datetime = field(default_factory=datetime.now)
    atualizado_em: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        data = asdict(self)
        data['Data'] = self.Data.isoformat()
        return data

