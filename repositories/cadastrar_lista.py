"""Persistência das listas personalizadas em data/listas.json (por usuário)."""

from repositories.base import RepositorioJson
from src.listas import ListaPersonalizada


class CadastrarLista(RepositorioJson):
    """Persistência de listas por usuário."""
    def __init__(self, pasta=None):
        super().__init__("listas.json", pasta)

    def carregar_usuario(self, usuario):
        for dados in self.carregar().get(usuario.id, []):
            usuario.adicionar_lista(ListaPersonalizada.de_dict(dados))

    def salvar_usuario(self, usuario):
        dados = self.carregar()
        dados[usuario.id] = [lista.para_dict() for lista in usuario.listas]
        self.salvar(dados)
