"""Persistência dos usuários em data/dados.json.

Cada registro guarda login e senha; as listas e o histórico ficam nos
repositórios próprios e são reunidos em carregar_usuario/salvar_usuario.
"""

from repositories.base import RepositorioJson
from repositories.cadastrar_historico import CadastrarHistorico
from repositories.cadastrar_lista import CadastrarLista
from src.user import Usuario


class CadastrarUsuario(RepositorioJson):
    def __init__(self, pasta=None):
        super().__init__("dados.json", pasta)
        self._listas = CadastrarLista(pasta)
        self._historico = CadastrarHistorico(pasta)

    def obter_id(self, login):
        """ID do usuário a partir do login (ou None)."""
        for id_usuario, dados in self.carregar().items():
            if dados["usuario"] == login:
                return id_usuario
        return None

    def autenticar(self, usuario):
        """Devolve 'sucesso', 'senha_incorreta' ou 'usuario_inexistente'."""
        id_usuario = self.obter_id(usuario.login)
        if id_usuario is None:
            return "usuario_inexistente"
        if self.carregar()[id_usuario]["senha"] != usuario.senha:
            return "senha_incorreta"
        return "sucesso"

    def cadastrar(self, usuario):
        """Cadastra um usuário novo; False se o login já existe."""
        if self.obter_id(usuario.login) is not None:
            return False
        dados = self.carregar()
        usuario.id = str(max((int(i) for i in dados), default=0) + 1).zfill(4)
        dados[usuario.id] = {"usuario": usuario.login, "senha": usuario.senha}
        self.salvar(dados)
        return True

    def carregar_usuario(self, id_usuario):
        """Usuário completo, com listas e histórico."""
        try:
            registro = self.carregar()[str(id_usuario)]
        except KeyError:
            raise ValueError(f"Usuário {id_usuario} não encontrado.") from None
        usuario = Usuario(registro["usuario"], registro["senha"], str(id_usuario))
        self._listas.carregar_usuario(usuario)
        self._historico.carregar_usuario(usuario)
        return usuario

    def salvar_usuario(self, usuario):
        """Grava listas e histórico do usuário."""
        self._listas.salvar_usuario(usuario)
        self._historico.salvar_usuario(usuario)
