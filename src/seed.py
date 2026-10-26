"""Dados de exemplo: filmes e séries pré-cadastrados, com algumas avaliações."""

from datetime import datetime, timedelta

from src.midia import Filme, Serie, Status

A, E, N = Status.ASSISTIDO, Status.ASSISTINDO, Status.NAO_ASSISTIDO

# título, gênero, ano, classificação, elenco, duração, status, nota, dias atrás
FILMES = [
    ("Interestelar", "Ficção Científica", 2014, "10", "Matthew McConaughey, Anne Hathaway", 169, A, 9.5, 40),
    ("Matrix", "Ficção Científica", 1999, "14", "Keanu Reeves, Carrie-Anne Moss", 136, A, 9.0, 21),
    ("Parasita", "Suspense", 2019, "16", "Song Kang-ho, Choi Woo-shik", 132, A, 8.5, 9),
    ("Cidade de Deus", "Crime", 2002, "18", "Alexandre Rodrigues, Leandro Firmino", 130, A, 9.0, 3),
    ("Toy Story", "Animação", 1995, "L", "Tom Hanks, Tim Allen", 81, E, None, 0),
    ("O Poderoso Chefão", "Crime", 1972, "16", "Marlon Brando, Al Pacino", 175, N, None, 0),
]

# título, gênero, ano, classificação, elenco, episódios, duração, assistidos, notas, dias atrás
SERIES = [
    ("Breaking Bad", "Crime", 2008, "16", "Bryan Cranston, Aaron Paul", 7, 47, 7, (9.5, 9.0, 8.5), 14),
    ("Dark", "Ficção Científica", 2017, "16", "Louis Hofmann, Lisa Vicari", 10, 50, 4, (9.0, 8.5), 5),
]


def popular(repositorio, usuario, agora=None):
    """Cadastra os exemplos que ainda não existem e devolve quantos entraram.

    O chamador grava o usuário depois (listas e histórico ficam nele).
    """
    agora = agora or datetime.now()
    novas = 0

    for titulo, genero, ano, classif, elenco, duracao, status, nota, dias in FILMES:
        filme = Filme(titulo, genero, ano, classif, elenco, duracao)
        try:
            repositorio.cadastrar(filme)
        except ValueError:
            continue  # já cadastrado
        quando = agora - timedelta(days=dias)
        for descricao, minutos in filme.definir_status(status):
            usuario.registrar_conclusao(filme.id, descricao, minutos, quando)
        filme.nota = nota
        repositorio.salvar_midia(filme)
        novas += 1

    for titulo, genero, ano, classif, elenco, qtd, duracao, vistos, notas, dias in SERIES:
        serie = Serie(titulo, genero, ano, classif, elenco)
        try:
            repositorio.cadastrar(serie)
        except ValueError:
            continue
        serie.criar_temporada(1, qtd, duracao)
        quando = agora - timedelta(days=dias)
        for numero in range(1, vistos + 1):
            for descricao, minutos in serie.definir_status(A, 1, numero):
                usuario.registrar_conclusao(serie.id, descricao, minutos, quando)
        for numero, nota in enumerate(notas, start=1):
            serie.avaliar(nota, 1, numero)
        repositorio.salvar_midia(serie)
        novas += 1

    por_titulo = {m.titulo: m for m in repositorio.listar()}
    _preencher_lista(usuario, "Para assistir", ("O Poderoso Chefão", "Toy Story"), por_titulo)
    _preencher_lista(usuario, "Favoritos", ("Interestelar", "Breaking Bad"), por_titulo)
    return novas


def _preencher_lista(usuario, nome, titulos, por_titulo):
    try:
        lista = usuario.lista(nome)
    except ValueError:
        lista = usuario.criar_lista(nome)
    for titulo in titulos:
        midia = por_titulo.get(titulo)
        if midia is not None and midia.id not in lista:
            lista.adicionar(midia.id)
