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






# -- métodos especiais --------------------------------------------------------








# -- séries, temporadas e episódios -------------------------------------------






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
