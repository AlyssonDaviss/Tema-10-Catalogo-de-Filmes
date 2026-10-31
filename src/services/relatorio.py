"""Relatórios: funções puras sobre listas de mídias e sobre o histórico.

Regra de negócio: relatórios consideram apenas mídias finalizadas (ASSISTIDO),
exceto os que contam episódios ou tempo, que somam o que de fato foi assistido.
"""

from src.domain.midia import Serie, media


def finalizadas(midias):
    return [m for m in midias if m.finalizada]


def nota_geral(midias):
    """Média das notas médias de todas as mídias que têm alguma nota."""
    return media(m.nota_media for m in midias if m.nota_media is not None)


def media_por(midias, atributo="genero"):
    """Nota média por 'genero' ou 'tipo' (mídias finalizadas e avaliadas)."""
    grupos = {}
    for m in finalizadas(midias):
        if m.nota_media is not None:
            grupos.setdefault(getattr(m, atributo), []).append(m.nota_media)
    return {chave: media(notas) for chave, notas in sorted(grupos.items())}


def minutos_por_tipo(midias):
    """Total de minutos assistidos por tipo (filme/série)."""
    totais = {"FILME": 0.0, "SERIE": 0.0}
    for m in midias:
        totais[m.tipo] += m.minutos_assistidos
    return totais


def top(midias, quantidade=10):
    """As mídias finalizadas mais bem avaliadas (usa Midia.__lt__)."""
    avaliadas = [m for m in finalizadas(midias) if m.nota_media is not None]
    avaliadas.sort(key=lambda m: m.titulo.casefold())  # desempate estável
    return sorted(avaliadas, reverse=True)[:quantidade]


def series_mais_assistidas(midias):
    """[(série, episódios assistidos)] da que tem mais para a que tem menos."""
    series = [(m, m.episodios_assistidos) for m in midias if isinstance(m, Serie)]
    series = [(s, n) for s, n in series if n > 0]
    return sorted(series, key=lambda par: (-par[1], par[0].titulo.casefold()))


def minutos_por_periodo(usuario, por="mes"):
    """Minutos assistidos pelo usuário agrupados por 'semana' ou 'mes'."""
    if por not in ("semana", "mes"):
        raise ValueError("O período deve ser 'semana' ou 'mes'.")
    totais = {}
    for registro in usuario.historico:
        if por == "mes":
            chave = registro.concluido_em.strftime("%Y-%m")
        else:
            ano, semana, _ = registro.concluido_em.isocalendar()
            chave = f"{ano}-S{semana:02d}"
        totais[chave] = totais.get(chave, 0.0) + registro.minutos
    return dict(sorted(totais.items()))
