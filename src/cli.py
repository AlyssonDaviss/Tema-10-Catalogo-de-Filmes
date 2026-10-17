from repositories.cadastrar_midia import CadastrarMidia
from repositories.cadastrar_avaliacao import CadastrarAvaliacao
from src.midia import Midia, Serie, Episodio
from src.avaliacao import Avaliação


class CLI:
    """Interface de linha de comando do sistema."""

    def __init__(self, comando=None, argumentos=None, id_usuario=None):
        self.comando = comando
        self.argumentos = argumentos or []
        self.id_usuario = id_usuario

    def Executar(self):
        """Exibe o menu principal e processa as opções."""
        comandos = Comandos(self.id_usuario)

        while True:
            print("\n===== MENU PRINCIPAL =====")
            print("1 - Cadastrar mídia")
            print("2 - Listar mídias")
            print("3 - Avaliar mídia")
            print("4 - Sair")

            opcao = input("Opção: ")

            if opcao == "1":
                comandos.Cadastrar()

            elif opcao == "2":
                comandos.Listar()

            elif opcao == "3":
                comandos.Avaliar()

            elif opcao == "4":
                print("Saindo...")
                break

            else:
                print("Opção inválida.")

    def Processar_comando(self):
        """Processa um comando específico."""
        comandos = Comandos(self.id_usuario)

        if self.comando == "listar":
            return comandos.Listar()

        elif self.comando == "cadastrar":
            return comandos.Cadastrar()

        elif self.comando == "avaliar":
            return comandos.Avaliar()

        else:
            self.Mostrar_ajuda()

    def Mostrar_ajuda(self):
        """Mostra os comandos disponíveis."""
        print("Comandos disponíveis:")
        print("cadastrar - Cadastrar mídia")
        print("listar - Listar mídias")
        print("avaliar - Avaliar mídia")


