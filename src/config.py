# Classe: Configurações
class Configurações:
    """
    A classe Configurações representa as configurações do sistema, permitindo que os usuários 
    ajustem parâmetros importantes para a recomendação de mídias e gerenciamento de listas personalizadas.
    
    Classe: Configurações
    Atributos: Nota mínima para a recomendação e limite de listas personalizadas por usuário
    Métodos: Mostrar configuração, Nota mínima recomendada e Limite de lista
    """

    def __init__(self, nota_min_recomendacao, limite_listas_personalizadas):
        self.nota_min_recomendacao = nota_min_recomendacao
        self.limite_listas_personalizadas = limite_listas_personalizadas

    def Mostrar_config(self):
        """Método: Mostrar configuração"""
        pass

    def Nota_min_recomendado(self):
        """Método: Nota mínima recomendada"""
        pass

    def Limite_lista(self):
        """Método: Limite de lista"""
        pass
