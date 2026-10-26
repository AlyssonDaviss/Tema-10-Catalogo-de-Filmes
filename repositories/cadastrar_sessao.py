"""Sessão do usuário que fez login (data/sessao.json), usada pelos subcomandos."""

from repositories.base import RepositorioJson


class CadastrarSessao(RepositorioJson):
    """Persistência da sessão ativa."""
    def __init__(self, pasta=None):
        super().__init__("sessao.json", pasta)

    def atual(self):
        """ID do usuário conectado, ou None."""
        return self.carregar().get("id_usuario")

    def definir(self, id_usuario):
        self.salvar({"id_usuario": id_usuario})

    def limpar(self):
        self.salvar({})
