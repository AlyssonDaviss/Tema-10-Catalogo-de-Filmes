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
        status,
        id = 0
    ):
        self.__titulo = titulo
        self.__tipo = tipo
        self.__genero = genero
        self.__ano = ano
        self.__classificacao_indicativa = classificacao_indicativa
        self.__elenco = elenco
        self.__status = status
        self._id = id

    def carregar_dados(self):
        caminho = Path(__file__).resolve().parent.parent / "data" / "midia_dic.json"

        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        return dados

    def Cadastrar_Midia(self):
        dados = self.carregar_dados()

        self._id = str(len(dados) + 1).zfill(4)

        if self.__tipo == "filme":
            dados[self._id] = {
                "tipo": self.__tipo,
                "titulo": self.__titulo,
                "genero":  self.__genero,
                "duracao": ""
            }

        elif self.__tipo == "serie":

            dados[self._id] = {
                "tipo": self.__tipo,
                "titulo": self.__titulo,
                "genero": self.__genero,
                "temporadas": {}
            }

        caminho = Path(__file__).resolve().parent.parent / "data" / "midia_dic.json"

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

        return True

    def obter_id(self):
        return self._id

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
    def __init__(
        self, titulo, genero, ano, classificacao_indicativa,
        elenco, status, duracao, id=0
    ):
        super().__init__(
            titulo, "filme", genero, ano,
            classificacao_indicativa, elenco, status, id
        )

        self.__duracao = duracao

    def registrar_duracao(self):
        """Método: Registrar duração"""
        dados = self.carregar_dados()
        if self.obter_id() in dados:
            dados[self.obter_id()]["duracao"] = self.__duracao

            caminho = Path(__file__).resolve().parent.parent / "data" / "midia_dic.json"
                
            with open(caminho, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, indent=4, ensure_ascii=False)
            return True
        else:
            return "ID não cadastrado."

# Classe: Série
class Serie(Midia):
    """
    Classe: Série
    Herda de: Mídia
    Atributos: nº Temporadas, nº Episódios e Nota opcional
    Métodos: Registrar temporadas e Atualizar status
    """

    def __init__(
        self, titulo, tipo, genero, ano,
        classificacao_indicativa, elenco, status,
        numero_temporadas=0, numero_episodios=0,
        nota=None, id=0
    ):
        super().__init__(
            titulo, tipo, genero, ano,
            classificacao_indicativa, elenco, status, id
        )
        self.__numero_temporadas = numero_temporadas
        self.__numero_episodios = numero_episodios
        self.__nota = nota
        self._id_serie = id

    def registrar_temporadas(self):
        """Método: Registrar temporadas"""
        dados = self.carregar_dados()
        id_serie = str(self.obter_id())

        temporadas = dados.get(id_serie, {}).get("temporadas", {})

        titulo = f"Temporada {len(temporadas) + 1}"
        numero_episodios = int(input("Número de episódios: "))
        data_lancamento = input("Data de lançamento: ")

        temporada = Temporada(
            titulo,
            numero_episodios,
            data_lancamento
        )

        return temporada

    def cadastrar_temporada(self, temporada):
        """Método: Cadastrar temporada"""
        dados = self.carregar_dados()
        id_serie = str(self._id_serie)

        if id_serie not in dados:
            return "ID não cadastrado."

        temporadas = dados[id_serie].setdefault("temporadas", {})

        ids = [int(i) for i in temporadas if i.isdigit()]

        id_temporada = str(max(ids, default=0) + 1).zfill(4)
        temporada._id = id_temporada

        temporadas[id_temporada] = {
            "titulo": temporada.obter_titulo(),
            "numero_episodios": temporada.obter_numero_episodios(),
            "data_lancamento": temporada.obter_data_lancamento(),
            "episodios": {}
        }

        caminho = Path(__file__).resolve().parent.parent / "data" / "midia_dic.json"

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

        return True

    def atualizar_status(self):
        """Método: Atualizar status"""
        pass


# Classe: Temporada
class Temporada:
    """
    Classe: Temporada
    Se relaciona com: Série e Episódio
    Atributos: Título, nº Episódios, Data de lançamento
    Métodos: Registrar episódios
    """

    def __init__(self, titulo, numero_episodios, data_lancamento, id=0):
        self.__titulo = titulo
        self.__numero_episodios = numero_episodios
        self.__data_lancamento = data_lancamento
        self._id = id

    def carregar_dados(self):
        caminho = Path(__file__).resolve().parent.parent / "data" / "midia_dic.json"

        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        return dados
    def obter_id(self):
        return self._id

    def obter_titulo(self):
        return self.__titulo

    def obter_numero_episodios(self):
        return self.__numero_episodios

    def obter_data_lancamento(self):
        return self.__data_lancamento

    def registrar_episodios(self, id_serie, id_temporada, episodio):
        """Método: Registrar episódios"""
        dados = self.carregar_dados()

        id_serie = str(id_serie)
        id_temporada = str(id_temporada)

        if id_serie not in dados:
            return "Série não cadastrada."

        temporadas = dados[id_serie].get("temporadas", {})

        if id_temporada not in temporadas:
            return "Temporada não cadastrada."

        episodios = temporadas[id_temporada].setdefault("episodios", {})

        if len(episodios) >= temporadas[id_temporada]["numero_episodios"]:
            return "Limite de episódios atingido."

        ids = [int(i) for i in episodios if i.isdigit()]
        id_episodio = str(max(ids, default=0) + 1).zfill(4)

        episodios[id_episodio] = {
            "numero_episodio": len(episodios) + 1,
            "titulo": episodio.obter_titulo(),
            "duracao": episodio.obter_duracao(),
            "data_lancamento": episodio.obter_data_lancamento()
        }

        caminho = (
            Path(__file__).resolve().parent.parent
            / "data" / "midia_dic.json"
        )

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

        return True

# Classe: Episódio
class Episodio:
    """
    Classe: Episódio
    Se relaciona com: Temporada e Avaliação
    Atributos: Nº Episódio, Título, Duração e Data de lançamento
    Métodos: Obter atributos
    """

    def __init__(
        self,
        titulo,
        duracao,
        data_lancamento
    ):
        self.__titulo = titulo
        self.__duracao = duracao
        self.__data_lancamento = data_lancamento

    def obter_titulo(self):
        return self.__titulo

    def obter_duracao(self):
        return self.__duracao

    def obter_data_lancamento(self):
        return self.__data_lancamento