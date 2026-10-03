# Classe: Mídia
class Mídia:
    """
    Classe: Mídia
    Atributos: Título, Tipo, Gênero, Ano, Classificação Indicativa,
    Elenco e Status
    Métodos: Cadastrar mídia, Impedir duplicidade e Registrar status
    """

    def __init__(
        self,
        titulo,
        tipo,
        genero,
        ano,
        classificacao_indicativa,
        elenco,
        status
    ):
        self.__titulo = titulo
        self.__tipo = tipo
        self.__genero = genero
        self.__ano = ano
        self.__classificacao_indicativa = classificacao_indicativa
        self.__elenco = elenco
        self.__status = status

    def Cadastrar_Midia(self):
        """Método: Cadastrar mídia"""
        pass

    def Impedir_Duplicidade(self):
        """Método: Impedir duplicidade"""
        pass

    def Registrar_status(self):
        """Método: Registrar status"""
        pass


# Classe: Filme
class Filme(Mídia):
    """
    Classe: Filme
    Herda de: Mídia
    Atributos: Duração
    Métodos: Registrar duração
    """

    def __init__(self, duracao):
        self.__duracao = duracao

    def Registrar_duração(self):
        """Método: Registrar duração"""
        pass


# Classe: Série
class Série(Mídia):
    """
    Classe: Série
    Herda de: Mídia
    Atributos: nº Temporadas, nº Episódios e Nota opcional
    Métodos: Registrar temporadas e Atualizar status
    """

    def __init__(self, numero_temporadas, numero_episodios, nota=None):
        self.__numero_temporadas = numero_temporadas
        self.__numero_episodios = numero_episodios
        self.__nota = nota

    def Registrar_temporadas(self):
        """Método: Registrar temporadas"""
        pass

    def Atualizar_status(self):
        """Método: Atualizar status"""
        pass


# Classe: Temporada
class Temporada:
    """
    Classe: Temporada
    Se relaciona com: Série e Episódio
    Atributos: Título, nº Episódios, Data de lançamento e Nota opcional
    Métodos: Registrar episódios
    """

    def __init__(self, titulo, numero_episodios, data_lancamento, nota=None):
        self.__titulo = titulo
        self.__numero_episodios = numero_episodios
        self.__data_lancamento = data_lancamento
        self.__nota = nota

    def Registrar_episodios(self):
        """Método: Registrar episódios"""
        pass


# Classe: Episódio
class Episódio:
    """
    Classe: Episódio
    Se relaciona com: Temporada e Avaliação
    Atributos: nº Episódio, Título, Duração, Data de lançamento,
    Status de visualização e Nota opcional
    Métodos: Registrar status
    """

    def __init__(
        self,
        numero_episodio,
        titulo,
        duracao,
        data_lancamento,
        status_visualizacao,
        nota=None
    ):
        self.__numero_episodio = numero_episodio
        self.__titulo = titulo
        self.__duracao = duracao
        self.__data_lancamento = data_lancamento
        self.__status_visualizacao = status_visualizacao
        self.__nota = nota

    def Registrar_status(self):
        """Método: Registrar status"""
        pass
