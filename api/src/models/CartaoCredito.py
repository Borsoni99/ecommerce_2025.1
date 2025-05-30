from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

@dataclass
class CartaoCredito:
    numero: str
    dt_expiracao: datetime
    cvv: str
    saldo: float
    id_usuario_cartao: int
    id: Optional[int] = None

    def to_dict(self):
        data = asdict(self)
        # Converte o datetime para string ISO, se existir
        data['dt_expiracao'] = self.dt_expiracao.isoformat() if self.dt_expiracao else None
        return data

    @classmethod
    def from_dict(cls, data: dict):
        dt = data.get('dt_expiracao')
        if dt and isinstance(dt, str):
            try:
                # Tenta primeiro o formato ISO
                dt = datetime.fromisoformat(dt)
            except ValueError:
                try:
                    # Se falhar, tenta o formato MM/YYYY
                    mes, ano = map(int, dt.split('/'))
                    dt = datetime(ano, mes, 1)
                except ValueError:
                    raise ValueError("Data deve estar no formato ISO (YYYY-MM-DDThh:mm:ss) ou MM/YYYY")

        return cls(
            id=data.get('id'),
            numero=data.get('numero'),
            dt_expiracao=dt,
            cvv=data.get('cvv'),
            saldo=float(data.get('saldo', 0)),
            id_usuario_cartao=data.get('id_usuario_cartao')
        )
