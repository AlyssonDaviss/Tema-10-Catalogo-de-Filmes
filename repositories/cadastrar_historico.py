"""Persistência do histórico de visualização em data/historico.json (por usuário)."""

from repositories.base import RepositorioJson
from src.historico import RegistroHistorico


class CadastrarHistorico(RepositorioJson):
    def __init__(self, pasta=None):
        super().__init__("historico.json", pasta)

    def carregar_usuario(self, usuario):
        for dados in self.carregar().get(usuario.id, []):
            usuario.adicionar_registro(RegistroHistorico.de_dict(dados))

    def salvar_usuario(self, usuario):
        dados = self.carregar()
        dados[usuario.id] = [r.para_dict() for r in usuario.historico]
        self.salvar(dados)
