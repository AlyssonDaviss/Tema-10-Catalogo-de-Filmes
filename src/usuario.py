# Classe: Usuário
class Usuário:
    """
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