
class Avaliação:
    """
    Representa a avaliação de um usuário sobre uma mídia ou episódio.

    Atributos:
        Nota, comentário e status geral.

    Métodos:
        Gerar média, registrar nota, registrar comentário
        e registrar status.
    """

    STATUS_VALIDOS = {
        "NÃO ASSISTIDO",
        "ASSISTINDO",
        "ASSISTIDO"
    }

    def __init__(
        self,
        nota=None,
        comentario="",
        status="NÃO ASSISTIDO"
    ):
        self.__nota = None
        self.__comentario = ""
        self.__status = "NÃO ASSISTIDO"

        if nota is not None:
            resultado = self.Registrar_nota(nota)
            if resultado is not True:
                raise ValueError(resultado)

        resultado = self.Registrar_comentario(comentario)
        if resultado is not True:
            raise ValueError(resultado)

        resultado = self.Registrar_status(status)
        if resultado is not True:
            raise ValueError(resultado)

    def Gerar_media(self, notas):
        """Calcula a média das notas recebidas."""
        if not notas:
            return 0

        return sum(notas) / len(notas)

    def Registrar_nota(self, nota):
        """Registra uma nota entre 0 e 10."""
        if (
            not isinstance(nota, (int, float))
            or isinstance(nota, bool)
        ):
            return "A nota deve ser um número."

        if not 0 <= nota <= 10:
            return "A nota deve estar entre 0 e 10."

        self.__nota = nota
        return True

    def Registrar_comentario(self, comentario):
        """Registra o comentário da avaliação."""
        if not isinstance(comentario, str):
            return "O comentário deve ser um texto."

        self.__comentario = comentario.strip()
        return True

    def Registrar_status(self, status):
        """Registra o status geral da avaliação."""
        if not isinstance(status, str):
            return "O status deve ser um texto."

        status = status.strip().upper()

        if status not in self.STATUS_VALIDOS:
            return (
                "Status inválido. Use: NÃO ASSISTIDO, "
                "ASSISTINDO ou ASSISTIDO."
            )

        self.__status = status
        return True

    def obter_nota(self):
        return self.__nota

    def obter_comentario(self):
        return self.__comentario

    def obter_status(self):
        return self.__status
