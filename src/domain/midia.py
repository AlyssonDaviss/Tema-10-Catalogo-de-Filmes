"""Modelo de domínio: Midia (base), Filme, Serie, Temporada e Episodio.

Serie agrega Temporada, que contém Episodio. Filme e Episodio compartilham o
comportamento de "coisa que se assiste" (duração, status e nota) através do
mixin AssistivelMixin, então as validações existem uma única vez.
"""

import unicodedata
from abc import ABC, abstractmethod
from datetime import date
from enum import Enum


# --------------------------------------------------------------------------
# Utilitários
# --------------------------------------------------------------------------
def normalizar(texto):
    """Minúsculas e sem acentos: 'Série' -> 'serie'."""
    texto = unicodedata.normalize("NFD", str(texto).strip().casefold())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def media(valores):
    """Média aritmética ou None quando não há valores."""
    valores = list(valores)
    return sum(valores) / len(valores) if valores else None


def _texto(valor, nome):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{nome} não pode ser vazio.")
    return valor.strip()


def _inteiro_positivo(valor, nome):
    try:
        inteiro = int(valor)
    except (TypeError, ValueError):
        raise ValueError(f"{nome} deve ser um número inteiro.") from None
    if inteiro <= 0:
        raise ValueError(f"{nome} deve ser positivo.")
    return inteiro


class Status(Enum):
    """Estados de visualização de um filme ou episódio."""
    NAO_ASSISTIDO = "NÃO ASSISTIDO"
    ASSISTINDO = "ASSISTINDO"
    ASSISTIDO = "ASSISTIDO"

    @classmethod
    def converter(cls, valor):
        """Aceita um Status ou texto livre ('assistido', 'nao-assistido')."""
        if isinstance(valor, cls):
            return valor
        texto = normalizar(valor).replace("_", " ").replace("-", " ")
        for status in cls:
            if normalizar(status.value) == texto:
                return status
        raise ValueError(
            "Status inválido. Use: NÃO ASSISTIDO, ASSISTINDO ou ASSISTIDO."
        )


# --------------------------------------------------------------------------
# Comportamento comum a Filme e Episodio
# --------------------------------------------------------------------------
class AssistivelMixin:
    """Mixin com duração (> 0), status e nota (0 a 10, opcional) validados.

    Combinado a Midia por herança dupla em Filme(AssistivelMixin, Midia);
    Episodio também o reutiliza.
    """

    def __init__(self, duracao, status=Status.NAO_ASSISTIDO, nota=None):
        self.duracao = duracao
        self.status = status
        self.nota = nota

    @property
    def duracao(self):
        return self._duracao

    @duracao.setter
    def duracao(self, valor):
        try:
            valor = float(str(valor).replace(",", "."))
        except ValueError:
            raise ValueError("A duração deve ser numérica.") from None
        if not valor > 0:
            raise ValueError("A duração deve ser maior que zero.")
        self._duracao = valor

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, valor):
        self._status = Status.converter(valor)

    @property
    def nota(self):
        return self._nota

    @nota.setter
    def nota(self, valor):
        if valor is None:
            self._nota = None
            return
        try:
            nota = float(str(valor).replace(",", "."))
        except ValueError:
            raise ValueError("A nota deve ser numérica.") from None
        if not 0 <= nota <= 10:
            raise ValueError("A nota deve estar entre 0 e 10.")
        self._nota = nota

    @property
    def minutos_assistidos(self):
        return self._duracao if self._status is Status.ASSISTIDO else 0.0


