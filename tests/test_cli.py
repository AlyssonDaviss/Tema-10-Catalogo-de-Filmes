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






def test_ajuda_em_tres_niveis(cli):
    codigo, saida, _ = cli("ajuda")
    assert codigo == 0 and "adicionar-temporada" in saida and "exemplos" in saida
    assert "midia avaliar <id> <nota>" in cli("ajuda", "midia")[1]
    assert "--duracao" in cli("ajuda", "midia", "adicionar")[1]
    codigo, _, erro = cli("ajuda", "foo")
    assert codigo == 1 and "Não existe" in erro


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










def test_voltar_para_nao_assistido_limpa_historico_e_periodo(cli):
    cli("usuario", "entrar", "ana", "--senha", "1")
    cli(*FILME)
    cli("midia", "atualizar-status", 1, "assistido")
    assert "Matrix" in cli("usuario", "historico")[1]
    cli("midia", "atualizar-status", 1, "nao assistido")
    assert "Histórico vazio" in cli("usuario", "historico")[1]
    assert "Nenhuma conclusão" in cli("midia", "relatorio", "periodo", "--por", "mes")[2] or \
           "Nenhuma conclusão" in cli("midia", "relatorio", "periodo", "--por", "mes")[1]


def test_editar_midia_rejeita_duplicidade(tmp_path):
    from src.services.comandos import Comandos

    cmd = Comandos(tmp_path)
    a = cmd.adicionar_midia("filme", "Matrix", "Ficção", 1999, "14", "Elenco", 136)
    cmd.adicionar_midia("filme", "Outro", "Drama", 2000, "12", "Elenco", 100)
    with pytest.raises(ValueError, match="Já existe"):
        cmd.editar_midia(2, titulo=a.titulo, genero="Ficção", ano=1999,
                         classificacao="14", elenco="Elenco", duracao=136)
