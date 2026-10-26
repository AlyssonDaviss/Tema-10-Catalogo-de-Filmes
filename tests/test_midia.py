import pytest

from src.midia import Episodio, Filme, Midia, Serie, Status


def filme(titulo="Matrix", ano=1999, **extra):
    return Filme(titulo, "Ficção", ano, "14", "Keanu Reeves, Carrie-Anne Moss", 136, **extra)


def serie(episodios=3, titulo="Dark"):
    s = Serie(titulo, "Ficção", 2017, "16")
    s.criar_temporada(1, episodios, 50)
    return s


# -- validações ---------------------------------------------------------------
def test_filme_valido_normaliza_dados():
    f = filme()
    assert f.tipo == "FILME"
    assert f.elenco == ["Keanu Reeves", "Carrie-Anne Moss"]
    assert f.status is Status.NAO_ASSISTIDO
    assert f.nota is None


@pytest.mark.parametrize(
    "campo, valor",
    [("titulo", "  "), ("genero", ""), ("ano", -5), ("ano", "abc"),
     ("duracao", 0), ("duracao", "x"), ("nota", 10.5), ("nota", -1), ("nota", "ótimo"),
     ("status", "quase")],
)
def test_filme_rejeita_valores_invalidos(campo, valor):
    f = filme()
    with pytest.raises(ValueError):
        setattr(f, campo, valor)


def test_episodio_exige_numeros_positivos():
    with pytest.raises(ValueError):
        Episodio(0, 1, "Piloto", 40)
    with pytest.raises(ValueError):
        Episodio(1, -2, "Piloto", 40)
    with pytest.raises(ValueError):
        Episodio(1, 1, "", 40)


def test_status_aceita_variacoes_de_escrita():
    assert Status.converter("nao-assistido") is Status.NAO_ASSISTIDO
    assert Status.converter(" Assistindo ") is Status.ASSISTINDO


# -- métodos especiais --------------------------------------------------------
def test_eq_compara_titulo_e_tipo_sem_diferenciar_maiusculas():
    assert filme("MATRIX") == filme("matrix", ano=2003)
    assert filme("Dark") != serie(titulo="Dark")


def test_lt_ordena_por_nota_media():
    a, b, c = filme("A"), filme("B"), filme("C")
    a.nota, b.nota = 9, 7
    assert sorted([b, c, a]) == [c, b, a]  # sem nota < 7 < 9
    assert b < a


def test_len_conta_episodios_de_todas_as_temporadas():
    s = serie(episodios=3)
    s.criar_temporada(2, 5, 50)
    assert len(s) == 8


def test_str_e_repr():
    f = filme()
    assert "Matrix (1999) [FILME]" in str(f)
    assert repr(f).startswith("Filme(")


# -- séries, temporadas e episódios -------------------------------------------
def test_criar_temporada_gera_episodios_genericos():
    s = serie(episodios=4)
    assert [e.titulo for e in s.temporada(1)] == [f"Episódio {n}" for n in range(1, 5)]
    assert s.duracao_total == 200


def test_criar_temporada_invalida_nao_deixa_lixo():
    s = Serie("X", "Y", 2000, "L")
    with pytest.raises(ValueError):
        s.criar_temporada(1, 3, 0)
    assert s.temporadas == []


def test_episodio_duplicado_e_rejeitado():
    s = serie(episodios=2)
    with pytest.raises(ValueError, match="já existe"):
        s.adicionar_episodio(Episodio(1, 1, "Outro", 30))


def test_serie_vira_assistida_quando_todos_os_episodios_forem():
    s = serie(episodios=2)
    assert s.status is Status.NAO_ASSISTIDO
    s.definir_status("ASSISTIDO", 1, 1)
    assert s.status is Status.ASSISTINDO
    s.definir_status("ASSISTIDO", 1, 2)
    assert s.status is Status.ASSISTIDO
    s.definir_status("NÃO ASSISTIDO", 1, 2)
    assert s.status is Status.ASSISTINDO


def test_nota_media_da_serie_vem_dos_episodios_avaliados():
    s = serie(episodios=2)
    assert s.nota_media is None
    s.avaliar(9, 1, 1)
    s.avaliar("8,0", 1, 2)
    assert s.nota_media == pytest.approx(8.5)


def test_definir_status_so_devolve_o_que_acabou_de_ser_concluido():
    s = serie(episodios=3)
    assert len(s.definir_status("ASSISTIDO", 1, 1)) == 1
    assert len(s.definir_status("ASSISTIDO")) == 2  # o episódio 1 não conta de novo
    assert s.minutos_assistidos == 150


def test_filme_nao_aceita_temporada_e_serie_avalia_escopos():
    with pytest.raises(ValueError):
        filme().avaliar(8, temporada=1)
    s = serie(episodios=2)
    s.avaliar(8)
    assert [ep.nota for ep in s.episodios] == [8, 8]


def test_temporada_ou_episodio_inexistente():
    s = serie(episodios=2)
    with pytest.raises(ValueError):
        s.definir_status("ASSISTIDO", 9)
    with pytest.raises(ValueError):
        s.definir_status("ASSISTIDO", 1, 99)


# -- serialização ---------------------------------------------------------------
def test_dict_ida_e_volta_preserva_filme_e_serie():
    f = filme(status="ASSISTIDO", nota=9)
    s = serie(episodios=2)
    s.definir_status("ASSISTIDO", 1, 1)
    s.avaliar(7.5, 1, 1)
    for original in (f, s):
        copia = Midia.de_dict(original.para_dict())
        assert type(copia) is type(original)
        assert copia.para_dict() == original.para_dict()
