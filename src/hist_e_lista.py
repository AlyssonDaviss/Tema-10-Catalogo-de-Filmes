# Classe: Histórico de visualização
class Histórico_de_visualização:
    """
    Classe: Histórico de visualização
    Se relaciona com: Usuário e Mídia
    Atributos: Mídia, Data e Hora
    Métodos: Salvar histórico e Registrar data e hora
    """

    def __init__(self, midia, data, hora):
        self.__midia = midia
        self.__data = data
        self.__hora = hora

    def Salvar_historico(self):
        """Método: Salvar histórico"""
        pass

    def Registrar_data_hora(self):
        """Método: Registrar data e hora"""
        pass

# Classe: Lista
class Lista:
    """
    Classe: Lista
    Se relaciona com: Usuário e Mídia
    Atributos: Nome, Tipo e Conteúdo
    Métodos: Criar lista, Adicionar na lista, Remover na lista e Apagar lista
    """

    def __init__(self, nome, tipo, conteudo):
        self.__nome = nome
        self.__tipo = tipo
        self.__conteudo = conteudo

    def Criar_lista(self):
        """Método: Criar lista"""
        pass

    def Adicionar_na_lista(self):
        """Método: Adicionar na lista"""
        pass

    def Remover_na_lista(self):
        """Método: Remover na lista"""
        pass

    def Apagar_lista(self):
        """Método: Apagar lista"""
        pass