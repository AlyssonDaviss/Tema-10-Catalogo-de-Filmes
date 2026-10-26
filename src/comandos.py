"""Regras de uso do sistema, sem entrada nem saída de tela.

É a camada comum aos subcomandos (src/cli.py) e ao menu interativo (src/menu.py):
cada método recebe valores prontos, aplica as regras, grava e devolve o resultado.
"""

import random

from repositories.cadastrar_config import CadastrarConfiguracoes
from repositories.cadastrar_midia import CadastrarMidia
from repositories.cadastrar_pessoa import CadastrarUsuario
from repositories.cadastrar_sessao import CadastrarSessao
from src import relatorio
from src.midia import Episodio, Filme, Serie, Status, normalizar
from src.seed import popular
from src.user import Usuario

DICA_LOGIN = "Entre primeiro com: python main.py usuario entrar SEU_NOME"
RELATORIOS = ("geral", "notas", "tempo", "top", "series", "periodo", "historico")


def linha(midia):
    return f"[{midia.id}] {midia}"


def mostrar(linhas):
    print("\n".join(linhas))


def ler_senha(mensagem="Senha: "):
    """Lê a senha com input(). O getpass trava em vários terminais do Windows
    (Git Bash, Code Runner, consoles de IDE), então a senha aparece enquanto é digitada."""
    return input(mensagem).strip()


