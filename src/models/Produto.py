from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Produto:
    categoria: str
    nome: str
    preco: float
    descricao: str
    urls_imagem: List[str] = field(default_factory=list)
    id: Optional[str] = None

    def to_dict(self):
        """
        Converte os campos em português para inglês para o Cosmos DB,
        mantendo a consistência com a estrutura do banco
        """
        data = {
            'id': self.id,
            'productCategory': self.categoria,
            'productName': self.nome,
            'price': self.preco,
            'imageUrl': self.urls_imagem,
            'productDescription': self.descricao
        }
        return {k: v for k, v in data.items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict):
        """
        Converte os campos em inglês do Cosmos DB para português
        """
        return cls(
            id=data.get('id'),
            categoria=data.get('productCategory', data.get('categoria')),  # tenta ambos os campos
            nome=data.get('productName', data.get('nome')),  # tenta ambos os campos
            preco=float(data.get('price', data.get('preco', 0))),  # tenta ambos os campos
            urls_imagem=data.get('imageUrl', data.get('urls_imagem', [])),  # tenta ambos os campos
            descricao=data.get('productDescription', data.get('descricao', ''))  # tenta ambos os campos
        ) 