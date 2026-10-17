
import json
import os


class CadastrarAvaliacao:
    def __init__(self, caminho="data/avaliacoes.json"):
        self.__caminho = caminho

    def carregar_dados(self):
        if not os.path.exists(self.__caminho):
            return {}

        with open(self.__caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def salvar_dados(self, dados):
        diretorio = os.path.dirname(self.__caminho)

        if diretorio:
            os.makedirs(diretorio, exist_ok=True)

        with open(self.__caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    def registrar_avaliacao(
        self, id_usuario, id_midia, nota, status, comentario=""
    ):
        dados = self.carregar_dados()

        id_usuario = str(id_usuario)
        id_midia = str(id_midia)

        if not isinstance(nota, (int, float)) or isinstance(nota, bool):
            return "A nota deve ser um número."

        if not 0 <= nota <= 10:
            return "A nota deve estar entre 0 e 10."

        status_permitidos = (
            "planejando",
            "completo",
            "assistindo",
            "pausado",
            "dropado"
        )

        if status not in status_permitidos:
            return "Status inválido."

        if not isinstance(comentario, str):
            return "O comentário deve ser um texto."

        if id_usuario not in dados:
            dados[id_usuario] = {}

        dados[id_usuario][id_midia] = {
            "nota": nota,
            "status": status,
            "comentario": comentario.strip()
        }

        self.salvar_dados(dados)
        return True

    def gerar_media(self, id_midia):
        dados = self.carregar_dados()
        notas = []

        for avaliacoes_usuario in dados.values():
            avaliacao = avaliacoes_usuario.get(str(id_midia))

            if avaliacao is not None:
                notas.append(avaliacao["nota"])

        if not notas:
            return 0

        return sum(notas) / len(notas)
