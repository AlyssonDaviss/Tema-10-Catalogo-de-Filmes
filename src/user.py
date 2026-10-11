
# Classe: Usuário
import json
from pathlib import Path

class Usuario:
    """
    A classe Usuário representa um usuário do sistema, permitindo que ele faça login e acesse suas
    listas personalizadas, avaliações e histórico de visualização.

    Classe: Usuário
    Atributos: Login e Senha
    Métodos: Fazer login
    """

    def __init__(self, login, senha):
        self.__login = login
        self.__senha = senha

    def carregar_dados(self):
        caminho = Path(__file__).resolve().parent.parent / "data" / "dados.json"

        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        return dados

    def cadastrar(self):
        dados = self.carregar_dados()

        for usuario in dados.values():
            if usuario["usuario"] == self.__login:
                return False

        novo_id = str(len(dados) + 1).zfill(4)

        dados[novo_id] = {
            "usuario": self.__login,
            "senha": self.__senha,
            "historico": [],
            "listas": {
                "favoritos": [],
                "assistir_mais_tarde": []
            }
        }

        caminho = Path(__file__).resolve().parent.parent / "data" / "dados.json"

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

        return True