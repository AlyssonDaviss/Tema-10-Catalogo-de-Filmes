
class Avaliação:
    """
    Representa a avaliação de um usuário sobre uma mídia ou episódio.

    Atributos: Nota e Comentário
    Métodos: Gerar média, Registrar nota e Registrar comentário
    """

    def __init__(self, nota=None, comentario=""):
        self.__nota = nota
        self.__comentario = comentario

    def Gerar_media(self, notas):
        """Calcula a média das notas recebidas."""
        if not notas:
            return 0

        return sum(notas) / len(notas)

    def Registrar_nota(self, nota):
        """Registra uma nota entre 0 e 10."""
        if not isinstance(nota, (int, float)) or isinstance(nota, bool):
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
