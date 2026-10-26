"""Menu interativo: as respostas do usuário são simuladas em input()."""

import builtins

import pytest

from repositories.cadastrar_midia import CadastrarMidia
from repositories.cadastrar_pessoa import CadastrarUsuario
from src.comandos import Comandos
from src.menu import Menu
from src.midia import Filme
from src.user import Usuario


def digitar(monkeypatch, *respostas):
    fila = iter(respostas)
    monkeypatch.setattr(builtins, "input", lambda _="": next(fila))


@pytest.fixture
def pasta(tmp_path):
    CadastrarUsuario(tmp_path).cadastrar(Usuario("ana", "123"))
    return tmp_path


def abrir(pasta):
    Menu(Comandos(pasta)).iniciar()


def test_login_cria_conta_nova_sem_confirmacao(tmp_path, monkeypatch, capsys):
    digitar(monkeypatch, "bia", "senha", "0")
    abrir(tmp_path)
    assert CadastrarUsuario(tmp_path).obter_id("bia") == "0001"
    assert "Conta criada" in capsys.readouterr().out


def test_senha_errada_pede_novamente(pasta, monkeypatch, capsys):
    digitar(monkeypatch, "ana", "errada", "ana", "123", "0")
    abrir(pasta)
    saida = capsys.readouterr().out
    assert "Senha incorreta" in saida and "Login realizado" in saida


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


def test_erro_de_regra_nao_fecha_o_menu(pasta, monkeypatch, capsys):
    CadastrarMidia(pasta).cadastrar(Filme("A", "B", 2000, "L", "", 90))
    digitar(monkeypatch, "ana", "123",
            "2", "1", "1", "a", "B", "2000", "L", "", "90", "0", "0")
    abrir(pasta)
    assert "Já existe" in capsys.readouterr().out


def test_listas_pelo_menu(pasta, monkeypatch):
    digitar(monkeypatch, "ana", "123",
            "5", "5", "0",                       # Configurações > carregar exemplos
            "3", "3", "Maratona", "0",           # Listas > criar
            "0")
    abrir(pasta)
    assert CadastrarUsuario(pasta).carregar_usuario("0001").lista("Maratona") is not None


def test_continuar_com_a_sessao_existente(pasta, monkeypatch, capsys):
    Comandos(pasta).entrar("ana", "123")
    digitar(monkeypatch, "0")               # sessão existente, sair
    abrir(pasta)
    assert "Olá, ana" in capsys.readouterr().out
