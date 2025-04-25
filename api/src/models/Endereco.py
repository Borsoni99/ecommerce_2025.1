from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Endereco:
    logradouro: str
    complemento: str
    bairro: str
    cidade: str
    estado: str
    id_tp_endereco: int
    id_usuario: int
    id: Optional[int] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            logradouro=data.get('logradouro'),
            complemento=data.get('complemento'),
            bairro=data.get('bairro'),
            cidade=data.get('cidade'),
            estado=data.get('estado'),
            id_tp_endereco=data.get('id_tp_endereco'),
            id_usuario=data.get('id_usuario')
        )
