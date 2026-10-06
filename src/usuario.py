# Classe: Usuário
class Usuário:
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

    def Fazer_login(self, login, senha):
        """Método: Fazer login"""
        if login == self.__login and senha == self.__senha:
            return True
        pass