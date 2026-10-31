"""Persistência das configurações em settings.json (na raiz do projeto)."""

from dataclasses import asdict

from repositories.base import RAIZ, RepositorioJson
from src.domain.config import Configuracoes


class CadastrarConfiguracoes(RepositorioJson):
    """Persistência das configurações do sistema."""
    def __init__(self, pasta=None):
        super().__init__("settings.json", pasta or RAIZ)

    def carregar(self):
        """Lê as configurações; chaves ausentes usam o valor padrão."""
        try:
            return Configuracoes(**super().carregar())
        except TypeError as erro:
            raise ValueError(f"settings.json inválido: {erro}") from None

    def salvar(self, configuracoes):
        super().salvar(asdict(configuracoes))