# --------------------------------------------------------------------------
# Midia (classe base)
# --------------------------------------------------------------------------
class Midia(ABC):
    """Dados comuns a filmes e séries; o resto é definido nas subclasses."""

    TIPO = None

    def __init__(self, titulo, genero, ano, classificacao, elenco=(), id=None):
        self.titulo = titulo
        self.genero = genero
        self.ano = ano
        self.classificacao = classificacao
        self.elenco = elenco
        self.id = id

    # -- atributos validados ------------------------------------------------
    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        self._titulo = _texto(valor, "O título")

    @property
    def genero(self):
        return self._genero

    @genero.setter
    def genero(self, valor):
        self._genero = _texto(valor, "O gênero")

    @property
    def ano(self):
        return self._ano

    @ano.setter
    def ano(self, valor):
        self._ano = _inteiro_positivo(valor, "O ano")

    @property
    def classificacao(self):
        return self._classificacao

    @classificacao.setter
    def classificacao(self, valor):
        self._classificacao = _texto(str(valor), "A classificação indicativa")

    @property
    def elenco(self):
        return list(self._elenco)

    @elenco.setter
    def elenco(self, valor):
        if isinstance(valor, str):
            valor = valor.split(",")
        self._elenco = [nome.strip() for nome in valor if nome.strip()]

    @property
    def tipo(self):
        return self.TIPO

    @property
    def chave(self):
        """Identidade para duplicidade: título + tipo + ano."""
        return (self.titulo.casefold(), self.tipo, self.ano)

    @property
    def finalizada(self):
        return self.status is Status.ASSISTIDO

    # -- contrato das subclasses -------------------------------------------
    @property
    @abstractmethod
    def status(self): ...

    @property
    @abstractmethod
    def nota_media(self): ...

    @property
    @abstractmethod
    def duracao_total(self): ...

    @property
    @abstractmethod
    def minutos_assistidos(self): ...

    @abstractmethod
    def definir_status(self, status, temporada=None, episodio=None):
        """Altera o status e devolve [(descrição, minutos)] do que foi concluído agora."""

    @abstractmethod
    def avaliar(self, nota, temporada=None, episodio=None): ...

    @abstractmethod
    def _detalhe(self): ...

    def para_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "titulo": self.titulo,
            "genero": self.genero,
            "ano": self.ano,
            "classificacao": self.classificacao,
            "elenco": self.elenco,
        }

    @staticmethod
    def de_dict(dados):
        classe = {"FILME": Filme, "SERIE": Serie}[dados["tipo"]]
        return classe._de_dict(dados)

    # -- métodos especiais -------------------------------------------------
    def __str__(self):
        nota = self.nota_media
        nota = "sem nota" if nota is None else f"nota {nota:.1f}"
        return (
            f"{self.titulo} ({self.ano}) [{self.tipo}] | {self._detalhe()} "
            f"| {self.status.value} | {nota}"
        )

    def __repr__(self):
        return (
            f"{type(self).__name__}(id={self.id!r}, titulo={self.titulo!r}, "
            f"ano={self.ano!r})"
        )

    def __eq__(self, outro):
        if not isinstance(outro, Midia):
            return NotImplemented
        return (self.titulo.casefold(), self.tipo) == (
            outro.titulo.casefold(),
            outro.tipo,
        )

    def __hash__(self):
        return hash((self.titulo.casefold(), self.tipo))

    def __lt__(self, outro):
        """Ordena por nota média; mídia sem nota fica abaixo das avaliadas."""
        if not isinstance(outro, Midia):
            return NotImplemented
        return self._nota_para_ordenar() < outro._nota_para_ordenar()

    def _nota_para_ordenar(self):
        nota = self.nota_media
        return -1 if nota is None else nota


# --------------------------------------------------------------------------
# Filme
# --------------------------------------------------------------------------
class Filme(AssistivelMixin, Midia):
    """Representa um filme com duração, status e nota."""
    TIPO = "FILME"

    def __init__(
        self, titulo, genero, ano, classificacao, elenco, duracao,
        status=Status.NAO_ASSISTIDO, nota=None, id=None,
    ):
        Midia.__init__(self, titulo, genero, ano, classificacao, elenco, id)
        AssistivelMixin.__init__(self, duracao, status, nota)

    @property
    def nota_media(self):
        return self.nota

    @property
    def duracao_total(self):
        return self.duracao

    def definir_status(self, status, temporada=None, episodio=None):
        self._sem_episodios(temporada, episodio)
        status = Status.converter(status)
        concluido = status is Status.ASSISTIDO and not self.finalizada
        self.status = status
        return [(self.titulo, self.duracao)] if concluido else []

    def avaliar(self, nota, temporada=None, episodio=None):
        self._sem_episodios(temporada, episodio)
        self.nota = nota

    @staticmethod
    def _sem_episodios(temporada, episodio):
        if temporada is not None or episodio is not None:
            raise ValueError("Filmes não possuem temporadas nem episódios.")

    def _detalhe(self):
        return f"{self.duracao:g} min"

    def para_dict(self):
        return {
            **super().para_dict(),
            "duracao": self.duracao,
            "status": self.status.value,
            "nota": self.nota,
        }

    @classmethod
    def _de_dict(cls, d):
        return cls(
            d["titulo"], d["genero"], d["ano"], d["classificacao"],
            d["elenco"], d["duracao"], d["status"], d["nota"], d["id"],
        )


