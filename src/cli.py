"""CLI com subcomandos:  python main.py <grupo> <ação> [argumentos]

Sem argumentos, o main abre o menu interativo (src/menu.py).
"""

import argparse
import sys

from src.services.comandos import RELATORIOS, Comandos, ler_senha, linha, mostrar, mostrar_mensagem

# Fonte única dos exemplos: usada no "-h" e na tela inicial do terminal de comandos.
EXEMPLOS = (
    "usuario entrar Davi",
    'midia adicionar --tipo filme --titulo Matrix --genero "Ficção" --ano 1999 --classificacao 14 --duracao 136',
    "midia listar --status assistido",
    "midia avaliar 1 9.5",
    "serie adicionar-temporada 2 --episodios 10 --duracao 50",
    "midia relatorio top",
)


# -- argumentos reaproveitados -------------------------------------------------
ID = (("id",), {"type": int, "help": "ID da mídia (veja em: midia listar)"})
STATUS = (("status",), {"help": "NÃO ASSISTIDO, ASSISTINDO ou ASSISTIDO"})
TEMPORADA = (("-t", "--temporada"), {"type": int, "help": "número da temporada"})
EPISODIO = (("-e", "--episodio"), {"type": int, "help": "número do episódio"})
LANCAMENTO = (("--lancamento",), {"help": "data de lançamento (AAAA-MM-DD)"})
DURACAO = (("--duracao",), {"required": True, "help": "duração em minutos"})
NOME_LISTA = (("nome",), {"help": "nome da lista"})


# -- midia ---------------------------------------------------------------------
def midia_adicionar(cmd, a):
    midia = cmd.adicionar_midia(a.tipo, a.titulo, a.genero, a.ano, a.classificacao,
                                a.elenco, a.duracao)
    mostrar_mensagem(f"Cadastrado: {linha(midia)}")
    if a.tipo.startswith("s"):
        mostrar_mensagem(f"Dica: adicione episódios com: serie adicionar-temporada {midia.id} -t 1 --episodios N --duracao MIN")


def midia_avaliar(cmd, a):
    mostrar_mensagem(f"Avaliação registrada: {linha(cmd.avaliar(a.id, a.nota, a.temporada, a.episodio))}")


def atualizar_status(cmd, a):
    mostrar_mensagem(f"Status atualizado: {linha(cmd.atualizar_status(a.id, a.status, a.temporada, a.episodio))}")


def midia_listar(cmd, a):
    midias = cmd.listar(a.tipo, a.status, a.genero, a.busca)
    mostrar([linha(m) for m in midias] or ["Nenhuma mídia encontrada."])


def midia_remover(cmd, a):
    mostrar_mensagem(f"Removido: {cmd.remover(a.id).titulo}")


def midia_recomendar(cmd, a):
    minimo = cmd.config.nota_minima_recomendado
    midias = cmd.recomendar()
    mostrar_mensagem(f"Sugestões (nota média a partir de {minimo:g}):")
    mostrar([linha(m) for m in midias] or ["Nenhuma mídia com essa nota ainda."])


def midia_relatorio(cmd, a):
    mostrar(cmd.relatorio(a.qual, a.por, a.n))


# -- serie ---------------------------------------------------------------------
def serie_adicionar_episodio(cmd, a):
    serie = cmd.adicionar_episodio(a.id, a.temporada, a.numero, a.titulo, a.duracao, a.lancamento)
    mostrar_mensagem(f"Episódio adicionado. {serie.titulo} agora tem {len(serie)} episódio(s).")


def serie_adicionar_temporada(cmd, a):
    serie, numero = cmd.adicionar_temporada(a.id, a.episodios, a.duracao, a.lancamento, a.temporada)
    mostrar_mensagem(f"Temporada {numero} criada em {serie.titulo} com {a.episodios} episódios.")


def serie_episodios(cmd, a):
    mostrar(cmd.episodios(a.id))