class Comandos:
    def __init__(self, pasta=None, id_usuario=None):
        self.midias = CadastrarMidia(pasta)
        self.pessoas = CadastrarUsuario(pasta)
        self.sessao = CadastrarSessao(pasta)
        self.repositorio_config = CadastrarConfiguracoes(pasta)
        self.config = self.repositorio_config.carregar()
        self.usuario = None
        id_usuario = id_usuario or self.sessao.atual()
        if id_usuario:
            try:
                self.usuario = self.pessoas.carregar_usuario(id_usuario)
            except ValueError:  # usuário apagado: sessão antiga
                self.sessao.limpar()

    # -- conta ----------------------------------------------------------------
    def usuario_existe(self, login):
        return self.pessoas.obter_id(login.strip()) is not None

    def entrar(self, login, senha):
        """Faz login (criando a conta se for nova). Devolve True se a conta foi criada."""
        usuario = Usuario(login, senha)
        resultado = self.pessoas.autenticar(usuario)
        if resultado == "senha_incorreta":
            raise ValueError("Senha incorreta.")
        novo = resultado == "usuario_inexistente"
        if novo:
            self.pessoas.cadastrar(usuario)
        self.usuario = self.pessoas.carregar_usuario(self.pessoas.obter_id(usuario.login))
        self.sessao.definir(self.usuario.id)
        return novo

    def sair(self):
        self.sessao.limpar()
        self.usuario = None

    def _exigir_usuario(self):
        if self.usuario is None:
            raise ValueError(f"Esta ação exige login. {DICA_LOGIN}")
        return self.usuario

    def _salvar_usuario(self):
        self.pessoas.salvar_usuario(self.usuario)

    # -- mídias ---------------------------------------------------------------
    def adicionar_midia(self, tipo, titulo, genero, ano, classificacao, elenco="", duracao=None):
        tipo = normalizar(tipo)
        comuns = (titulo, genero, ano, classificacao, elenco)
        if tipo == "filme":
            if duracao is None:
                raise ValueError("Filmes exigem a duração em minutos (--duracao).")
            midia = Filme(*comuns, duracao)
        elif tipo == "serie":
            if duracao is not None:
                raise ValueError("Séries não têm duração própria: ela vem dos episódios.")
            midia = Serie(*comuns)
        else:
            raise ValueError("Tipo inválido. Use 'filme' ou 'serie'.")
        return self.midias.cadastrar(midia)

    def listar(self, tipo=None, status=None, genero=None, busca=None):
        tipo = tipo and normalizar(tipo)
        genero = genero and normalizar(genero)
        busca = busca and normalizar(busca)
        status = status and Status.converter(status)
        return [
            m for m in self.midias.listar()
            if (tipo is None or normalizar(m.tipo) == tipo)
            and (status is None or m.status is status)
            and (genero is None or normalizar(m.genero) == genero)
            and (busca is None or busca in normalizar(m.titulo))
        ]

    def avaliar(self, id_midia, nota, temporada=None, episodio=None):
        midia = self.midias.obter(id_midia)
        midia.avaliar(nota, temporada, episodio)
        self.midias.salvar_midia(midia)
        return midia

    def atualizar_status(self, id_midia, status, temporada=None, episodio=None):
        """Muda o status; cada filme/episódio concluído agora entra no histórico."""
        usuario = self._exigir_usuario()
        midia = self.midias.obter(id_midia)
        for descricao, minutos in midia.definir_status(status, temporada, episodio):
            usuario.registrar_conclusao(midia.id, descricao, minutos)
        self.midias.salvar_midia(midia)
        self._salvar_usuario()
        return midia

    def remover(self, id_midia):
        midia = self.midias.remover(id_midia)
        if self.usuario is not None:
            self.usuario.remover_midia_de_todas(midia.id)
            self._salvar_usuario()
        return midia

    def recomendar(self, quantidade=3):
        minimo = self.config.nota_minima_recomendado
        candidatas = [
            m for m in self.midias.listar()
            if m.nota_media is not None and m.nota_media >= minimo
        ]
        return random.sample(candidatas, min(quantidade, len(candidatas)))

    def resumo(self):
        midias = self.midias.listar()
        return f"{len(midias)} mídia(s) no catálogo, {len(relatorio.finalizadas(midias))} finalizada(s)"

    # -- séries ---------------------------------------------------------------
    def _serie(self, id_midia):
        serie = self.midias.obter(id_midia)
        if not isinstance(serie, Serie):
            raise ValueError(f"'{serie.titulo}' não é uma série.")
        return serie

    def adicionar_temporada(self, id_midia, quantidade, duracao, data=None, numero=None):
        """Cria a próxima temporada (ou a de número informado) com N episódios genéricos."""
        serie = self._serie(id_midia)
        numero = numero or max((t.numero for t in serie.temporadas), default=0) + 1
        serie.criar_temporada(numero, quantidade, duracao, data)
        self.midias.salvar_midia(serie)
        return serie, numero

    def adicionar_episodio(self, id_midia, temporada, numero, titulo, duracao, data=None):
        serie = self._serie(id_midia)
        serie.adicionar_episodio(Episodio(temporada, numero, titulo, duracao, data))
        self.midias.salvar_midia(serie)
        return serie

    def episodios(self, id_midia):
        serie = self._serie(id_midia)
        linhas = [str(serie)]
        for temporada in serie.temporadas:
            linhas.append(f"  {temporada}")
            linhas.extend(f"    {episodio}" for episodio in temporada)
        return linhas

    # -- listas e favoritos ---------------------------------------------------
    def criar_lista(self, nome):
        lista = self._exigir_usuario().criar_lista(nome, self.config.limite_listas)
        self._salvar_usuario()
        return lista

    def apagar_lista(self, nome):
        self._exigir_usuario().apagar_lista(nome)
        self._salvar_usuario()

    def adicionar_favorito(self, id_midia):
        usuario = self._exigir_usuario()
        usuario.adicionar_favorito(self.midias.obter(id_midia).id, self.config.limite_listas)
        self._salvar_usuario()

    def adicionar_na_lista(self, nome, id_midia):
        lista = self._exigir_usuario().lista(nome)
        lista.adicionar(self.midias.obter(id_midia).id)
        self._salvar_usuario()
        return lista

    def remover_da_lista(self, nome, id_midia):
        lista = self._exigir_usuario().lista(nome)
        lista.remover(self.midias.obter(id_midia).id)
        self._salvar_usuario()
        return lista

    def listas(self, nome=None):
        """Resumo das listas, ou o conteúdo de uma delas."""
        usuario = self._exigir_usuario()
        if nome is None:
            linhas = [f"{l.nome}: {len(l)} mídia(s)" for l in usuario.listas]
            return linhas or ["Você ainda não tem listas. Crie uma com: usuario criar-lista NOME"]
        linhas = []
        for id_midia in usuario.lista(nome).midias:
            try:
                linhas.append(linha(self.midias.obter(id_midia)))
            except ValueError:  # removida do catálogo por outro usuário
                linhas.append(f"[{id_midia}] (mídia removida do catálogo)")
        return linhas or ["A lista está vazia."]

    # -- relatórios -----------------------------------------------------------
    def _tempo(self, minutos):
        return f"{minutos:g} min ({self.config.horas(minutos):g} h)"

    def relatorio(self, qual, por=None, quantidade=10):
        midias = self.midias.listar()
        if qual == "geral":
            nota = relatorio.nota_geral(midias)
            total = sum(m.minutos_assistidos for m in midias)
            return [
                self.resumo().capitalize(),
                f"Nota geral do catálogo: {'sem notas' if nota is None else f'{nota:.2f}'}",
                f"Tempo total assistido: {self._tempo(total)}",
            ]
        if qual == "notas":
            por = por or "genero"
            if por not in ("genero", "tipo"):
                raise ValueError("Para 'notas' use --por genero ou --por tipo.")
            dados = relatorio.media_por(midias, por)
            return [f"{chave}: {nota:.2f}" for chave, nota in dados.items()] or [
                "Nenhuma mídia finalizada com nota."]
        if qual == "tempo":
            return [f"{tipo}: {self._tempo(m)}"
                    for tipo, m in relatorio.minutos_por_tipo(midias).items()]
        if qual == "top":
            ranking = relatorio.top(midias, quantidade)
            return [f"{i}º {m.titulo} ({m.tipo}) - {m.nota_media:.2f}"
                    for i, m in enumerate(ranking, start=1)] or [
                "Nenhuma mídia finalizada com nota."]
        if qual == "series":
            ranking = relatorio.series_mais_assistidas(midias)
            return [f"{s.titulo}: {n} de {len(s)} episódios assistidos"
                    for s, n in ranking] or ["Nenhum episódio assistido ainda."]
        if qual == "periodo":
            por = por or "mes"
            dados = relatorio.minutos_por_periodo(self._exigir_usuario(), por)
            return [f"{periodo}: {self._tempo(m)}" for periodo, m in dados.items()] or [
                "Nenhuma conclusão registrada no histórico."]
        if qual == "historico":
            historico = self._exigir_usuario().historico
            return [f"{r.concluido_em:%d/%m/%Y %H:%M}  {r.descricao} ({r.minutos:g} min)"
                    for r in historico] or ["Histórico vazio."]
        raise ValueError(f"Relatório desconhecido. Opções: {', '.join(RELATORIOS)}.")

    # -- configurações e exemplos --------------------------------------------
    def config_linhas(self):
        return [f"{chave}: {valor}" for chave, valor in vars(self.config).items()]

    def definir_config(self, chave, valor):
        self.config = self.config.definir(chave, str(valor).replace(",", "."))
        self.repositorio_config.salvar(self.config)

    def carregar_exemplos(self):
        novas = popular(self.midias, self._exigir_usuario())
        self._salvar_usuario()
        return novas