# --------------------------------------------------------------------------
# Episodio, Temporada e Serie
# --------------------------------------------------------------------------
class Episodio(AssistivelMixin):
    """Representa um episódio dentro de uma temporada."""
    def __init__(
        self, temporada, numero, titulo, duracao, data_lancamento=None,
        status=Status.NAO_ASSISTIDO, nota=None,
    ):
        super().__init__(duracao, status, nota)
        self.temporada = temporada
        self.numero = numero
        self.titulo = titulo
        self.data_lancamento = data_lancamento

    @property
    def temporada(self):
        return self._temporada

    @temporada.setter
    def temporada(self, valor):
        self._temporada = _inteiro_positivo(valor, "O número da temporada")

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, valor):
        self._numero = _inteiro_positivo(valor, "O número do episódio")

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        self._titulo = _texto(valor, "O título do episódio")

    @property
    def data_lancamento(self):
        return self._data_lancamento

    @data_lancamento.setter
    def data_lancamento(self, valor):
        if valor is None or isinstance(valor, date):
            self._data_lancamento = valor
            return
        try:
            self._data_lancamento = date.fromisoformat(valor)
        except (TypeError, ValueError):
            raise ValueError("A data deve estar no formato AAAA-MM-DD.") from None

    def para_dict(self):
        lancamento = self.data_lancamento
        return {
            "numero": self.numero,
            "titulo": self.titulo,
            "duracao": self.duracao,
            "data_lancamento": lancamento.isoformat() if lancamento else None,
            "status": self.status.value,
            "nota": self.nota,
        }

    @classmethod
    def de_dict(cls, temporada, d):
        return cls(
            temporada, d["numero"], d["titulo"], d["duracao"],
            d["data_lancamento"], d["status"], d["nota"],
        )

    def __str__(self):
        nota = "sem nota" if self.nota is None else f"nota {self.nota:g}"
        return (
            f"T{self.temporada}E{self.numero} {self.titulo} "
            f"({self.duracao:g} min) | {self.status.value} | {nota}"
        )

    def __repr__(self):
        return f"Episodio(T{self.temporada}E{self.numero}, {self.titulo!r})"


class Temporada:
    """Agrupa episódios de uma série."""
    def __init__(self, numero):
        self.numero = numero
        self._episodios = {}

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, valor):
        self._numero = _inteiro_positivo(valor, "O número da temporada")

    @property
    def episodios(self):
        return [self._episodios[n] for n in sorted(self._episodios)]

    def adicionar_episodio(self, episodio):
        if episodio.temporada != self.numero:
            raise ValueError("O episódio pertence a outra temporada.")
        if episodio.numero in self._episodios:
            raise ValueError(
                f"O episódio {episodio.numero} já existe na temporada {self.numero}."
            )
        self._episodios[episodio.numero] = episodio

    def episodio(self, numero):
        try:
            return self._episodios[int(numero)]
        except (KeyError, ValueError):
            raise ValueError(
                f"O episódio {numero} não existe na temporada {self.numero}."
            ) from None

    @property
    def duracao_total(self):
        return sum(ep.duracao for ep in self._episodios.values())

    @property
    def nota_media(self):
        return media(ep.nota for ep in self._episodios.values() if ep.nota is not None)

    def __len__(self):
        return len(self._episodios)

    def __iter__(self):
        return iter(self.episodios)

    def __str__(self):
        return f"Temporada {self.numero} ({len(self)} episódios)"