# -- usuario -------------------------------------------------------------------
def usuario_entrar(cmd, a):
    senha = a.senha or ler_senha()
    novo = cmd.entrar(a.nome, senha)
    mostrar_mensagem(f"Conta criada. Você está conectado como {cmd.usuario.login}." if novo
                     else f"Você entrou como {cmd.usuario.login}.")


def usuario_sair(cmd, a):
    cmd.sair()
    mostrar_mensagem("Você saiu da conta.")


def usuario_quem(cmd, a):
    mostrar_mensagem(f"Conectado como {cmd.usuario.login}." if cmd.usuario else "Ninguém conectado.")


def usuario_criar_lista(cmd, a):
    mostrar_mensagem(f"Lista criada: {cmd.criar_lista(a.nome).nome}")


def usuario_adicionar_favorito(cmd, a):
    cmd.adicionar_favorito(a.id)
    mostrar_mensagem("Adicionada aos favoritos.")


def usuario_adicionar_na_lista(cmd, a):
    mostrar_mensagem(f"Adicionada à lista '{cmd.adicionar_na_lista(a.nome, a.id).nome}'.")


def usuario_remover_da_lista(cmd, a):
    mostrar_mensagem(f"Removida da lista '{cmd.remover_da_lista(a.nome, a.id).nome}'.")


def usuario_apagar_lista(cmd, a):
    cmd.apagar_lista(a.nome)
    mostrar_mensagem("Lista apagada.")


def usuario_listas(cmd, a):
    mostrar(cmd.listas(a.nome))


def usuario_historico(cmd, a):
    mostrar(cmd.relatorio("historico"))


# -- config, exemplos, menu ----------------------------------------------------
def config_mostrar(cmd, a):
    mostrar(cmd.config_linhas())


def config_definir(cmd, a):
    cmd.definir_config(a.chave, a.valor)
    mostrar_mensagem(f"{a.chave} atualizado.")


def exemplos(cmd, a):
    mostrar_mensagem(f"{cmd.carregar_exemplos()} mídia(s) de exemplo cadastrada(s).")


def abrir_menu(cmd, a):
    from src.menu import Menu

    Menu(cmd).iniciar()


# -- ajuda ---------------------------------------------------------------------
def _subcomandos(parser):
    """{nome: parser} dos subcomandos de um parser (vazio se for um comando final)."""
    for acao in parser._actions:
        if isinstance(acao, argparse._SubParsersAction):
            return acao.choices
    return {}


def nomes_grupos(parser=None):
    """Nomes dos grupos que têm ações (midia, serie, usuario, config)."""
    raiz = _subcomandos(parser or criar_parser())
    return [nome for nome, sub in raiz.items() if _subcomandos(sub)]


def _assinatura(parser):
    """Resumo dos argumentos: <obrigatório posicional> --obrigatório X [--opcional X]."""
    partes = []
    for a in parser._actions:
        if isinstance(a, (argparse._HelpAction, argparse._SubParsersAction)):
            continue
        valor = "|".join(map(str, a.choices)) if a.choices else (a.metavar or a.dest).upper()
        if a.option_strings:
            texto = f"{max(a.option_strings, key=len)} {valor}"
            partes.append(texto if a.required else f"[{texto}]")
        else:
            nome = valor.lower()
            partes.append(f"[{nome}]" if a.nargs in ("?", "*") else f"<{nome}>")
    return " ".join(partes)


def _ajuda_geral(raiz):
    linhas = ["COMANDOS   (detalhes: ajuda <grupo>  |  ajuda <grupo> <ação>)"]
    avulsos = []
    for nome, sub in raiz.items():
        filhos = _subcomandos(sub)
        if not filhos:
            avulsos.append((nome, sub.description))
            continue
        linhas += ["", f"{nome} - {sub.description}"]
        largura = max(map(len, filhos))
        linhas += [f"  {acao:<{largura}}  {filho.description}" for acao, filho in filhos.items()]
    largura = max(len(nome) for nome, _ in avulsos)
    linhas += ["", "outros"] + [f"  {nome:<{largura}}  {desc}" for nome, desc in avulsos]
    return "\n".join(linhas)


