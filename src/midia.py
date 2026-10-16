from repositories.cadastrar_midia import CadastrarMidia


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
        # Um sublinhado só: as subclasses (Filme, Serie) conseguem acessar.
        self._repositorio = CadastrarMidia()

    @property
    def titulo(self):
        return self.__titulo

    @property
    def tipo(self):
        return self.__tipo

    @property
    def genero(self):
        return self.__genero

    def carregar_dados(self):
        return self._repositorio.carregar_dados()

    def Cadastrar_Midia(self):
        resultado = self._repositorio.cadastrar_midia(self)

        if resultado is False:
            return False

        self._id = resultado
        return True

    def obter_id(self):
        return self._id

    def Impedir_Duplicidade(self):
        dados = self.carregar_dados()

        for midia in dados.values():
            if midia["titulo"].casefold() == self.__titulo.casefold():
                return False

        return self.Cadastrar_Midia()

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

    def registrar_duracao(self):
        return self._repositorio.atualizar_duracao(
            self.obter_id(), self.__duracao
        )


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
        self._id_serie = id

    def registrar_temporadas(self):
        dados = self.carregar_dados()
        id_serie = str(self.obter_id())

        temporadas = dados.get(
            id_serie, {}
        ).get("temporadas", {})

        titulo = f"Temporada {len(temporadas) + 1}"
        numero_episodios = int(input("Número de episódios: "))
        data_lancamento = input("Data de lançamento: ")

        return Temporada(
            titulo, numero_episodios, data_lancamento
        )

    def cadastrar_temporada(self, temporada):
        resultado = self._repositorio.cadastrar_temporada(
            self._id_serie, temporada
        )

        if isinstance(resultado, str) and not resultado.isdigit():
            return resultado

        temporada._id = resultado
        return True

    def atualizar_status(self):
        pass


class Temporada:
    def __init__(self, titulo, numero_episodios, data_lancamento, id=0):
        self.__titulo = titulo
        self.__numero_episodios = numero_episodios
        self.__data_lancamento = data_lancamento
        self._id = id
        self.__repositorio = CadastrarMidia()

    def carregar_dados(self):
        return self.__repositorio.carregar_dados()

    def obter_id(self):
        return self._id

    def obter_titulo(self):
        return self.__titulo

    def obter_numero_episodios(self):
        return self.__numero_episodios

    def obter_data_lancamento(self):
        return self.__data_lancamento

    def registrar_episodios(self, id_serie, id_temporada, episodio):
        return self.__repositorio.registrar_episodio(
            id_serie, id_temporada, episodio
        )


class Episodio:
    def __init__(self, titulo, duracao, data_lancamento):
        self.__titulo = titulo
        self.__duracao = duracao
        self.__data_lancamento = data_lancamento

    def obter_titulo(self):
        return self.__titulo

    def obter_duracao(self):
        return self.__duracao

    def obter_data_lancamento(self):
        return self.__data_lancamento