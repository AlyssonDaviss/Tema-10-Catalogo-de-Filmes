# Classe: Usuário
class Usuário:
    """
    Classe: Usuário
    Atributos: Login e Senha
    Métodos: Fazer login
    """

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    def Fazer_login(self):
        """Método: Fazer login"""
        pass


# Classe: CLI
class CLI:
    """
    Classe: CLI
    Atributos: Comando e Argumentos
    Métodos: Executar, Processar comando e Mostrar ajuda
    """

    def __init__(self, comando, argumentos):
        self.comando = comando
        self.argumentos = argumentos

    def Executar(self):
        """Método: Executar"""
        pass

    def Processar_comando(self):
        """Método: Processar comando"""
        pass

    def Mostrar_ajuda(self):
        """Método: Mostrar ajuda"""
        pass


# Classe: Comandos
class Comandos:
    """
    Classe: Comandos
    Métodos: Cadastrar, Listar, Buscar, Avaliar, Remover, Criar lista,
    Gerar relatório e Mostrar configuração
    """

    def Cadastrar(self):
        """Método: Cadastrar"""
        pass

    def Listar(self):
        """Método: Listar"""
        pass

    def Buscar(self):
        """Método: Buscar"""
        pass

    def Avaliar(self):
        """Método: Avaliar"""
        pass

    def Remover(self):
        """Método: Remover"""
        pass

    def Criar_lista(self):
        """Método: Criar lista"""
        pass

    def Gerar_relatorio(self):
        """Método: Gerar relatório"""
        pass

    def Mostrar_config(self):
        """Método: Mostrar configuração"""
        pass


# Classe: Mídia
class Mídia:
    """
    Classe: Mídia
    Atributos: Título, Tipo, Gênero, Ano, Classificação Indicativa,
    Elenco e Status
    Métodos: Cadastrar mídia, Impedir duplicidade e Registrar status
    """

    def __init__(
        self,
        titulo,
        tipo,
        genero,
        ano,
        classificacao_indicativa,
        elenco,
        status
    ):
        self.titulo = titulo
        self.tipo = tipo
        self.genero = genero
        self.ano = ano
        self.classificacao_indicativa = classificacao_indicativa
        self.elenco = elenco
        self.status = status

    def Cadastrar_Midia(self):
        """Método: Cadastrar mídia"""
        pass

    def Impedir_Duplicidade(self):
        """Método: Impedir duplicidade"""
        pass

    def Registrar_status(self):
        """Método: Registrar status"""
        pass


# Classe: Filme
class Filme(Mídia):
    """
    Classe: Filme
    Herda de: Mídia
    Atributos: Duração
    Métodos: Registrar duração
    """

    def __init__(self, duracao):
        self.duracao = duracao

    def Registrar_duração(self):
        """Método: Registrar duração"""
        pass


# Classe: Série
class Série(Mídia):
    """
    Classe: Série
    Herda de: Mídia
    Atributos: nº Temporadas, nº Episódios e Nota opcional
    Métodos: Registrar temporadas e Atualizar status
    """

    def __init__(self, numero_temporadas, numero_episodios, nota=None):
        self.numero_temporadas = numero_temporadas
        self.numero_episodios = numero_episodios
        self.nota = nota

    def Registrar_temporadas(self):
        """Método: Registrar temporadas"""
        pass

    def Atualizar_status(self):
        """Método: Atualizar status"""
        pass


# Classe: Temporada
class Temporada:
    """
    Classe: Temporada
    Se relaciona com: Série e Episódio
    Atributos: Título, nº Episódios, Data de lançamento e Nota opcional
    Métodos: Registrar episódios
    """

    def __init__(self, titulo, numero_episodios, data_lancamento, nota=None):
        self.titulo = titulo
        self.numero_episodios = numero_episodios
        self.data_lancamento = data_lancamento
        self.nota = nota

    def Registrar_episodios(self):
        """Método: Registrar episódios"""
        pass


