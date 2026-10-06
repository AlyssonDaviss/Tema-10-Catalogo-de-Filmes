# Classe: Avaliação
class Avaliação:
    """
    A classe avaliação representa a avaliação de um usuário sobre uma mídia ou episódio específico. 
    Ela se relaciona com as classes Usuário, Mídia e Episódio, permitindo que os usuários forneçam 
    feedback sobre o conteúdo que consumiram.
    
    Classe: Avaliação
    Se relaciona com: Usuário, Mídia e Episódio
    Atributos: Nota e Comentário
    Métodos: Gerar média, Registrar nota e Registrar comentário
    """

    def __init__(self, nota, comentario):
        self.__nota = nota
        self.__comentario = comentario

    def Gerar_media(self):
        """Método: Gerar média"""
        pass

    def Registrar_nota(self):
        """Método: Registrar nota"""
        pass

    def Registrar_comentario(self):
        """Método: Registrar comentário"""
        pass