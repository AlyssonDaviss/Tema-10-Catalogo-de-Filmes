
class Midia:
    """Classe base para filmes e séries."""

    def __init__(
        self,
        titulo,
        tipo,
        genero,
        ano,
        classificacao_indicativa,
        elenco,
        id=0
    ):
        self.titulo = titulo
        self.tipo = tipo
        self.genero = genero
        self.ano = ano
        self.classificacao_indicativa = classificacao_indicativa
        self.elenco = elenco
        self._id = id

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O título não pode ser vazio.")
        self.__titulo = valor.strip()

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, valor):
        if not isinstance(valor, str):
            raise ValueError("O tipo deve ser um texto.")

        valor = valor.strip().upper()

        if valor not in ("FILME", "SERIE"):
            raise ValueError("O tipo deve ser FILME ou SERIE.")

        self.__tipo = valor

    @property
    def genero(self):
        return self.__genero

    @genero.setter
    def genero(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O gênero não pode ser vazio.")
        self.__genero = valor.strip()

    @property
    def ano(self):
        return self.__ano

    @ano.setter
    def ano(self, valor):
        try:
            ano = int(valor)
        except (TypeError, ValueError):
            raise ValueError("O ano deve ser um número inteiro.")

        if ano <= 0:
            raise ValueError("O ano deve ser positivo.")

        self.__ano = ano

    @property
    def classificacao_indicativa(self):
        return self.__classificacao_indicativa

    @classificacao_indicativa.setter
    def classificacao_indicativa(self, valor):
        if valor is None or not str(valor).strip():
            raise ValueError("Informe a classificação indicativa.")
        self.__classificacao_indicativa = str(valor).strip()

    @property
    def elenco(self):
        return self.__elenco.copy()

    @elenco.setter
    def elenco(self, valor):
        if isinstance(valor, str):
            valor = [
                nome.strip()
                for nome in valor.split(",")
                if nome.strip()
            ]

        if not isinstance(valor, (list, tuple)):
            raise ValueError("O elenco deve ser uma lista.")

        self.__elenco = list(valor)

    def obter_id(self):
        return self._id

    def definir_id(self, id):
        self._id = id

    def obter_ano(self):
        return self.ano

    def obter_classificacao_indicativa(self):
        return self.classificacao_indicativa

    def obter_elenco(self):
        return self.elenco

    def __str__(self):
        return f"{self.titulo} ({self.ano}) - {self.tipo}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"titulo={self.titulo!r}, "
            f"ano={self.ano!r}, "
            f"id={self._id!r})"
        )

    def __eq__(self, outro):
        if not isinstance(outro, Midia):
            return NotImplemented

        return (
            self.titulo.casefold(),
            self.tipo,
            self.ano
        ) == (
            outro.titulo.casefold(),
            outro.tipo,
            outro.ano
        )

    def __lt__(self, outro):
        if not isinstance(outro, Midia):
            return NotImplemented

        return (
            self.titulo.casefold(),
            self.ano
        ) < (
            outro.titulo.casefold(),
            outro.ano
        )


class Filme(Midia):
    """Representa um filme."""

    def __init__(
        self,
        titulo,
        genero,
        ano,
        classificacao_indicativa,
        elenco,
        duracao=1,
        id=0
    ):
        super().__init__(
            titulo,
            "FILME",
            genero,
            ano,
            classificacao_indicativa,
            elenco,
            id
        )
        self.duracao = duracao

    @property
    def duracao(self):
        return self.__duracao

    @duracao.setter
    def duracao(self, valor):
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            raise ValueError("A duração deve ser numérica.")

        if valor <= 0:
            raise ValueError("A duração deve ser maior que zero.")

        self.__duracao = valor

    def obter_duracao(self):
        return self.duracao

    def __str__(self):
        return f"{super().__str__()} - {self.duracao:g} minutos"


class Serie(Midia):
    """Representa uma série composta por temporadas."""

    def __init__(
        self,
        titulo,
        tipo,
        genero,
        ano,
        classificacao_indicativa,
        elenco,
        numero_temporadas=0,
        numero_episodios=0,
        id=0
    ):
        super().__init__(
            titulo,
            "SERIE",
            genero,
            ano,
            classificacao_indicativa,
            elenco,
            id
        )

        if numero_temporadas < 0 or numero_episodios < 0:
            raise ValueError("As quantidades não podem ser negativas.")

        self.__temporadas = []

    @property
    def temporadas(self):
        return self.__temporadas.copy()

    def registrar_temporadas(
        self,
        numero_temporada,
        numero_episodios,
        duracao_media,
        data_lancamento,
        titulo=None
    ):
        """Cria uma temporada e gera seus episódios automaticamente."""
        if not titulo:
            titulo = f"Temporada {numero_temporada}"

        quantidade = int(numero_episodios)

        if quantidade <= 0:
            raise ValueError(
                "A temporada deve ter pelo menos um episódio."
            )

        temporada = Temporada(
            titulo=titulo,
            numero=numero_temporada,
            data_lancamento=data_lancamento
        )

        for numero in range(1, quantidade + 1):
            episodio = Episodio.criar_automatico(
                numero=numero,
                duracao=duracao_media,
                data_lancamento=data_lancamento
            )
            temporada.adicionar_episodio(episodio)

        self.adicionar_temporada(temporada)
        return temporada

    def adicionar_temporada(self, temporada):
        if not isinstance(temporada, Temporada):
            raise TypeError("É necessário informar uma Temporada.")

        if any(
            item.numero == temporada.numero
            for item in self.__temporadas
        ):
            raise ValueError("Essa temporada já está cadastrada.")

        self.__temporadas.append(temporada)
        self.__temporadas.sort(key=lambda item: item.numero)

    def obter_numero_temporadas(self):
        return len(self.__temporadas)

    def obter_numero_episodios(self):
        return sum(len(temporada) for temporada in self.__temporadas)

    def __len__(self):
        return self.obter_numero_episodios()

    def __str__(self):
        return (
            f"{super().__str__()} - "
            f"{self.obter_numero_temporadas()} temporadas, "
            f"{self.obter_numero_episodios()} episódios"
        )
    
    def obter_temporadas(self):
        return self.__temporadas


