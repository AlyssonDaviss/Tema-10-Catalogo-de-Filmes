"""Menu interativo: as respostas do usuário são simuladas em input()."""

import builtins

import pytest

from repositories.cadastrar_midia import CadastrarMidia
from repositories.cadastrar_pessoa import CadastrarUsuario
from src.services.comandos import Comandos
from src.menu import Menu
from src.domain.midia import Filme
from src.domain.user import Usuario


def digitar(monkeypatch, *respostas):
    fila = iter(respostas)
    monkeypatch.setattr(builtins, "input", lambda _="": next(fila))


@pytest.fixture
def pasta(tmp_path):
    CadastrarUsuario(tmp_path).cadastrar(Usuario("ana", "123"))
    return tmp_path


def abrir(pasta):
    Menu(Comandos(pasta)).iniciar()






def test_cadastrar_filme_avaliar_e_marcar_assistido(pasta, monkeypatch):
    digitar(monkeypatch, "ana", "123",
            "2", "1", "1", "Matrix", "Ficção", "1999", "14", "Keanu Reeves", "136",
            "3", "1", "9,5", "4", "1", "3", "0", "0")
    abrir(pasta)
    filme = CadastrarMidia(pasta).obter(1)
    assert filme.nota == 9.5 and filme.finalizada
    assert CadastrarUsuario(pasta).carregar_usuario("0001").historico[0].descricao == "Matrix"


def test_serie_com_temporada_automatica_e_status_por_episodio(pasta, monkeypatch):
    digitar(monkeypatch, "ana", "123",
            "2", "1", "2", "Dark", "Ficção", "2017", "16", "", "1", "3", "50",
            "4", "1", "3", "1", "1", "3", "0", "0")
    abrir(pasta)
    serie = CadastrarMidia(pasta).obter(1)
    assert len(serie) == 3 and serie.status.value == "ASSISTINDO"




def test_listas_pelo_menu(pasta, monkeypatch):
    digitar(monkeypatch, "ana", "123",
            "3", "3", "Maratona", "0",           # Listas > criar
            "0")
    abrir(pasta)
    assert CadastrarUsuario(pasta).carregar_usuario("0001").lista("Maratona") is not None


