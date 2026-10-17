# Classe: Lista
class Lista:
    """
    Representa uma lista personalizada de mídias criada por um usuário.

    Atributos:
        Nome: Nome da lista.
        Tipo: Categoria da lista.
        Conteúdo: Mídias armazenadas.
    """

    def __init__(self, nome, tipo, conteudo=None):
        self.__nome = nome
        self.__tipo = tipo
        self.__conteudo = list(conteudo) if conteudo else []

    def Criar_lista(self):
        """Cria a lista, garantindo que ela tenha um nome."""
        if not self.__nome.strip():
            return "O nome da lista não pode ser vazio."

        return True

    def Adicionar_na_lista(self, midia):
        """Adiciona uma mídia se ela ainda não estiver na lista."""
        if midia in self.__conteudo:
            return "Esta mídia já está na lista."

        self.__conteudo.append(midia)
        return True

    def Remover_na_lista(self, midia):
        """Remove uma mídia da lista."""
        if midia not in self.__conteudo:
            return "Esta mídia não está na lista."

        self.__conteudo.remove(midia)
        return True

    def Apagar_lista(self):
        """Apaga todas as mídias da lista."""
        self.__conteudo.clear()
        return True

    def obter_nome(self):
        return self.__nome

    def obter_tipo(self):
        return self.__tipo

    def obter_conteudo(self):
        return self.__conteudo.copy()