def _ajuda_grupo(nome, sub, filhos):
    linhas = [f"{nome.upper()} - {sub.description}", ""]
    for acao, filho in filhos.items():
        linhas += [f"  {nome} {acao} {_assinatura(filho)}".rstrip(), f"      {filho.description}"]
    linhas += ["", f"detalhes de um comando: ajuda {nome} <ação>"]
    return "\n".join(linhas)


def texto_ajuda(parser, alvo=()):
    """Guia em três níveis: tudo, um grupo ou um comando."""
    raiz = _subcomandos(parser)
    if not alvo:
        return _ajuda_geral(raiz)
    nome, *resto = (palavra.casefold() for palavra in alvo)
    if nome not in raiz:
        raise ValueError(f"Não existe '{nome}'. Veja a lista completa com: ajuda")
    filhos = _subcomandos(raiz[nome])
    if not filhos:
        return raiz[nome].format_help().strip()
    if not resto:
        return _ajuda_grupo(nome, raiz[nome], filhos)
    if len(resto) > 1 or resto[0] not in filhos:
        raise ValueError(f"Não existe '{' '.join(resto)}' em {nome}. Veja: ajuda {nome}")
    return filhos[resto[0]].format_help().strip()


def ajuda(cmd, a):
    mostrar_mensagem(texto_ajuda(criar_parser(), a.alvo))


# -- montagem do parser --------------------------------------------------------
def _grupo(raiz, nome, ajuda):
    return raiz.add_parser(nome, help=ajuda, description=ajuda).add_subparsers(
        dest=f"acao_{nome}", metavar="ação", required=True)


def _acao(grupo, nome, funcao, ajuda, *argumentos):
    parser = grupo.add_parser(nome, help=ajuda, description=ajuda)
    for nomes, opcoes in argumentos:
        parser.add_argument(*nomes, **opcoes)
    parser.set_defaults(funcao=funcao)


