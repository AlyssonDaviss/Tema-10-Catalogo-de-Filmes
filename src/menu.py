"""Menu interativo: perguntas passo a passo sobre a mesma lógica dos subcomandos."""

from src.services.comandos import Comandos, ler_senha, linha, mostrar, mostrar_mensagem
from src.domain.midia import Serie, Status


# -- entrada de dados ----------------------------------------------------------
def _ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Preencha este campo.")


def _ler_numero(mensagem, tipo=float, minimo=None, maximo=None):
    while True:
        try:
            valor = tipo(input(mensagem).strip().replace(",", "."))
        except ValueError:
            print("Digite um número.")
            continue
        if minimo is not None and valor < minimo:
            print(f"O valor mínimo é {minimo:g}.")
        elif maximo is not None and valor > maximo:
            print(f"O valor máximo é {maximo:g}.")
        else:
            return valor


def _confirmar(mensagem):
    return input(f"{mensagem} (s/n): ").strip().casefold() in ("s", "sim")


def _data_opcional():
    return None


def _escolher(titulo, opcoes, saida="Voltar"):
    """Mostra [(valor, rótulo)] numerados; devolve o valor (None = voltar)."""
    if not opcoes:
        print("Nada para escolher aqui ainda.")
        return None
    # Deixa o início de cada tela fácil de localizar.
    print(f"\n=== {titulo} ===")
    for numero, (_, rotulo) in enumerate(opcoes, start=1):
        print(f"  {numero}. {rotulo}")
    print(f"  0. {saida}\n")
    while True:
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            return None
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            return opcoes[int(escolha) - 1][0]
        print("Opção inválida, digite um dos números acima.")


def _menu(titulo, acoes, saida="Voltar"):
    """Repete um menu de [(rótulo, função)] até o usuário voltar; erros de regra não o fecham."""
    while True:
        acao = _escolher(titulo, [(funcao, rotulo) for rotulo, funcao in acoes], saida)
        if acao is None:
            return
        try:
            acao()
        except ValueError as erro:
            mostrar_mensagem(f"Não foi possível: {erro}")


