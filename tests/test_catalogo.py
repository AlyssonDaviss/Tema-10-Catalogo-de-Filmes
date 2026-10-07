from src.config import Configurações
from src.lista import Lista
from src.midia import Filme
from src.relatorio import Relatório
from src.usuario import Usuário


def test_usuario_login_valido():
    usuario = Usuário("Alysson", "123456")
    assert usuario.Fazer_login("Alysson", "123456") is True
    assert usuario.Fazer_login("Alysson", "errada") is False


def test_lista_adiciona_e_remove_itens():
    lista = Lista("Favoritos", "filme", [])
    assert lista.Adicionar_na_lista("0001") == ["0001"]
    assert lista.Remover_na_lista("0001") == []


def test_configuracoes_exibe_valores():
    config = Configurações(4.5, 3)
    cfg = config.Mostrar_config()
    assert cfg["nota_min_recomendacao"] == 4.5
    assert cfg["limite_listas_personalizadas"] == 3


def test_relatorio_calcula_media_geral():
    relatorio = Relatório()
    assert relatorio.Gerar_media_geral_catalogo([4.5, 3.8, 4.0]) == 4.1


def test_filme_usa_duracao_e_status():
    filme = Filme("Filme 1", "filme", "Ação", 2024, "12", ["Ator A"], "assistido", 120)
    assert filme.Registrar_duração() == 120
    assert filme.Registrar_status("assistindo") == "assistindo"
