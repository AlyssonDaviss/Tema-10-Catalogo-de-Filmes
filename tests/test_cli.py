"""Subcomandos: executar([...]) numa pasta temporária."""

import pytest

from src.cli import executar


@pytest.fixture
def cli(tmp_path, capsys):
    """Roda um subcomando e devolve (código, saída, erro)."""
    def rodar(*argumentos):
        codigo = executar([str(a) for a in argumentos], tmp_path)
        saida = capsys.readouterr()
        return codigo, saida.out, saida.err
    return rodar


FILME = ("midia", "adicionar", "--tipo", "filme", "--titulo", "Matrix", "--genero", "Ficção",
         "--ano", 1999, "--classificacao", 14, "--duracao", 136)


def test_fluxo_de_filme_ate_o_relatorio_top(cli):
    cli("usuario", "entrar", "ana", "--senha", "123")
    assert cli(*FILME)[0] == 0
    cli("midia", "atualizar-status", 1, "assistido")
    cli("midia", "avaliar", 1, "9,5")
    codigo, saida, _ = cli("midia", "relatorio", "top")
    assert codigo == 0 and "1º Matrix (FILME) - 9.50" in saida
    assert "136 min" in cli("midia", "relatorio", "tempo")[1]


def test_fluxo_de_serie_com_temporada_automatica(cli):
    cli("usuario", "entrar", "ana", "--senha", "123")
    cli("midia", "adicionar", "--tipo", "serie", "--titulo", "Dark", "--genero", "Ficção",
        "--ano", 2017, "--classificacao", 16)
    assert cli("serie", "adicionar-temporada", 1, "--episodios", 3, "--duracao", 50)[0] == 0
    cli("serie", "adicionar-episodio", 1, "-t", 2, "-n", 1, "--titulo", "Piloto", "--duracao", 40)
    cli("serie", "atualizar-status", 1, "assistido", "-t", 1)
    saida = cli("serie", "episodios", 1)[1]
    assert "Temporada 2 (1 episódios)" in saida and "T1E3" in saida
    assert "ASSISTINDO" in cli("midia", "listar", "--tipo", "serie")[1]  # T2 ainda não vista
    assert "3 de 4" in cli("midia", "relatorio", "series")[1]


def test_erro_de_regra_vira_mensagem_e_codigo_1(cli):
    assert cli(*FILME)[0] == 0
    codigo, _, erro = cli(*FILME)
    assert codigo == 1 and "Já existe" in erro
    codigo, _, erro = cli("midia", "avaliar", 1, 11)
    assert codigo == 1 and "entre 0 e 10" in erro
    codigo, _, erro = cli("midia", "avaliar", 99, 5)
    assert codigo == 1 and "não encontrada" in erro


def test_filme_exige_duracao_e_serie_nao_aceita(cli):
    codigo, _, erro = cli("midia", "adicionar", "--tipo", "filme", "--titulo", "A", "--genero", "B",
                          "--ano", 2000, "--classificacao", "L")
    assert codigo == 1 and "duração" in erro
    codigo, _, erro = cli("midia", "adicionar", "--tipo", "serie", "--titulo", "A", "--genero", "B",
                          "--ano", 2000, "--classificacao", "L", "--duracao", 30)
    assert codigo == 1 and "Séries não têm duração" in erro


def test_acoes_do_usuario_exigem_login_e_orientam(cli):
    cli(*FILME)
    codigo, _, erro = cli("usuario", "criar-lista", "Favoritas")
    assert codigo == 1 and "usuario entrar" in erro
    assert cli("midia", "atualizar-status", 1, "assistido")[0] == 1


def test_listas_favoritos_e_sessao(cli):
    cli(*FILME)
    cli("usuario", "entrar", "ana", "--senha", "123")
    cli("usuario", "criar-lista", "Para ver depois")
    cli("usuario", "adicionar-na-lista", "para ver depois", 1)
    cli("usuario", "adicionar-favorito", 1)
    saida = cli("usuario", "listas")[1]
    assert "Para ver depois: 1" in saida and "Favoritos: 1" in saida
    assert "Matrix" in cli("usuario", "listas", "Favoritos")[1]
    assert "ana" in cli("usuario", "quem")[1]
    cli("usuario", "sair")
    assert cli("usuario", "listas")[0] == 1


def test_senha_incorreta_nao_cria_sessao(cli):
    cli("usuario", "entrar", "ana", "--senha", "123")
    cli("usuario", "sair")
    codigo, _, erro = cli("usuario", "entrar", "ana", "--senha", "errada")
    assert codigo == 1 and "Senha incorreta" in erro
    assert "Ninguém" in cli("usuario", "quem")[1]


def test_config_definir_persiste_e_valida(cli):
    assert cli("config", "definir", "limite_listas", 2)[0] == 0
    assert "limite_listas: 2" in cli("config", "mostrar")[1]
    assert cli("config", "definir", "limite_listas", -1)[0] == 1
    cli("usuario", "entrar", "ana", "--senha", "1")
    cli("usuario", "criar-lista", "A")
    cli("usuario", "criar-lista", "B")
    assert "Limite" in cli("usuario", "criar-lista", "C")[2]


def test_filtros_do_listar(cli):
    cli("usuario", "entrar", "ana", "--senha", "1")
    cli("exemplos")
    assert len(cli("midia", "listar", "--busca", "matr")[1].splitlines()) == 1
    assert len(cli("midia", "listar", "--status", "nao assistido")[1].splitlines()) == 1
    assert "Nenhuma mídia" in cli("midia", "listar", "--genero", "Terror")[1]


def test_ajuda_lista_os_grupos(capsys):
    with pytest.raises(SystemExit):
        executar(["-h"])
    saida = capsys.readouterr().out
    assert "midia" in saida and "serie" in saida and "usuario" in saida and "exemplos:" in saida
