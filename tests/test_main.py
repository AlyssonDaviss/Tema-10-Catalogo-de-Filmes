"""Testes do terminal interativo de comandos."""

from main import _terminal_comandos


def test_terminal_aspas_sem_fechar_nao_encerra(monkeypatch, tmp_path, capsys):
    entradas = iter(['midia listar --busca "Matrix', 'config mostrar', 'sair'])
    monkeypatch.setattr('builtins.input', lambda _='': next(entradas))

    assert _terminal_comandos(tmp_path) == 0
    saida = capsys.readouterr().out
    assert 'Erro ao interpretar o comando' in saida
    assert 'nota_minima_recomendado' in saida


def test_terminal_continua_apos_comando_invalido(monkeypatch, tmp_path, capsys):
    entradas = iter(['comando inexistente', 'usuario quem', 'sair'])
    monkeypatch.setattr('builtins.input', lambda _='': next(entradas))

    assert _terminal_comandos(tmp_path) == 0
    assert 'Ninguém conectado.' in capsys.readouterr().out