def criar_parser():
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="Catálogo pessoal de filmes e séries.",
        epilog="exemplos:\n" + "\n".join(f"  python main.py {e}" for e in EXEMPLOS)
               + "\n\nguia completo: python main.py ajuda",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    raiz = parser.add_subparsers(dest="grupo", metavar="comando", required=True)

    midia = _grupo(raiz, "midia", "filmes e séries: cadastrar, avaliar, listar, relatórios")
    _acao(midia, "adicionar", midia_adicionar, "cadastra um filme ou uma série",
          (("--tipo",), {"required": True, "choices": ["filme", "serie"]}),
          (("--titulo",), {"required": True}),
          (("--genero",), {"required": True}),
          (("--ano",), {"required": True}),
          (("--classificacao",), {"required": True, "help": "L, 10, 12, 14, 16 ou 18"}),
          (("--elenco",), {"default": "", "help": 'nomes separados por vírgula: "Ana, Bruno"'}),
          (("--duracao",), {"help": "minutos (só para filmes)"}))
    _acao(midia, "listar", midia_listar, "lista o catálogo, com filtros opcionais",
          (("--tipo",), {"choices": ["filme", "serie"]}),
          (("--status",), {"help": "NÃO ASSISTIDO, ASSISTINDO ou ASSISTIDO"}),
          (("--genero",), {}), (("--busca",), {"help": "parte do título"}))
    _acao(midia, "avaliar", midia_avaliar, "dá uma nota de 0 a 10 a um filme ou episódio",
          ID, (("nota",), {"help": "de 0 a 10"}), TEMPORADA, EPISODIO)
    _acao(midia, "atualizar-status", atualizar_status, "muda o status de um filme ou série",
          ID, STATUS, TEMPORADA, EPISODIO)
    _acao(midia, "recomendar", midia_recomendar, "sorteia mídias com nota acima do mínimo")
    _acao(midia, "remover", midia_remover, "remove uma mídia do catálogo", ID)
    _acao(midia, "relatorio", midia_relatorio, "relatórios do catálogo",
          (("qual",), {"choices": RELATORIOS,
                       "help": "geral, notas, tempo, top, series, periodo ou historico"}),
          (("--por",), {"help": "notas: genero|tipo   periodo: semana|mes"}),
          (("-n",), {"type": int, "default": 10, "help": "tamanho do top (padrão 10)"}))

    serie = _grupo(raiz, "serie", "temporadas e episódios de uma série")
    _acao(serie, "adicionar-temporada", serie_adicionar_temporada,
          "cria uma temporada já com N episódios (o mais rápido para começar)",
          ID, (("--episodios",), {"type": int, "required": True, "help": "quantidade de episódios"}),
          DURACAO, LANCAMENTO,
          (("-t", "--temporada"), {"type": int, "help": "número (padrão: a próxima)"}))
    _acao(serie, "adicionar-episodio", serie_adicionar_episodio, "adiciona um episódio avulso",
          ID, (("-t", "--temporada"), {"type": int, "required": True}),
          (("-n", "--numero"), {"type": int, "required": True, "help": "número do episódio"}),
          (("--titulo",), {"required": True}), DURACAO, LANCAMENTO)
    _acao(serie, "atualizar-status", atualizar_status,
          "muda o status da série toda, de uma temporada (-t) ou de um episódio (-t -e)",
          ID, STATUS, TEMPORADA, EPISODIO)
    _acao(serie, "episodios", serie_episodios, "mostra temporadas e episódios", ID)

    usuario = _grupo(raiz, "usuario", "conta, listas, favoritos e histórico")
    _acao(usuario, "entrar", usuario_entrar, "entra na conta (cria se for nova)",
          (("nome",), {}), (("--senha",), {"help": "se omitida, será pedida"}))
    _acao(usuario, "sair", usuario_sair, "sai da conta")
    _acao(usuario, "quem", usuario_quem, "mostra quem está conectado")
    _acao(usuario, "criar-lista", usuario_criar_lista, "cria uma lista personalizada", NOME_LISTA)
    _acao(usuario, "adicionar-favorito", usuario_adicionar_favorito, "adiciona aos favoritos", ID)
    _acao(usuario, "adicionar-na-lista", usuario_adicionar_na_lista, "adiciona uma mídia a uma lista",
          NOME_LISTA, ID)
    _acao(usuario, "remover-da-lista", usuario_remover_da_lista, "remove uma mídia de uma lista",
          NOME_LISTA, ID)
    _acao(usuario, "apagar-lista", usuario_apagar_lista, "apaga uma lista", NOME_LISTA)
    _acao(usuario, "listas", usuario_listas, "mostra suas listas (ou o conteúdo de uma)",
          (("nome",), {"nargs": "?", "help": "lista a detalhar"}))
    _acao(usuario, "historico", usuario_historico, "mostra o histórico de visualização")

    config = _grupo(raiz, "config", "configurações (settings.json)")
    _acao(config, "mostrar", config_mostrar, "mostra as configurações")
    _acao(config, "definir", config_definir, "altera uma configuração",
          (("chave",), {}), (("valor",), {}))

    _acao(raiz, "exemplos", exemplos, "cadastra filmes e séries de exemplo")
    _acao(raiz, "menu", abrir_menu, "abre o menu interativo")
    _acao(raiz, "ajuda", ajuda, "guia dos comandos: ajuda | ajuda <grupo> | ajuda <grupo> <ação>",
          (("alvo",), {"nargs": "*", "help": "grupo e, se quiser, a ação"}))
    return parser


def executar(argv, pasta=None):
    args = criar_parser().parse_args(argv)
    try:
        args.funcao(Comandos(pasta), args)
    except ValueError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1
    return 0