class Menu:
    """Interface guiada por opções numéricas."""
    def __init__(self, cmd):
        self.cmd = cmd

    # -- início ---------------------------------------------------------------
    def iniciar(self):
        # O login é feito antes de mostrar as opções que dependem do usuário.
        if not self._identificar():
            return
        c = self.cmd
        mostrar_mensagem(f"Olá, {c.usuario.login}! {c.resumo()}.")
        _menu("CATÁLOGO DE FILMES E SÉRIES", [
            ("Ver catálogo", self.ver_catalogo),
            ("Mídias", self.menu_midias),
            ("Minhas listas e favoritos", self.menu_listas),
            ("Relatórios", self.menu_relatorios),
            ("Configurações", self.menu_configuracoes),
        ], saida="Sair")
        mostrar_mensagem("Até logo!")

    def _identificar(self):
        c = self.cmd
        if c.usuario is not None:
            return True
        for _ in range(3):
            login = _ler_texto("Usuário: ")
            try:
                novo = c.entrar(login, ler_senha())
            except ValueError as erro:
                print(erro)
                continue
            mostrar_mensagem("Conta criada. Bem-vindo!" if novo else "Login realizado.")
            return True
        print("Não foi possível entrar.")
        return False

    # -- seleção ----------------------------------------------------------------
    def _escolher_midia(self, classe=None):
        # Guardamos as mídias por ID para validar a escolha sem procurar de novo.
        midias = [m for m in self.cmd.midias.listar() if classe is None or isinstance(m, classe)]
        if not midias:
            print("Nenhuma mídia disponível. Cadastre uma primeiro.")
            return None
        mostrar([linha(m) for m in midias])
        por_id = {m.id: m for m in midias}
        while True:
            id_midia = _ler_numero("Digite o ID da mídia (0 para cancelar): ", int, 0)
            if id_midia == 0:
                return None
            if id_midia in por_id:
                return por_id[id_midia]
            print("Esse ID não está na lista acima.")

    @staticmethod
    def _escolher_alvo(serie, so_episodio=False):
        """(temporada, episódio) a afetar; (None, None) é a série inteira; None cancela."""
        escopo = "episodio" if so_episodio else _escolher("APLICAR EM", [
            ("serie", "A série inteira"),
            ("temporada", "Uma temporada"),
            ("episodio", "Um episódio"),
        ])
        if escopo is None:
            return None
        if escopo == "serie":
            return None, None
        temporada = _escolher("TEMPORADA", [(t, str(t)) for t in serie.temporadas])
        if temporada is None:
            return None
        if escopo == "temporada":
            return temporada.numero, None
        episodio = _escolher("EPISÓDIO", [(e, str(e)) for e in temporada])
        return None if episodio is None else (temporada.numero, episodio.numero)

    def _escolher_lista(self):
        listas = self.cmd._exigir_usuario().listas
        return _escolher("SUAS LISTAS", [(l, f"{l.nome} ({len(l)})") for l in listas])

    # -- mídias -----------------------------------------------------------------
    def menu_midias(self):
        _menu("MÍDIAS", [
            ("Cadastrar filme ou série", self.cadastrar),
            ("Editar filme ou série", self.editar),
            ("Avaliar filme, série, temporada ou episódio", self.avaliar),
            ("Marcar como assistido / assistindo", self.atualizar_status),
            ("Sugestões para assistir", self.recomendar),
            ("Remover do catálogo", self.remover),
        ])

    def cadastrar(self):
        tipo = _escolher("O QUE CADASTRAR?", [("filme", "Filme"), ("serie", "Série")])
        if tipo is None:
            return
        dados = dict(
            titulo=_ler_texto("Título: "),
            genero=_ler_texto("Gênero: "),
            ano=_ler_numero("Ano: ", int, 1),
            classificacao=_ler_texto("Classificação indicativa (L, 10, 12, 14, 16, 18): "),
            elenco=input("Elenco, separado por vírgulas (Enter para pular): "),
        )
        if tipo == "filme":
            dados["duracao"] = _ler_numero("Duração em minutos: ", float, 0.01)
        midia = self.cmd.adicionar_midia(tipo, **dados)
        if tipo == "serie":
            quantidade_temporadas = _ler_numero("Número de temporadas: ", int, 1)
            episodios = _ler_texto("Episódios por temporada (ex.: 10,8,8): ")
            try:
                quantidades = [int(valor.strip()) for valor in episodios.split(",")]
            except ValueError:
                raise ValueError("Informe quantidades inteiras separadas por vírgulas.") from None
            if len(quantidades) != quantidade_temporadas or any(n <= 0 for n in quantidades):
                raise ValueError("Informe um número positivo de episódios para cada temporada.")
            duracao = _ler_numero("Duração média de cada episódio (min): ", float, 0.01)
            for numero, quantidade in enumerate(quantidades, start=1):
                self.cmd.adicionar_temporada(midia.id, quantidade, duracao, numero=numero)
        mostrar_mensagem(f"Cadastrado: {linha(midia)}")

    def editar(self):
        midia = self._escolher_midia()
        if midia is None:
            return
        dados = dict(
            titulo=_ler_texto(f"Título [{midia.titulo}]: "),
            genero=_ler_texto(f"Gênero [{midia.genero}]: "),
            ano=_ler_numero(f"Ano [{midia.ano}]: ", int, 1),
            classificacao=_ler_texto(f"Classificação [{midia.classificacao}]: "),
            elenco=input(f"Elenco [{', '.join(midia.elenco)}]: "),
        )
        if not dados["elenco"]:
            dados["elenco"] = ", ".join(midia.elenco)
        if not isinstance(midia, Serie):
            dados["duracao"] = _ler_numero(f"Duração em minutos [{midia.duracao:g}]: ", float, 0.01)
        self.cmd.editar_midia(midia.id, **dados)
        mostrar_mensagem(f"Atualizada: {linha(midia)}")

    def ver_catalogo(self):
        mostrar([linha(m) for m in self.cmd.listar()] or ["Catálogo vazio."])

    def buscar(self):
        achadas = self.cmd.listar(busca=_ler_texto("Parte do título: "))
        mostrar([linha(m) for m in achadas] or ["Nenhuma mídia encontrada."])

    def avaliar(self):
        midia = self._escolher_midia()
        if midia is None:
            return
        alvo = (None, None)
        if isinstance(midia, Serie):
            alvo = self._escolher_alvo(midia)
            if alvo is None:
                return
        nota = _ler_numero("Nota de 0 a 10: ", float, 0, 10)
        mostrar_mensagem(f"Avaliação registrada: {linha(self.cmd.avaliar(midia.id, nota, *alvo))}")

    def atualizar_status(self):
        midia = self._escolher_midia()
        if midia is None:
            return
        alvo = (None, None)
        if isinstance(midia, Serie):
            alvo = self._escolher_alvo(midia)
            if alvo is None:
                return
        status = _escolher("NOVO STATUS", [(s, s.value.capitalize()) for s in Status])
        if status is not None:
            mostrar_mensagem(f"Atualizado: {linha(self.cmd.atualizar_status(midia.id, status, *alvo))}")

    def recomendar(self):
        sugestoes = self.cmd.recomendar()
        minimo = self.cmd.config.nota_minima_recomendado
        mostrar_mensagem(f"Sugestões com nota média a partir de {minimo:g}:")
        mostrar([linha(m) for m in sugestoes] or ["Ainda não há mídias avaliadas com essa nota."])

    def remover(self):
        midia = self._escolher_midia()
        if midia is not None and _confirmar(f"Remover '{midia.titulo}' para sempre?"):
            self.cmd.remover(midia.id)
            mostrar_mensagem("Removida.")

    # -- séries -----------------------------------------------------------------
    def menu_series(self):
        _menu("SÉRIES", [
            ("Adicionar temporada (episódios criados automaticamente)", self.adicionar_temporada),
            ("Adicionar um episódio avulso", self.adicionar_episodio),
            ("Ver temporadas e episódios", self.ver_episodios),
        ])

    def adicionar_temporada(self):
        serie = self._escolher_midia(Serie)
        if serie is not None:
            self._temporadas(serie.id)

    def _temporadas(self, id_serie):
        while True:
            quantidade = _ler_numero("Quantos episódios tem a temporada? ", int, 1)
            duracao = _ler_numero("Duração média de cada episódio (min): ", float, 0.01)
            serie, numero = self.cmd.adicionar_temporada(id_serie, quantidade, duracao,
                                                         _data_opcional())
            mostrar_mensagem(f"Temporada {numero} criada com {quantidade} episódios.")
            if not _confirmar("Adicionar mais uma temporada?"):
                return

    def adicionar_episodio(self):
        serie = self._escolher_midia(Serie)
        if serie is None:
            return
        self.cmd.adicionar_episodio(
            serie.id,
            _ler_numero("Temporada: ", int, 1),
            _ler_numero("Número do episódio: ", int, 1),
            _ler_texto("Título do episódio: "),
            _ler_numero("Duração (min): ", float, 0.01),
            _data_opcional(),
        )
        mostrar_mensagem("Episódio adicionado.")

    def ver_episodios(self):
        serie = self._escolher_midia(Serie)
        if serie is not None:
            mostrar(self.cmd.episodios(serie.id))

    # -- listas -----------------------------------------------------------------
    def menu_listas(self):
        self.cmd._exigir_usuario()
        _menu("MINHAS LISTAS", [
            ("Ver minhas listas", lambda: mostrar(self.cmd.listas())),
            ("Ver o conteúdo de uma lista", self.ver_lista),
            ("Criar lista", self.criar_lista),
            ("Adicionar mídia a uma lista", self.adicionar_na_lista),
            ("Remover mídia de uma lista", self.remover_da_lista),
            ("Adicionar aos favoritos", self.adicionar_favorito),
            ("Apagar lista", self.apagar_lista),
        ])

    def criar_lista(self):
        mostrar_mensagem(f"Lista criada: {self.cmd.criar_lista(_ler_texto('Nome da lista: ')).nome}")

    def ver_lista(self):
        lista = self._escolher_lista()
        if lista is not None:
            mostrar(self.cmd.listas(lista.nome))

    def adicionar_na_lista(self):
        lista = self._escolher_lista()
        midia = self._escolher_midia() if lista is not None else None
        if midia is not None:
            self.cmd.adicionar_na_lista(lista.nome, midia.id)
            mostrar_mensagem(f"Adicionada à lista '{lista.nome}'.")

    def remover_da_lista(self):
        lista = self._escolher_lista()
        if lista is None:
            return
        mostrar(self.cmd.listas(lista.nome))
        id_midia = _ler_numero("ID da mídia a remover (0 para cancelar): ", int, 0)
        if id_midia:
            self.cmd.remover_da_lista(lista.nome, id_midia)
            mostrar_mensagem(f"Removida da lista '{lista.nome}'.")

    def adicionar_favorito(self):
        midia = self._escolher_midia()
        if midia is not None:
            self.cmd.adicionar_favorito(midia.id)
            mostrar_mensagem("Adicionada aos favoritos.")

    def apagar_lista(self):
        lista = self._escolher_lista()
        if lista is not None and _confirmar(f"Apagar a lista '{lista.nome}'?"):
            self.cmd.apagar_lista(lista.nome)
            mostrar_mensagem("Lista apagada.")

    # -- relatórios ---------------------------------------------------------------
    def menu_relatorios(self):
        def ver(qual, por=None):
            return lambda: mostrar(self.cmd.relatorio(qual, por))

        def resumo_tempo():
            mostrar(self.cmd.relatorio("geral"))
            mostrar(self.cmd.relatorio("tempo"))
            mostrar(["Por semana:", *self.cmd.relatorio("periodo", "semana")])
            mostrar(["Por mês:", *self.cmd.relatorio("periodo", "mes")])

        _menu("RELATÓRIOS", [
            ("Resumo e tempo assistido", resumo_tempo),
            ("Top 10", ver("top")),
            ("Notas por gênero", ver("notas", "genero")),
            ("Séries com mais episódios assistidos", ver("series")),
            ("Histórico", ver("historico")),
        ])

    # -- configurações -------------------------------------------------------------
    def menu_configuracoes(self):
        def alterar(chave, rotulo):
            def acao():
                print(f"{rotulo} (atual: {getattr(self.cmd.config, chave)})")
                self.cmd.definir_config(chave, _ler_texto("Novo valor: "))
                mostrar_mensagem("Configuração salva.")
            return acao

        _menu("CONFIGURAÇÕES", [
            ("Ver configurações", lambda: mostrar(self.cmd.config_linhas())),
            ("Nota mínima para sugestões", alterar("nota_minima_recomendado", "Nota mínima")),
            ("Limite de listas por usuário", alterar("limite_listas", "Limite de listas")),
            ("Multiplicador de duração (minutos → horas)",
             alterar("multiplicador_duracao", "Multiplicador")),
        ])

    def sair_da_conta(self):
        self.cmd.sair()
        raise SystemExit("Você saiu da conta. Até logo!")