class Serie(Midia):
    """Representa uma série composta por temporadas e episódios."""
    TIPO = "SERIE"

    def __init__(self, titulo, genero, ano, classificacao, elenco=(), id=None):
        super().__init__(titulo, genero, ano, classificacao, elenco, id)
        self._temporadas = {}

    # -- estrutura ------------------------------------------------------
    @property
    def temporadas(self):
        return [self._temporadas[n] for n in sorted(self._temporadas)]

    @property
    def episodios(self):
        return [ep for temporada in self.temporadas for ep in temporada]

    def temporada(self, numero):
        try:
            return self._temporadas[int(numero)]
        except (KeyError, ValueError):
            raise ValueError(f"A temporada {numero} não existe.") from None

    def adicionar_episodio(self, episodio):
        temporada = self._temporadas.setdefault(
            episodio.temporada, Temporada(episodio.temporada)
        )
        temporada.adicionar_episodio(episodio)

    def criar_temporada(self, numero, quantidade, duracao, data_lancamento=None):
        """Cria uma temporada com 'quantidade' episódios genéricos ("Episódio N")."""
        numero = _inteiro_positivo(numero, "O número da temporada")
        quantidade = _inteiro_positivo(quantidade, "A quantidade de episódios")
        if numero in self._temporadas:
            raise ValueError(f"A temporada {numero} já existe.")
        # Constrói tudo antes de inserir: uma entrada inválida não deixa lixo.
        episodios = [
            Episodio(numero, n, f"Episódio {n}", duracao, data_lancamento)
            for n in range(1, quantidade + 1)
        ]
        for episodio in episodios:
            self.adicionar_episodio(episodio)

    # -- valores calculados ---------------------------------------------
    @property
    def status(self):
        """Derivado dos episódios: a série é ASSISTIDA quando todos estão."""
        status = {ep.status for ep in self.episodios}
        if not status or status == {Status.NAO_ASSISTIDO}:
            return Status.NAO_ASSISTIDO
        if status == {Status.ASSISTIDO}:
            return Status.ASSISTIDO
        return Status.ASSISTINDO

    @property
    def nota_media(self):
        return media(ep.nota for ep in self.episodios if ep.nota is not None)

    @property
    def duracao_total(self):
        return sum(ep.duracao for ep in self.episodios)

    @property
    def minutos_assistidos(self):
        return sum(ep.minutos_assistidos for ep in self.episodios)

    @property
    def episodios_assistidos(self):
        return sum(1 for ep in self.episodios if ep.status is Status.ASSISTIDO)

    # -- operações ------------------------------------------------------
    def definir_status(self, status, temporada=None, episodio=None):
        """Aplica o status à série toda, a uma temporada ou a um episódio."""
        status = Status.converter(status)
        concluidos = []
        for ep in self.escopo(temporada, episodio):
            if status is Status.ASSISTIDO and ep.status is not Status.ASSISTIDO:
                concluidos.append(
                    (f"{self.titulo} T{ep.temporada}E{ep.numero}", ep.duracao)
                )
            ep.status = status
        return concluidos

    def avaliar(self, nota, temporada=None, episodio=None):
        """Aplica a nota ao episódio, à temporada ou à série inteira."""
        for ep in self.escopo(temporada, episodio):
            ep.nota = nota

    def escopo(self, temporada, episodio):
        """Episódios afetados: a série toda, uma temporada ou um único episódio."""
        if temporada is None:
            if episodio is not None:
                raise ValueError("Informe também a temporada do episódio.")
            alvo = self.episodios
        elif episodio is None:
            alvo = self.temporada(temporada).episodios
        else:
            alvo = [self.temporada(temporada).episodio(episodio)]
        if not alvo:
            raise ValueError("A série ainda não possui episódios.")
        return alvo

    def _detalhe(self):
        return f"{len(self.temporadas)} temporada(s), {len(self)} episódios"

    def para_dict(self):
        return {
            **super().para_dict(),
            "temporadas": [
                {"numero": t.numero, "episodios": [e.para_dict() for e in t]}
                for t in self.temporadas
            ],
        }

    @classmethod
    def _de_dict(cls, d):
        serie = cls(d["titulo"], d["genero"], d["ano"], d["classificacao"],
                    d["elenco"], d["id"])
        for temporada in d["temporadas"]:
            for ep in temporada["episodios"]:
                serie.adicionar_episodio(Episodio.de_dict(temporada["numero"], ep))
        return serie

    def __len__(self):
        """Número total de episódios."""
        return sum(len(t) for t in self._temporadas.values())
