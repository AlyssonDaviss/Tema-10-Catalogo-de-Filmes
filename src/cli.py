# Classe: CLI
class CLI:
    """
    A classe CLI (Command Line Interface) representa a interface de linha de comando do sistema.
    Ela permite que os usuários interajam com o sistema por meio de comandos digitados no terminal.
    
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