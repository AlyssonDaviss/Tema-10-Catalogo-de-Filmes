# Classe: Usuário

class Usuario:
    def __init__(self, login, senha):
        self.__login = login
        self.__senha = senha

    @property
    def login(self):
        return self.__login

    @property
    def senha(self):
        return self.__senha 