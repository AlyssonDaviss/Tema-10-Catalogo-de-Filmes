"""Cadastro mínimo de dados de demonstração, sem avaliações ou histórico."""

from src.midia import Filme, Serie


def popular(repositorio, usuario=None, agora=None):
    """Cadastra dois filmes e uma série com uma temporada, se ainda não existirem."""
    exemplos = [
        Filme("Matrix", "Ficção Científica", 1999, "14", "Keanu Reeves", 136),
        Filme("Interestelar", "Ficção Científica", 2014, "10", "Matthew McConaughey", 169),
        Serie("Dark", "Suspense", 2017, "16", "Louis Hofmann"),
    ]
    novas = 0
    for midia in exemplos:
        try:
            repositorio.cadastrar(midia)
        except ValueError:
            continue
        if isinstance(midia, Serie):
            midia.criar_temporada(1, 1, 50)
            repositorio.salvar_midia(midia)
        novas += 1
    return novas
