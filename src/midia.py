# Classe: Mídia
import json
from pathlib import Path

class Midia:
    """
    A classe Mídia representa uma mídia, que pode ser um filme ou uma série, com seus atributos e métodos relacionados.
    Ela se relaciona com as classes Avaliação, Histórico de visualização e Lista, permitindo que os usuários interajam 
    com as mídias de acordo com suas preferências e avaliações.

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

    def carregar_dados(self):
        caminho = Path(__file__).resolve().parent.parent / "data" / "midia_dic.json"

        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        return dados

    def Cadastrar_Midia(self):
        dados = self.carregar_dados()

        novo_id = str(len(dados) + 1).zfill(4)

        if self.__tipo == "filme":
            dados[novo_id] = {
                "tipo": self.__tipo,
                "titulo": self.__titulo,
                "genero":  self.__genero,
                "duracao": ""
            }

        elif self.__tipo == "serie":

            dados[novo_id] = {
                "tipo": self.__tipo,
                "titulo": self.__titulo,
                "genero": self.__genero,
                "episodios": [
                    {
                        "id": "",
                        "titulo": "",
                        "duracao": 0
                    },
                    {
                        "id": "",
                        "titulo": "",
                        "duracao": 0
                    }
                ]
            }
        caminho = Path(__file__).resolve().parent.parent / "data" / "midia_dic.json"

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

        return True

    def Impedir_Duplicidade(self):
        """Método: Impedir duplicidade"""
        dados = self.carregar_dados()
        if self.__titulo in dados:
            return False
        else:
            self.Cadastrar_Midia()
        pass

    def Registrar_status(self):
        """Método: Registrar status"""
        pass


# Classe: Filme
class Filme(Midia):
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
class Serie(Midia):
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
class Episodio:
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
