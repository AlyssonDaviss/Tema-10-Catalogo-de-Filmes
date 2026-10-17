
import json
import os


class CadastrarHistorico:
    """Gerencia a persistência do histórico de visualização."""

    def __init__(self, arquivo=None):
        if arquivo is None:
            raiz_projeto = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
            arquivo = os.path.join(
                raiz_projeto, "data", "historico.json"
            )

        self.arquivo = arquivo

        os.makedirs(
            os.path.dirname(self.arquivo) or ".",
            exist_ok=True
        )

        if not os.path.exists(self.arquivo):
            self.salvar_dados({})

    def carregar_dados(self):
        try:
            with open(self.arquivo, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            return dados if isinstance(dados, dict) else {}

        except FileNotFoundError:
            return {}
        except (json.JSONDecodeError, OSError):
            return {}

    def salvar_dados(self, dados):
        try:
            with open(self.arquivo, "w", encoding="utf-8") as arquivo:
                json.dump(
                    dados,
                    arquivo,
                    ensure_ascii=False,
                    indent=4
                )
            return True

        except OSError as erro:
            return f"Erro ao salvar histórico: {erro}"

    def registrar_historico(self, id_usuario, registro):
        if id_usuario is None:
            return "É necessário identificar o usuário."

        dados = self.carregar_dados()
        usuario = str(id_usuario)

        dados.setdefault(usuario, [])
        dados[usuario].append(registro)

        return self.salvar_dados(dados)

    def listar_historico(self, id_usuario):
        dados = self.carregar_dados()
        return dados.get(str(id_usuario), [])
