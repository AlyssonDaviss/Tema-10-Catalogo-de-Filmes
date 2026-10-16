
class Midia:
    def __init__(
        self, titulo, tipo, genero, ano,
        classificacao_indicativa, elenco, status, id=0
    ):
        self.__titulo = titulo
        self.__tipo = tipo
        self.__genero = genero
        self.__ano = ano
        self.__classificacao_indicativa = classificacao_indicativa
        self.__elenco = elenco
        self.__status = status
        self._id = id

    @property
    def titulo(self):
        return self.__titulo

    @property
    def tipo(self):
        return self.__tipo

    @property
    def genero(self):
        return self.__genero

    def obter_id(self):
        return self._id

    def definir_id(self, id):
        self._id = id

    def obter_ano(self):
        return self.__ano

    def obter_classificacao_indicativa(self):
        return self.__classificacao_indicativa

    def obter_elenco(self):
        return self.__elenco

    def obter_status(self):
        return self.__status

    def Registrar_status(self):
        pass


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

    def obter_duracao(self):
        return self.__duracao


class Serie(Midia):
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

    def registrar_temporadas(
        self, numero_temporada, numero_episodios, data_lancamento
    ):
        titulo = f"Temporada {numero_temporada}"

        return Temporada(
            titulo, numero_episodios, data_lancamento
        )

    def obter_numero_temporadas(self):
        return self.__numero_temporadas

    def obter_numero_episodios(self):
        return self.__numero_episodios

    def atualizar_status(self):
        pass


class Temporada:
    def __init__(
        self, titulo, numero_episodios, data_lancamento, id=0
    ):
        self.__titulo = titulo
        self.__numero_episodios = numero_episodios
        self.__data_lancamento = data_lancamento
        self._id = id

    def obter_id(self):
        return self._id

    def definir_id(self, id):
        self._id = id

    def obter_titulo(self):
        return self.__titulo

    def obter_numero_episodios(self):
        return self.__numero_episodios

    def obter_data_lancamento(self):
        return self.__data_lancamento

class Episodio:
    def __init__(self, titulo, duracao):
        self.__titulo = titulo
        self.__duracao = duracao

    @classmethod
    def criar_automatico(cls, numero, duracao):
        return cls(f"Episódio {numero}", duracao)

    def obter_titulo(self):
        return self.__titulo

    def obter_duracao(self):
        return self.__duracao