class Temporada:
    """Agrupa os episódios de uma temporada."""

    def __init__(
        self,
        titulo,
        numero=None,
        data_lancamento=None,
        id=0
    ):
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError(
                "O título da temporada não pode ser vazio."
            )

        if numero is None:
            numero = 1

        try:
            numero = int(numero)
        except (TypeError, ValueError):
            raise ValueError(
                "O número da temporada deve ser inteiro."
            )

        if numero <= 0:
            raise ValueError(
                "O número da temporada deve ser positivo."
            )

        self.__titulo = titulo.strip()
        self.__numero = numero
        self.__data_lancamento = data_lancamento
        self.__episodios = []
        self._id = id

    @property
    def titulo(self):
        return self.__titulo

    @property
    def numero(self):
        return self.__numero

    @property
    def data_lancamento(self):
        return self.__data_lancamento

    @property
    def episodios(self):
        return self.__episodios.copy()

    def adicionar_episodio(self, episodio):
        if not isinstance(episodio, Episodio):
            raise TypeError("É necessário informar um Episodio.")

        if any(
            item.numero == episodio.numero
            for item in self.__episodios
        ):
            raise ValueError("Esse episódio já está cadastrado.")

        self.__episodios.append(episodio)
        self.__episodios.sort(key=lambda item: item.numero)

    def obter_id(self):
        return self._id

    def definir_id(self, id):
        self._id = id

    def obter_titulo(self):
        return self.titulo

    def obter_numero(self):
        return self.numero

    def obter_numero_episodios(self):
        return len(self.__episodios)

    def obter_duracao_media(self):
        if not self.__episodios:
            return 0

        return (
            sum(ep.duracao for ep in self.__episodios)
            / len(self.__episodios)
        )

    def obter_duracao_total(self):
        return sum(ep.duracao for ep in self.__episodios)

    def obter_data_lancamento(self):
        return self.data_lancamento

    def __len__(self):
        return len(self.__episodios)

    def __str__(self):
        return f"{self.titulo} - {len(self)} episódios"


class Episodio:
    """Representa um episódio individual de uma série."""

    def __init__(
        self,
        titulo,
        duracao,
        numero=1,
        data_lancamento=None,
        id=0
    ):
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError(
                "O título do episódio não pode ser vazio."
            )

        self.__titulo = titulo.strip()
        self.numero = numero
        self.duracao = duracao
        self.data_lancamento = data_lancamento
        self._id = id

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, valor):
        try:
            valor = int(valor)
        except (TypeError, ValueError):
            raise ValueError(
                "O número do episódio deve ser inteiro."
            )

        if valor <= 0:
            raise ValueError(
                "O número do episódio deve ser positivo."
            )

        self.__numero = valor

    @property
    def titulo(self):
        return self.__titulo

    @property
    def duracao(self):
        return self.__duracao

    @duracao.setter
    def duracao(self, valor):
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            raise ValueError("A duração deve ser numérica.")

        if valor <= 0:
            raise ValueError("A duração deve ser maior que zero.")

        self.__duracao = valor

    @property
    def data_lancamento(self):
        return self.__data_lancamento

    @data_lancamento.setter
    def data_lancamento(self, valor):
        self.__data_lancamento = valor

    @classmethod
    def criar_automatico(
        cls,
        numero,
        duracao,
        data_lancamento=None
    ):
        return cls(
            titulo=f"Episódio {numero}",
            duracao=duracao,
            numero=numero,
            data_lancamento=data_lancamento
        )

    def obter_id(self):
        return self._id

    def definir_id(self, id):
        self._id = id

    def obter_titulo(self):
        return self.titulo

    def obter_duracao(self):
        return self.duracao

    def __str__(self):
        return f"{self.titulo} - {self.duracao:g} minutos"

    def __repr__(self):
        return (
            f"Episodio(titulo={self.titulo!r}, "
            f"numero={self.numero!r}, "
            f"duracao={self.duracao!r})"
        )
