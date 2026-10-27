import json

import pytest

from repositories.cadastrar_config import CadastrarConfiguracoes
from repositories.cadastrar_midia import CadastrarMidia
from repositories.cadastrar_pessoa import CadastrarUsuario
from src.config import Configuracoes
from src.midia import Filme, Serie, Status
from src.user import Usuario


def filme(titulo="Matrix", ano=1999):
    return Filme(titulo, "Ficção", ano, "14", "", 100)


@pytest.fixture
def midias(tmp_path):
    return CadastrarMidia(tmp_path)


@pytest.fixture
def pessoas(tmp_path):
    return CadastrarUsuario(tmp_path)


# -- mídias: cadastro e duplicidade -------------------------------------------


def test_duplicidade_titulo_tipo_ano_e_rejeitada(midias):
    midias.cadastrar(filme("Dune", 1984))
    with pytest.raises(ValueError, match="Já existe"):
        midias.cadastrar(filme("DUNE", 1984))












# -- usuários, listas e histórico -------------------------------------------------




def test_listas_e_historico_persistem_por_usuario(pessoas):
    ana, bia = Usuario("ana", "1"), Usuario("bia", "2")
    pessoas.cadastrar(ana)
    pessoas.cadastrar(bia)
    ana.criar_lista("Para assistir").adicionar(3)
    ana.adicionar_favorito(3)
    ana.registrar_conclusao(3, "Matrix", 136)
    pessoas.salvar_usuario(ana)

    ana2 = pessoas.carregar_usuario(ana.id)
    assert ana2.lista("para assistir").midias == [3]
    assert ana2.lista("Favoritos").midias == [3]
    assert ana2.historico[0].descricao == "Matrix"
    assert pessoas.carregar_usuario(bia.id).listas == []


def test_listas_respeitam_limite_e_nomes_unicos():
    usuario = Usuario("ana", "1")
    usuario.criar_lista("Para assistir", limite=2)
    with pytest.raises(ValueError, match="Já existe"):
        usuario.criar_lista("para ASSISTIR", limite=2)
    usuario.criar_lista("Melhores de 2025", limite=2)
    with pytest.raises(ValueError, match="Limite"):
        usuario.criar_lista("Terceira", limite=2)




def test_remover_midia_limpa_todas_as_listas():
    usuario = Usuario("ana", "1")
    usuario.adicionar_favorito(5)
    usuario.criar_lista("Outra").adicionar(5)
    usuario.remover_midia_de_todas(5)
    assert [len(l) for l in usuario.listas] == [0, 0]


# -- configurações ---------------------------------------------------------------
def test_configuracoes_validam_e_convertem_horas():
    config = Configuracoes()
    assert config.horas(90) == 1.5
    assert Configuracoes(multiplicador_duracao=0.0166).horas(600, 1) == 10.0
    with pytest.raises(ValueError):
        config.definir("nota_minima_recomendado", 11)
    with pytest.raises(ValueError):
        config.definir("inexistente", 1)


