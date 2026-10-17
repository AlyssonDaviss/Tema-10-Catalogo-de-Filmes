
from repositories.cadastrar_midia import CadastrarMidia
from repositories.cadastrar_avaliacao import CadastrarAvaliacao
from src.midia import Midia, Serie, Episodio
from src.avaliacao import Avaliação
from src.relatorio import Relatório


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
            print("4 - Relatórios")
            print("0 - Sair")

            opcao = input("Opção: ").strip()

            if opcao == "1":
                comandos.Cadastrar()
            elif opcao == "2":
                comandos.Listar()
            elif opcao == "3":
                comandos.Avaliar()
            elif opcao == "4":
                comandos.Gerar_relatorio()
            elif opcao == "0":
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
        elif self.comando == "relatorios":
            return comandos.Gerar_relatorio()
        else:
            self.Mostrar_ajuda()

    def Mostrar_ajuda(self):
        """Mostra os comandos disponíveis."""
        print("Comandos disponíveis:")
        print("cadastrar - Cadastrar mídia")
        print("listar - Listar mídias")
        print("avaliar - Avaliar mídia")
        print("relatorios - Exibir relatórios")


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
        classificacao_indicativa = input(
            "Classificação indicativa: "
        ).strip()
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

        if tipo == "filme":
            while True:
                duracao = input(
                    "Duração em minutos (ex.: 120m): "
                ).strip()

                if duracao:
                    break

                print("A duração não pode ficar vazia.")

            resultado = cadastro_midia.atualizar_duracao(
                id_midia, duracao
            )

            if resultado is not True:
                print(resultado)
                return

        elif tipo == "serie":
            serie = Serie(
                titulo,
                tipo,
                genero,
                ano,
                classificacao_indicativa,
                elenco,
                status
            )

            numero_temporada = 1

            while True:
                print(f"\n===== TEMPORADA {numero_temporada} =====")

                nome_temporada = input(
                    "Nome da temporada (Enter para automático): "
                ).strip()

                if not nome_temporada:
                    nome_temporada = f"Temporada {numero_temporada}"

                while True:
                    try:
                        numero_episodios = int(
                            input("Quantidade de episódios: ").strip()
                        )

                        if numero_episodios < 1:
                            print("A quantidade deve ser maior que zero.")
                            continue

                        break

                    except ValueError:
                        print("Digite um número inteiro válido.")

                data_lancamento = input(
                    "Data de lançamento da temporada: "
                ).strip()

                while True:
                    try:
                        duracao_media = float(
                            input(
                                "Duração média dos episódios (em minutos): "
                            ).strip().replace(",", ".")
                        )

                        if duracao_media <= 0:
                            print("A duração deve ser maior que zero.")
                            continue

                        break

                    except ValueError:
                        print("Digite uma duração válida em minutos.")

                temporada = serie.registrar_temporadas(
                    numero_temporada,
                    numero_episodios,
                    data_lancamento,
                    nome_temporada
                )

                id_temporada = cadastro_midia.cadastrar_temporada(
                    id_midia,
                    temporada
                )

                if not str(id_temporada).isdigit():
                    print(id_temporada)
                    return

                for numero in range(1, numero_episodios + 1):
                    episodio = Episodio.criar_automatico(
                        numero,
                        duracao_media
                    )

                    resultado = cadastro_midia.registrar_episodio(
                        id_midia,
                        id_temporada,
                        episodio
                    )

                    if resultado is not True:
                        print(resultado)
                        return

                print(
                    f"{nome_temporada} cadastrada com "
                    f"{numero_episodios} episódios."
                )

                numero_temporada += 1

                continuar = input(
                    "Deseja cadastrar outra temporada? (s/n): "
                ).strip().lower()

                while continuar not in ("s", "n"):
                    print("Digite s para sim ou n para não.")
                    continuar = input(
                        "Deseja cadastrar outra temporada? (s/n): "
                    ).strip().lower()

                if continuar != "s":
                    break

        print(f"Mídia cadastrada com sucesso! ID: {id_midia}")

    def Listar(self):
        """Lista o ID, o título e o tipo das mídias."""
        cadastro_midia = CadastrarMidia()
        dados = cadastro_midia.carregar_dados()

        if not dados:
            print("Nenhuma mídia cadastrada.")
            return

        print(f"\n{'ID':<8} {'Nome':<30} {'Tipo'}")
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
            if titulo_busca in midia.get("titulo", "").casefold()
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
                busca = input(
                    "Digite o nome ou ID da mídia: "
                ).strip()
                dados = cadastro_midia.carregar_dados()

                encontrados = [
                    (id_midia, midia)
                    for id_midia, midia in dados.items()
                    if busca.casefold() == str(id_midia).casefold()
                    or busca.casefold()
                    in midia.get("titulo", "").casefold()
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
                    cadastro_avaliacao,
                    id_escolhido,
                    dados[id_escolhido]
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
                    cadastro_avaliacao,
                    id_escolhido,
                    dados[id_escolhido]
                )

            elif opcao == "3":
                break
            else:
                print("Opção inválida.")

    def _avaliar_midia(self, cadastro_avaliacao, id_midia, midia):
        """Solicita nota, status e comentário e salva a avaliação."""
        print(f"\nAvaliando: {midia.get('titulo')}")

        try:
            nota = float(
                input("Nota (0 a 10): ").strip().replace(",", ".")
            )
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

        avaliacao = Avaliação()

        resultado = avaliacao.Registrar_nota(nota)
        if resultado is not True:
            print(resultado)
            return

        resultado = avaliacao.Registrar_comentario(comentario)
        if resultado is not True:
            print(resultado)
            return

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
        """Exibe o menu de relatórios."""
        relatorio = Relatório()

        while True:
            print("\n===== RELATÓRIOS =====")
            print("1 - Relatório geral")
            print("2 - Média geral do catálogo")
            print("3 - Média por gênero")
            print("4 - Tempo total por tipo")
            print("5 - Top 10")
            print("6 - Série com mais episódios assistidos")
            print("7 - Voltar")

            opcao = input("Opção: ").strip()

            if opcao == "1":
                relatorio.Gerar_relatorio()
            elif opcao == "2":
                media = relatorio.Gerar_media_geral_catalogo()
                print(f"Média geral: {media:.2f}")
            elif opcao == "3":
                relatorio.Media_genero()
            elif opcao == "4":
                relatorio.Tempo_total_tipo()
            elif opcao == "5":
                relatorio.Top_10()
            elif opcao == "6":
                relatorio.Serie_maior_numero_ep_assistidos()
            elif opcao == "7":
                break
            else:
                print("Opção inválida.")

    def Mostrar_config(self):
        """Mostra as configurações."""
        print("Configurações do sistema.")
