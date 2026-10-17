
import json
from pathlib import Path

from src.avaliacao import Avaliação


class CadastrarAvaliacao:
    """Gerencia a persistência das avaliações dos usuários."""

    def __init__(self, caminho="data/avaliacoes.json"):
        self.__caminho = Path(caminho)
        self.__caminho.parent.mkdir(parents=True, exist_ok=True)

        if not self.__caminho.exists():
            self.salvar_dados({})

    def carregar_dados(self):
        """Carrega as avaliações armazenadas no JSON."""
        with open(self.__caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def salvar_dados(self, dados):
        """Salva as avaliações no JSON."""
        self.__caminho.parent.mkdir(parents=True, exist_ok=True)

        with open(self.__caminho, "w", encoding="utf-8") as arquivo:
            json.dump(
                dados,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

    def registrar_avaliacao(
        self,
        id_usuario,
        id_midia,
        nota=None,
        status="NÃO ASSISTIDO",
        comentario=""
    ):
        """Registra ou atualiza a avaliação de um usuário sobre uma mídia."""
        if nota is not None:
            if (
                not isinstance(nota, (int, float))
                or isinstance(nota, bool)
            ):
                return "A nota deve ser um número."

            if not 0 <= nota <= 10:
                return "A nota deve estar entre 0 e 10."

        avaliacao = Avaliação(
            nota=nota,
            comentario=comentario,
            status=status
        )

        dados = self.carregar_dados()
        id_usuario = str(id_usuario)
        id_midia = str(id_midia)

        if id_usuario not in dados:
            dados[id_usuario] = {}

        dados[id_usuario][id_midia] = {
            "nota": avaliacao.obter_nota(),
            "status": avaliacao.obter_status(),
            "comentario": avaliacao.obter_comentario()
        }

        self.salvar_dados(dados)
        return True

    def obter_avaliacao(self, id_usuario, id_midia):
        """Retorna a avaliação de um usuário para uma mídia."""
        dados = self.carregar_dados()

        return (
            dados.get(str(id_usuario), {})
            .get(str(id_midia))
        )

    def gerar_media(self, id_midia):
        """Calcula a média das notas registradas para uma mídia."""
        dados = self.carregar_dados()
        notas = []

        for avaliacoes_usuario in dados.values():
            avaliacao = avaliacoes_usuario.get(str(id_midia))

            if avaliacao is not None and avaliacao.get("nota") is not None:
                notas.append(avaliacao["nota"])

        if not notas:
            return 0

        return sum(notas) / len(notas)