class Comandos:
    """Executa as operações do sistema."""

    def __init__(self, id_usuario=None):
        self.id_usuario = id_usuario

    def Cadastrar(self):
        """Cadastra um filme ou uma série."""
        titulo = input("Título da mídia: ").strip()
        tipo = input("Tipo (filme/série): ").strip().lower()
        genero = input("Gênero: ").strip()
        ano = input("Ano de lançamento: ").strip()
        classificacao_indicativa = input("Classificação indicativa: ").strip()
        elenco = input("Elenco (opcional): ").strip()
        status = input("Status: ").strip()

        if tipo not in ("filme", "serie", "série"):
            print("Tipo de mídia inválido.")
            return

        if tipo == "série":
            tipo = "serie"

        midia = Midia(
            titulo,
            tipo,
            genero,
            ano,
            classificacao_indicativa,
            elenco,
            status
        )

        cadastro_midia = CadastrarMidia()

        id_midia = cadastro_midia.cadastrar_midia(midia)

        if not id_midia:
            print("Mídia já cadastrada ou tipo inválido.")
            return

        # Cadastro de filme
        if tipo == "filme":
            duracao = input("Duração: ").strip()

            resultado = cadastro_midia.atualizar_duracao(
                id_midia, duracao
            )

            if resultado is True:
                print("Duração cadastrada.")
            else:
                print(resultado)
                return

        # Cadastro de série
        elif tipo == "serie":
            # Mantenha aqui todo o seu código de cadastro da série
            ...

        # Mensagem final, só depois de concluir todo o cadastro
        print(f"Mídia cadastrada com sucesso! ID: {id_midia}")

    def Listar(self):
        """Lista o ID, o título e o tipo das mídias."""
        cadastro_midia = CadastrarMidia()
        dados = cadastro_midia.carregar_dados()

        if not dados:
            print("Nenhuma mídia cadastrada.")
            return

        print(
            f"\n{'ID':<8} {'Nome':<30} {'Tipo'}"
        )
        print("-" * 50)

        for id_midia, midia in dados.items():
            print(
                f"{id_midia:<8} "
                f"{midia.get('titulo', 'Sem título'):<30} "
                f"{midia.get('tipo', 'Desconhecido').capitalize()}"
            )

    def Buscar(self):
        """Busca uma mídia pelo título."""
        cadastro_midia = CadastrarMidia()
        dados = cadastro_midia.carregar_dados()

        titulo_busca = input(
            "Digite o título da mídia: "
        ).strip().casefold()

        encontrados = [
            (id_midia, midia)
            for id_midia, midia in dados.items()
            if titulo_busca
            in midia.get("titulo", "").casefold()
        ]

        if not encontrados:
            print("Nenhuma mídia encontrada.")
            return

        for id_midia, midia in encontrados:
            print(
                f"ID: {id_midia} | "
                f"Título: {midia.get('titulo')} | "
                f"Tipo: {midia.get('tipo')}"
            )

    def Avaliar(self):
        """Permite avaliar uma mídia cadastrada."""
        if self.id_usuario is None:
            print("Não foi possível identificar o usuário logado.")
            return

        cadastro_midia = CadastrarMidia()
        cadastro_avaliacao = CadastrarAvaliacao()

        while True:
            print("\n===== AVALIAR MÍDIA =====")
            print("1 - Pesquisar por nome/ID")
            print("2 - Listar mídias")
            print("3 - Sair")

            opcao = input("Opção: ").strip()

            if opcao == "1":
                busca = input("Digite o nome ou ID da mídia: ").strip()
                dados = cadastro_midia.carregar_dados()

                encontrados = [
                    (id_midia, midia)
                    for id_midia, midia in dados.items()
                    if busca.casefold() == str(id_midia).casefold()
                    or busca.casefold() in midia.get("titulo", "").casefold()
                ]

                if not encontrados:
                    print("Nenhuma mídia encontrada.")
                    continue

                for id_midia, midia in encontrados:
                    print(
                        f"ID: {id_midia} | "
                        f"Título: {midia.get('titulo')} | "
                        f"Tipo: {midia.get('tipo')}"
                    )

                id_escolhido = input(
                    "Digite o ID da mídia que deseja avaliar: "
                ).strip()

                if id_escolhido not in dados:
                    print("ID inválido.")
                    continue

                self._avaliar_midia(
                    cadastro_avaliacao, id_escolhido, dados[id_escolhido]
                )

            elif opcao == "2":
                self.Listar()

                dados = cadastro_midia.carregar_dados()
                if not dados:
                    continue

                id_escolhido = input(
                    "Digite o ID da mídia que deseja avaliar: "
                ).strip()

                if id_escolhido not in dados:
                    print("ID inválido.")
                    continue

                self._avaliar_midia(
                    cadastro_avaliacao, id_escolhido, dados[id_escolhido]
                )

            elif opcao == "3":
                break

            else:
                print("Opção inválida.")

    def _avaliar_midia(self, cadastro_avaliacao, id_midia, midia):
        """Solicita nota, status e comentário e salva a avaliação."""
        print(f"\nAvaliando: {midia.get('titulo')}")

        try:
            nota = float(input("Nota (0 a 10): ").strip().replace(",", "."))
        except ValueError:
            print("Nota inválida.")
            return

        print("\nStatus:")
        print("1 - Planejando")
        print("2 - Completo")
        print("3 - Assistindo")
        print("4 - Assistido")
        print("5 - Pausado")
        print("6 - Dropado")

        status_opcoes = {
            "1": "planejando",
            "2": "completo",
            "3": "assistindo",
            "4": "assistido",
            "5": "pausado",
            "6": "dropado"
        }

        opcao_status = input("Escolha: ").strip()

        if opcao_status not in status_opcoes:
            print("Opção de status inválida.")
            return

        status = status_opcoes[opcao_status]

        comentario = input("Comentário (opcional): ").strip()

        # A classe Avaliação só valida nota e comentário
        avaliacao = Avaliação()

        resultado = avaliacao.Registrar_nota(nota)
        if resultado is not True:
            print(resultado)
            return

        resultado = avaliacao.Registrar_comentario(comentario)
        if resultado is not True:
            print(resultado)
            return

        # O repositório salva usuário, mídia, nota, status e comentário no JSON
        resultado = cadastro_avaliacao.registrar_avaliacao(
            self.id_usuario,
            id_midia,
            nota,
            status,
            comentario
        )

        if resultado is True:
            print("Avaliação registrada com sucesso!")
        else:
            print(resultado)

    def Remover(self):
        """Remove uma mídia."""
        print("Funcionalidade de remoção ainda não implementada.")

    def Criar_lista(self):
        """Cria uma lista de mídias."""
        print("Funcionalidade de listas ainda não implementada.")

    def Gerar_relatorio(self):
        """Gera um relatório."""
        print("Funcionalidade de relatórios ainda não implementada.")

    def Mostrar_config(self):
        """Mostra as configurações."""
        print("Configurações do sistema.")