
import json
from pathlib import Path


class CadastrarUsuario:
    def __init__(self):
        self.caminho = (
            Path(__file__).resolve().parent.parent
            / "data" / "dados.json"
        )

    def carregar_dados(self):
        with open(self.caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def cadastrar(self, usuario):
        dados = self.carregar_dados()

        if self.usuario_existe(dados, usuario):
            return False

        novo_id = self.gerar_id(dados)
        dados[novo_id] = self.criar_dados_usuario(usuario)

        self.salvar_dados(dados)
        return True

    def usuario_existe(self, dados, usuario):
        for dados_usuario in dados.values():
            if dados_usuario["usuario"] == usuario.login:
                return True
        return False

    def senha_correta(self, dados, usuario):
        for dados_usuario in dados.values():
            if dados_usuario["usuario"] == usuario.login:
                return dados_usuario["senha"] == usuario.senha
        return False

    def autenticar(self, usuario):
        dados = self.carregar_dados()

        if not self.usuario_existe(dados, usuario):
            return "usuario_inexistente"

        if not self.senha_correta(dados, usuario):
            return "senha_incorreta"

        return "sucesso"

    def obter_id(self, login):
        """Retorna o ID do usuário a partir do login."""
        dados = self.carregar_dados()

        for id_usuario, dados_usuario in dados.items():
            if dados_usuario["usuario"] == login:
                return id_usuario

        return None

    def gerar_id(self, dados):
        return str(len(dados) + 1).zfill(4)

    def criar_dados_usuario(self, usuario):
        return {
            "usuario": usuario.login,
            "senha": usuario.senha,
            "historico": [],
            "listas": {
                "favoritos": [],
                "assistir_mais_tarde": []
            }
        }

    def salvar_dados(self, dados):
        with open(self.caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