# Classe: Episódio
class Episódio:
    """
    Classe: Episódio
    Se relaciona com: Temporada e Avaliação
    Atributos: nº Episódio, Título, Duração, Data de lançamento,
    Status de visualização e Nota opcional
    Métodos: Registrar status
    """

    def __init__(
        self,
        numero_episodio,
        titulo,
        duracao,
        data_lancamento,
        status_visualizacao,
        nota=None
    ):
        self.numero_episodio = numero_episodio
        self.titulo = titulo
        self.duracao = duracao
        self.data_lancamento = data_lancamento
        self.status_visualizacao = status_visualizacao
        self.nota = nota

    def Registrar_status(self):
        """Método: Registrar status"""
        pass


# Classe: Avaliação
class Avaliação:
    """
    Classe: Avaliação
    Se relaciona com: Usuário, Mídia e Episódio
    Atributos: Nota e Comentário
    Métodos: Gerar média, Registrar nota e Registrar comentário
    """

    def __init__(self, nota, comentario):
        self.nota = nota
        self.comentario = comentario

    def Gerar_media(self):
        """Método: Gerar média"""
        pass

    def Registrar_nota(self):
        """Método: Registrar nota"""
        pass

    def Registrar_comentario(self):
        """Método: Registrar comentário"""
        pass


# Classe: Histórico de visualização
class Histórico_de_visualização:
    """
    Classe: Histórico de visualização
    Se relaciona com: Usuário e Mídia
    Atributos: Mídia, Data e Hora
    Métodos: Salvar histórico e Registrar data e hora
    """

    def __init__(self, midia, data, hora):
        self.midia = midia
        self.data = data
        self.hora = hora

    def Salvar_historico(self):
        """Método: Salvar histórico"""
        pass

    def Registrar_data_hora(self):
        """Método: Registrar data e hora"""
        pass


# Classe: Lista
class Lista:
    """
    Classe: Lista
    Se relaciona com: Usuário e Mídia
    Atributos: Nome, Tipo e Conteúdo
    Métodos: Criar lista, Adicionar na lista, Remover na lista e Apagar lista
    """

    def __init__(self, nome, tipo, conteudo):
        self.nome = nome
        self.tipo = tipo
        self.conteudo = conteudo

    def Criar_lista(self):
        """Método: Criar lista"""
        pass

    def Adicionar_na_lista(self):
        """Método: Adicionar na lista"""
        pass

    def Remover_na_lista(self):
        """Método: Remover na lista"""
        pass

    def Apagar_lista(self):
        """Método: Apagar lista"""
        pass


# Classe: Relatório
class Relatório:
    """
    Classe: Relatório
    Métodos: Gerar média geral do catálogo, Gerar relatório, Média por gênero,
    Tempo total por tipo, Top 10 e Série com maior número de episódios assistidos
    """

    def Gerar_media_geral_catalogo(self):
        """Método: Gerar média geral do catálogo"""
        pass

    def Gerar_relatorio(self):
        """Método: Gerar relatório"""
        pass

    def Media_genero(self):
        """Método: Média por gênero"""
        pass

    def Tempo_total_tipo(self):
        """Método: Tempo total por tipo"""
        pass

    def Top_10(self):
        """Método: Top 10"""
        pass

    def Serie_maior_numero_ep_assistidos(self):
        """Método: Série com maior número de episódios assistidos"""
        pass


# Classe: Configurações
class Configurações:
    """
    Classe: Configurações
    Atributos: Nota mínima para a recomendação e limite de listas personalizadas por usuário
    Métodos: Mostrar configuração, Nota mínima recomendada e Limite de lista
    """

    def __init__(self, nota_min_recomendacao, limite_listas_personalizadas):
        self.nota_min_recomendacao = nota_min_recomendacao
        self.limite_listas_personalizadas = limite_listas_personalizadas

    def Mostrar_config(self):
        """Método: Mostrar configuração"""
        pass

    def Nota_min_recomendado(self):
        """Método: Nota mínima recomendada"""
        pass

    def Limite_lista(self):
        """Método: Limite de lista"""
        pass
