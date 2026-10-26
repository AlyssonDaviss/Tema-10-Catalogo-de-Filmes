from datetime import datetime

import pytest

from repositories.cadastrar_midia import CadastrarMidia
from src import relatorio
from src.midia import Filme, Serie
from src.seed import popular
from src.user import Usuario


def filme(titulo, genero, duracao, status="ASSISTIDO", nota=None):
    return Filme(titulo, genero, 2000, "L", "", duracao, status, nota)


def test_media_por_genero_considera_apenas_finalizadas():
    midias = [
        filme("A", "Drama", 100, nota=10),
        filme("B", "Drama", 100, nota=8),
        filme("C", "Drama", 100, status="ASSISTINDO", nota=1),  # ignorada
        filme("D", "Ação", 100, nota=7),
        filme("E", "Ação", 100),                                # sem nota
    ]
    assert relatorio.media_por(midias, "genero") == {"Ação": 7, "Drama": 9}


def test_media_por_tipo():
    serie = Serie("S", "Drama", 2000, "L")
    serie.criar_temporada(1, 1, 30)
    serie.definir_status("ASSISTIDO")
    serie.avaliar(6, 1, 1)
    assert relatorio.media_por([filme("A", "Drama", 100, nota=10), serie], "tipo") == {
        "FILME": 10, "SERIE": 6}


def test_tempo_total_soma_apenas_o_que_foi_assistido():
    serie = Serie("S", "Drama", 2000, "L")
    serie.criar_temporada(1, 4, 30)
    serie.definir_status("ASSISTIDO", 1, 1)
    serie.definir_status("ASSISTIDO", 1, 2)
    midias = [filme("A", "Drama", 100), filme("B", "Drama", 50, status="NÃO ASSISTIDO"), serie]
    assert relatorio.minutos_por_tipo(midias) == {"FILME": 100, "SERIE": 60}


def test_top_ordena_por_nota_limita_e_desempata_pelo_titulo():
    midias = [filme(t, "X", 90, nota=n) for t, n in
              (("Zeta", 9), ("Alfa", 9), ("Beta", 10), ("Gama", 5))]
    midias.append(filme("Sem nota", "X", 90))
    midias.append(filme("Nao vista", "X", 90, status="NÃO ASSISTIDO", nota=10))
    assert [m.titulo for m in relatorio.top(midias, 3)] == ["Beta", "Alfa", "Zeta"]


def test_series_com_mais_episodios_assistidos():
    a, b, c = (Serie(n, "X", 2000, "L") for n in "ABC")
    for s, vistos in ((a, 1), (b, 3), (c, 0)):
        s.criar_temporada(1, 3, 20)
        for n in range(1, vistos + 1):
            s.definir_status("ASSISTIDO", 1, n)
    ranking = relatorio.series_mais_assistidas([a, b, c])
    assert [(s.titulo, n) for s, n in ranking] == [("B", 3), ("A", 1)]


def test_tempo_por_semana_e_por_mes():
    usuario = Usuario("ana", "1")
    usuario.registrar_conclusao(1, "A", 100, datetime(2026, 10, 5))
    usuario.registrar_conclusao(1, "B", 50, datetime(2026, 10, 9))
    usuario.registrar_conclusao(1, "C", 30, datetime(2026, 10, 12))
    usuario.registrar_conclusao(1, "D", 20, datetime(2026, 11, 2))
    assert relatorio.minutos_por_periodo(usuario, "semana") == {
        "2026-S41": 150, "2026-S42": 30, "2026-S45": 20}
    assert relatorio.minutos_por_periodo(usuario, "mes") == {"2026-10": 180, "2026-11": 20}
    with pytest.raises(ValueError):
        relatorio.minutos_por_periodo(usuario, "ano")


def test_nota_geral_do_catalogo():
    midias = [filme("A", "X", 90, nota=10), filme("B", "X", 90, nota=6), filme("C", "X", 90)]
    assert relatorio.nota_geral(midias) == 8
    assert relatorio.nota_geral([]) is None


def test_relatorios_com_dados_do_seed(tmp_path):
    repositorio, usuario = CadastrarMidia(tmp_path), Usuario("ana", "1")
    assert popular(repositorio, usuario, agora=datetime(2026, 10, 25)) == 3
    midias = repositorio.listar()
    assert len(midias) == 3
    assert all(m.nota_media is None for m in midias)
    assert usuario.historico == []
    assert popular(repositorio, usuario) == 0  # idempotente
