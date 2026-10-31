"""Usuario: credenciais, listas personalizadas e histórico de visualização."""

from datetime import datetime

from src.domain.historico import RegistroHistorico
from src.domain.listas import ListaPersonalizada


class Usuario:
    """Representa uma conta com listas e histórico de visualização."""
    FAVORITOS = "Favoritos"

    def __init__(self, login, senha, id=None):
        self.login = login
        self.senha = senha
        self.id = id
        self._listas = {}  # nome (casefold) -> ListaPersonalizada
        self._historico = []

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O usuário não pode ser vazio.")
        self._login = valor.strip()

    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("A senha não pode ser vazia.")
        self._senha = valor.strip()

    # -- listas -----------------------------------------------------------
    @property
    def listas(self):
        return list(self._listas.values())

    def adicionar_lista(self, lista):
        if lista.nome.casefold() in self._listas:
            raise ValueError(f"Já existe uma lista chamada '{lista.nome}'.")
        self._listas[lista.nome.casefold()] = lista

    def criar_lista(self, nome, limite=None):
        """Cria a lista respeitando o limite de listas (settings.json)."""
        if limite is not None and len(self._listas) >= limite:
            raise ValueError(f"Limite de {limite} lista(s) atingido.")
        lista = ListaPersonalizada(nome)
        self.adicionar_lista(lista)
        return lista

    def lista(self, nome):
        try:
            return self._listas[str(nome).strip().casefold()]
        except KeyError:
            raise ValueError(f"A lista '{nome}' não existe.") from None

    def apagar_lista(self, nome):
        self.lista(nome)
        del self._listas[str(nome).strip().casefold()]

    def adicionar_favorito(self, id_midia, limite=None):
        """Favoritos é uma lista comum, criada na primeira vez que é usada."""
        if self.FAVORITOS.casefold() not in self._listas:
            self.criar_lista(self.FAVORITOS, limite)
        self.lista(self.FAVORITOS).adicionar(id_midia)

    def remover_midia_de_todas(self, id_midia):
        for lista in self._listas.values():
            if id_midia in lista:
                lista.remover(id_midia)

    # -- histórico --------------------------------------------------------
    @property
    def historico(self):
        return list(self._historico)

    def adicionar_registro(self, registro):
        self._historico.append(registro)

    def registrar_conclusao(self, id_midia, descricao, minutos, quando=None):
        self.adicionar_registro(
            RegistroHistorico(id_midia, descricao, minutos, quando or datetime.now())
        )

    def remover_registros(self, id_midia, descricoes=None):
        """Remove do histórico a mídia inteira ou os itens indicados dela."""
        descricoes = None if descricoes is None else set(descricoes)
        self._historico = [
            registro for registro in self._historico
            if registro.midia_id != id_midia
            or (descricoes is not None and registro.descricao not in descricoes)
        ]
