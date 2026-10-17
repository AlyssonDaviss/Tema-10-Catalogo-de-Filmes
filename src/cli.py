import random

from repositories.cadastrar_midia import CadastrarMidia
from repositories.cadastrar_avaliacao import CadastrarAvaliacao
from repositories.cadastrar_config import CadastrarConfiguracoes
from src.midia import Filme, Serie
from src.avaliacao import Avaliação
from src.relatorio import Relatório
from src.config import Configuracoes


class CLI:
    """Interface de linha de comando do sistema."""

    def __init__(self, comando=None, argumentos=None, id_usuario=None):
        self.comando = comando
        self.argumentos = argumentos or []
        self.id_usuario = id_usuario

    def Executar(self):
        comandos = Comandos(self.id_usuario)

        while True:
            print("\n===== MENU PRINCIPAL =====")
            print("1 - Cadastrar mídia")
            print("2 - Listar mídias")
            print("3 - Buscar mídia")
            print("4 - Avaliar mídia")
            print("5 - Atualizar status")
            print("6 - Relatórios")
            print("7 - Recomendações")
            print("8 - Configurações")
            print("0 - Sair")

            opcao = input("Opção: ").strip()

            opcoes = {
                "1": comandos.Cadastrar,
                "2": comandos.Listar,
                "3": comandos.Buscar,
                "4": comandos.Avaliar,
                "5": comandos.Atualizar_status,
                "6": comandos.Gerar_relatorio,
                "7": comandos.Recomendar,
                "8": comandos.Mostrar_config
            }

            if opcao == "0":
                print("Saindo...")
                break

            funcao = opcoes.get(opcao)

            if funcao:
                funcao()
            else:
                print("Opção inválida.")

    def Processar_comando(self):
        comandos = Comandos(self.id_usuario)

        opcoes = {
            "listar": comandos.Listar,
            "cadastrar": comandos.Cadastrar,
            "buscar": comandos.Buscar,
            "avaliar": comandos.Avaliar,
            "atualizar-status": comandos.Atualizar_status,
            "relatorios": comandos.Gerar_relatorio,
            "recomendar": comandos.Recomendar,
            "configuracoes": comandos.Mostrar_config
        }

        funcao = opcoes.get(self.comando)

        if funcao:
            return funcao()

        self.Mostrar_ajuda()

    def Mostrar_ajuda(self):
        print("Comandos disponíveis:")
        print("cadastrar - Cadastrar mídia")
        print("listar - Listar mídias")
        print("buscar - Buscar mídia")
        print("avaliar - Avaliar mídia ou episódio")
        print("atualizar-status - Atualizar status")
        print("relatorios - Exibir relatórios")
        print("recomendar - Receber recomendações")
        print("configuracoes - Gerenciar configurações")


class Comandos:
    """Executa as operações do sistema."""

    STATUS = {
        "1": "NÃO ASSISTIDO",
        "2": "ASSISTINDO",
        "3": "ASSISTIDO"
    }

    def __init__(self, id_usuario=None):
        self.id_usuario = id_usuario
        self.repositorio_configuracoes = CadastrarConfiguracoes()

        if self.id_usuario is not None:
            dados = self.repositorio_configuracoes.obter_ou_criar(
                self.id_usuario
            )

            self.configuracoes = Configuracoes(
                nota_min_recomendacao=dados.get(
                    "nota_min_recomendacao", 7.0
                ),
                limite_listas_personalizadas=dados.get(
                    "limite_listas_personalizadas", 10
                )
            )
        else:
            self.configuracoes = Configuracoes()

    @staticmethod
    def _ler_inteiro(mensagem, minimo=1):
        while True:
            try:
                valor = int(input(mensagem).strip())

                if valor < minimo:
                    print(f"Digite um inteiro maior ou igual a {minimo}.")
                    continue

                return valor
            except ValueError:
                print("Digite um número inteiro válido.")

    @staticmethod
    def _ler_numero(mensagem, minimo=0, maximo=None):
        while True:
            try:
                valor = float(
                    input(mensagem).strip().replace(",", ".")
                )

                if valor < minimo:
                    print(f"O valor deve ser maior ou igual a {minimo}.")
                    continue

                if maximo is not None and valor > maximo:
                    print(f"O valor máximo permitido é {maximo}.")
                    continue

                return valor
            except ValueError:
                print("Digite um número válido.")

    @staticmethod
    def _ler_status():
        print("\nStatus:")
        print("1 - NÃO ASSISTIDO")
        print("2 - ASSISTINDO")
        print("3 - ASSISTIDO")

        while True:
            opcao = input("Escolha: ").strip()

            if opcao in Comandos.STATUS:
                return Comandos.STATUS[opcao]

            print("Opção inválida.")

    def Cadastrar(self):
        """Cadastra um filme ou uma série sem status inicial."""
        titulo = input("Título da mídia: ").strip()
        tipo = input("Tipo (filme/série): ").strip().casefold()
        genero = input("Gênero: ").strip()
        ano = self._ler_inteiro("Ano de lançamento: ")
        classificacao = input(
            "Classificação indicativa: "
        ).strip()
        elenco = input(
            "Elenco separado por vírgulas (opcional): "
        ).strip()

        if tipo not in ("filme", "serie", "série"):
            print("Tipo inválido. Escolha filme ou série.")
            return

        tipo = "serie" if tipo == "série" else tipo

        try:
            if tipo == "filme":
                duracao = self._ler_numero(
                    "Duração do filme em minutos: ",
                    minimo=0.01
                )

                midia = Filme(
                    titulo=titulo,
                    genero=genero,
                    ano=ano,
                    classificacao_indicativa=classificacao,
                    elenco=elenco,
                    duracao=duracao
                )
            else:
                midia = Serie(
                    titulo=titulo,
                    tipo="SERIE",
                    genero=genero,
                    ano=ano,
                    classificacao_indicativa=classificacao,
                    elenco=elenco
                )

        except (ValueError, TypeError) as erro:
            print(f"Dados inválidos: {erro}")
            return

        cadastro = CadastrarMidia()
        id_midia = cadastro.cadastrar_midia(midia)

        if not id_midia:
            print(
                "Cadastro não realizado. Já existe uma mídia com "
                "o mesmo título, tipo e ano, ou os dados são inválidos."
            )
            return

        if tipo == "filme":
            print(f"Filme cadastrado! ID: {id_midia}")
            return

        numero_temporada = 1

        while True:
            print(f"\n===== TEMPORADA {numero_temporada} =====")

            nome = input(
                "Nome da temporada (Enter para automático): "
            ).strip()

            if not nome:
                nome = f"Temporada {numero_temporada}"

            quantidade = self._ler_inteiro(
                "Quantidade de episódios: "
            )

            duracao_media = self._ler_numero(
                "Duração média dos episódios (minutos): ",
                minimo=0.01
            )

            data = input(
                "Data de lançamento da temporada (AAAA-MM-DD): "
            ).strip()

            try:
                temporada = midia.registrar_temporadas(
                    numero_temporada,
                    quantidade,
                    duracao_media,
                    data,
                    nome
                )
            except (ValueError, TypeError) as erro:
                print(f"Não foi possível criar a temporada: {erro}")
                return

            id_temporada = cadastro.cadastrar_temporada(
                id_midia,
                temporada
            )

            if (
                not isinstance(id_temporada, str)
                or not id_temporada.isdigit()
            ):
                print(f"Erro ao cadastrar temporada: {id_temporada}")
                return

            print(
                f"Temporada cadastrada! ID: {id_temporada}. "
                f"Episódios criados: {quantidade}."
            )

            numero_temporada += 1

            continuar = input(
                "Deseja cadastrar outra temporada? (s/n): "
            ).strip().casefold()

            if continuar != "s":
                break

        print(f"Série cadastrada! ID: {id_midia}")

    def Listar(self):
        """Lista mídias e seus status para o usuário atual."""
        dados = CadastrarMidia().carregar_dados()
        avaliacoes = CadastrarAvaliacao().carregar_dados()
        minhas_avaliacoes = avaliacoes.get(
            str(self.id_usuario), {}
        )

        if not dados:
            print("Nenhuma mídia cadastrada.")
            return

        print(
            f"\n{'ID':<8} {'Título':<30} "
            f"{'Tipo':<10} {'Ano':<6} {'Status'}"
        )
        print("-" * 90)

        for id_midia, midia in dados.items():
            avaliacao = minhas_avaliacoes.get(id_midia, {})
            status = avaliacao.get("status", "NÃO AVALIADO")

            print(
                f"{id_midia:<8} "
                f"{midia.get('titulo', 'Sem título'):<30} "
                f"{midia.get('tipo', '?'):<10} "
                f"{str(midia.get('ano', '?')):<6} "
                f"{status}"
            )

    def Buscar(self):
        """Busca mídias pelo título ou identificador."""
        dados = CadastrarMidia().carregar_dados()
        termo = input("Digite o título ou ID: ").strip().casefold()

        encontrados = [
            (id_midia, midia)
            for id_midia, midia in dados.items()
            if termo == str(id_midia).casefold()
            or termo in midia.get("titulo", "").casefold()
        ]

        if not encontrados:
            print("Nenhuma mídia encontrada.")
            return

        avaliacoes = CadastrarAvaliacao().carregar_dados()
        minhas_avaliacoes = avaliacoes.get(
            str(self.id_usuario), {}
        )

        for id_midia, midia in encontrados:
            avaliacao = minhas_avaliacoes.get(id_midia, {})

            print(
                f"ID: {id_midia} | "
                f"Título: {midia.get('titulo')} | "
                f"Tipo: {midia.get('tipo')} | "
                f"Ano: {midia.get('ano')} | "
                f"Status: {avaliacao.get('status', 'NÃO AVALIADO')}"
            )

    def Atualizar_status(self):
        """Atualiza o status geral de uma mídia ou de um episódio."""
        if self.id_usuario is None:
            print("É necessário identificar o usuário para atualizar o status.")
            return

        dados = CadastrarMidia().carregar_dados()

        if not dados:
            print("Nenhuma mídia cadastrada.")
            return

        print("\n1 - Atualizar status de filme ou série")
        print("2 - Atualizar status de episódio")
        print("0 - Voltar")

        opcao = input("Opção: ").strip()

        if opcao == "0":
            return

        if opcao == "1":
            id_midia = input("ID da mídia: ").strip().zfill(4)

            if id_midia not in dados:
                print("Mídia não encontrada.")
                return

            status = self._ler_status()
            resultado = self._registrar_avaliacao(
                id_midia=id_midia,
                status=status
            )

        elif opcao == "2":
            resultado = self._atualizar_status_episodio(dados)

        else:
            print("Opção inválida.")
            return

        if resultado is True:
            print("Status atualizado com sucesso.")
        else:
            print(resultado)

    def _atualizar_status_episodio(self, dados):
        """Registra o status de um episódio na avaliação do usuário."""
        id_serie = input("ID da série: ").strip().zfill(4)

        if id_serie not in dados:
            return "Série não encontrada."

        serie = dados[id_serie]

        if serie.get("tipo", "").lower() != "serie":
            return "O ID informado não corresponde a uma série."

        temporadas = serie.get("temporadas", {})

        if not temporadas:
            return "A série não possui temporadas cadastradas."

        for id_temp, temporada in temporadas.items():
            print(f"{id_temp} - {temporada.get('titulo')}")

        id_temporada = input("ID da temporada: ").strip().zfill(4)

        if id_temporada not in temporadas:
            return "Temporada não encontrada."

        episodios = temporadas[id_temporada].get("episodios", {})

        if not episodios:
            return "Essa temporada não possui episódios."

        for id_ep, episodio in episodios.items():
            print(f"{id_ep} - {episodio.get('titulo')}")

        id_episodio = input("ID do episódio: ").strip().zfill(4)

        if id_episodio not in episodios:
            return "Episódio não encontrado."

        status = self._ler_status()

        # A chave composta identifica o episódio sem confundi-lo
        # com a avaliação geral da série.
        chave_avaliacao = (
            f"{id_serie}:temporada:{id_temporada}:episodio:{id_episodio}"
        )

        return self._registrar_avaliacao(
            id_midia=chave_avaliacao,
            status=status
        )

    def _selecionar_item(self, itens, mensagem, descricao):
        """Mostra itens identificados por ID e permite voltar."""
        if not itens:
            print("Não há opções disponíveis.")
            return None

        print(f"\n===== {mensagem} =====")

        for identificador, item in itens:
            print(f"{identificador} - {descricao(item)}")

        print("0 - Voltar")

        ids = {
            str(identificador).zfill(4): item
            for identificador, item in itens
        }

        while True:
            escolha = input("Digite o ID: ").strip()

            if escolha == "0":
                return None

            escolha = escolha.zfill(4)

            if escolha in ids:
                return escolha, ids[escolha]

            print("ID inválido. Escolha uma opção listada ou digite 0.")

    def _mostrar_avaliacao_atual(self, chave):
        """Exibe a avaliação atual do usuário para o item selecionado."""
        if self.id_usuario is None:
            return

        dados = CadastrarAvaliacao().carregar_dados()
        usuario = dados.get(str(self.id_usuario), {})
        avaliacao = usuario.get(str(chave))

        print("\n===== AVALIAÇÃO ATUAL =====")

        if not avaliacao:
            print("Ainda não existe uma avaliação sua para este item.")
            return

        nota = avaliacao.get("nota")
        status = avaliacao.get("status", "NÃO ASSISTIDO")
        comentario = avaliacao.get("comentario", "")

        print(f"Nota: {nota if nota is not None else 'Não informada'}")
        print(f"Status: {status}")
        print(f"Comentário: {comentario or 'Sem comentário'}")

    def Avaliar(self):
        """Menu principal de avaliações."""
        if self.id_usuario is None:
            print("É necessário identificar o usuário para avaliar.")
            return

        while True:
            print("\n===== AVALIAR MÍDIA OU EPISÓDIO =====")
            print("1 - Avaliar filme")
            print("2 - Avaliar série")
            print("0 - Voltar")

            opcao = input("Opção: ").strip()

            if opcao == "0":
                break

            if opcao not in ("1", "2"):
                print("Opção inválida.")
                continue

            dados = CadastrarMidia().carregar_dados()

            if not dados:
                print("Nenhuma mídia cadastrada.")
                continue

            if opcao == "1":
                self._avaliar_filme(dados)
            else:
                self._avaliar_serie(dados)

    def _confirmar_e_salvar_avaliacao(self, chave, titulo_completo):
        """Coleta, confirma e salva uma avaliação."""
        self._mostrar_avaliacao_atual(chave)

        print(f"\n===== AVALIAR: {titulo_completo} =====")
        entrada_nota = input(
            "Nota de 0 a 10 (Enter para não informar, C para cancelar): "
        ).strip()

        if entrada_nota.upper() == "C":
            print("Avaliação cancelada.")
            return

        if entrada_nota == "":
            nota = None
        else:
            try:
                nota = float(entrada_nota.replace(",", "."))
                if not 0 <= nota <= 10:
                    print("A nota deve estar entre 0 e 10.")
                    return
            except ValueError:
                print("Digite uma nota válida.")
                return

        status = self._ler_status()
        comentario = input("Comentário (opcional): ").strip()

        print("\n===== CONFIRMAR AVALIAÇÃO =====")
        print(f"Item: {titulo_completo}")
        print(f"Nota: {nota if nota is not None else 'Não informada'}")
        print(f"Status: {status}")
        print(f"Comentário: {comentario or 'Sem comentário'}")
        print("1 - Salvar avaliação")
        print("0 - Cancelar")

        if input("Opção: ").strip() != "1":
            print("Avaliação cancelada.")
            return

        resultado = self._registrar_avaliacao(
            id_midia=chave,
            nota=nota,
            status=status,
            comentario=comentario
        )

        if resultado is True:
            print("\nAvaliação registrada com sucesso!")
        else:
            print(f"Não foi possível registrar a avaliação: {resultado}")

    def _avaliar_filme(self, dados):
        """Seleciona um filme e registra sua avaliação."""
        filmes = [
            (id_midia, midia)
            for id_midia, midia in dados.items()
            if midia.get("tipo", "").lower() == "filme"
        ]

        selecao = self._selecionar_item(
            filmes,
            "SELECIONAR FILME",
            lambda filme: (
                f"{filme.get('titulo', 'Sem título')} "
                f"({filme.get('ano', '?')})"
            )
        )

        if selecao is None:
            return

        id_midia, filme = selecao
        titulo = (
            f"{filme.get('titulo', 'Sem título')} "
            f"({filme.get('ano', '?')})"
        )

        self._confirmar_e_salvar_avaliacao(id_midia, titulo)

    def _avaliar_serie(self, dados):
        """Exibe as modalidades de avaliação de uma série."""
        while True:
            print("\n===== AVALIAR SÉRIE =====")
            print("1 - Nota geral da série")
            print("2 - Nota por temporada")
            print("3 - Nota por episódio")
            print("0 - Voltar")

            opcao = input("Opção: ").strip()

            if opcao == "0":
                return
            elif opcao == "1":
                self._avaliar_serie_geral(dados)
            elif opcao == "2":
                self._avaliar_temporada(dados)
            elif opcao == "3":
                self._avaliar_episodio(dados)
            else:
                print("Opção inválida.")

    def _selecionar_serie(self, dados):
        """Auxiliar para selecionar uma série cadastrada."""
        series = [
            (id_midia, midia)
            for id_midia, midia in dados.items()
            if midia.get("tipo", "").lower() in ("serie", "série")
        ]

        return self._selecionar_item(
            series,
            "SELECIONAR SÉRIE",
            lambda serie: (
                f"{serie.get('titulo', 'Sem título')} "
                f"({serie.get('ano', '?')})"
            )
        )

    def _avaliar_serie_geral(self, dados):
        """Registra uma avaliação geral da série."""
        selecao = self._selecionar_serie(dados)

        if selecao is None:
            return

        id_serie, serie = selecao
        titulo = serie.get("titulo", "Série sem título")

        self._confirmar_e_salvar_avaliacao(
            id_serie,
            f"{titulo} — Avaliação geral"
        )

    def _avaliar_temporada(self, dados):
        """Seleciona uma temporada e registra sua avaliação."""
        selecao_serie = self._selecionar_serie(dados)

        if selecao_serie is None:
            return

        id_serie, serie = selecao_serie
        temporadas = serie.get("temporadas", {})

        if not temporadas:
            print("Essa série não possui temporadas cadastradas.")
            return

        selecao_temporada = self._selecionar_item(
            list(temporadas.items()),
            f"TEMPORADAS DE {serie.get('titulo', 'Série')}",
            lambda temporada: (
                f"{temporada.get('titulo', 'Temporada')} — "
                f"{len(temporada.get('episodios', {}))} episódios"
            )
        )

        if selecao_temporada is None:
            return

        id_temporada, temporada = selecao_temporada
        chave = f"{id_serie}:temporada:{id_temporada}"

        titulo_serie = serie.get("titulo", "Série sem título")
        titulo_temporada = temporada.get("titulo", "Temporada")

        self._confirmar_e_salvar_avaliacao(
            chave,
            f"{titulo_serie} — {titulo_temporada}"
        )

    def _avaliar_episodio(self, dados):
        """Seleciona série, temporada e episódio para avaliar."""
        selecao_serie = self._selecionar_serie(dados)

        if selecao_serie is None:
            return

        id_serie, serie = selecao_serie
        temporadas = serie.get("temporadas", {})

        if not temporadas:
            print("Essa série não possui temporadas cadastradas.")
            return

        selecao_temporada = self._selecionar_item(
            list(temporadas.items()),
            f"TEMPORADAS DE {serie.get('titulo', 'Série')}",
            lambda temporada: (
                f"{temporada.get('titulo', 'Temporada')} — "
                f"{len(temporada.get('episodios', {}))} episódios"
            )
        )

        if selecao_temporada is None:
            return

        id_temporada, temporada = selecao_temporada
        episodios = temporada.get("episodios", {})

        if not episodios:
            print("Essa temporada não possui episódios cadastrados.")
            return

        selecao_episodio = self._selecionar_item(
            list(episodios.items()),
            f"EPISÓDIOS DE {temporada.get('titulo', 'Temporada')}",
            lambda episodio: episodio.get(
                "titulo", "Episódio sem título"
            )
        )

        if selecao_episodio is None:
            return

        id_episodio, episodio = selecao_episodio

        chave = (
            f"{id_serie}:temporada:{id_temporada}:episodio:{id_episodio}"
        )

        titulo_completo = (
            f"{serie.get('titulo', 'Série')} — "
            f"{temporada.get('titulo', 'Temporada')} — "
            f"{episodio.get('titulo', 'Episódio')}"
        )

        self._confirmar_e_salvar_avaliacao(chave, titulo_completo)

    def _registrar_avaliacao(
        self,
        id_midia,
        nota=None,
        status="NÃO ASSISTIDO",
        comentario=""
    ):
        """Valida e persiste uma avaliação."""
        try:
            avaliacao = Avaliação(
                nota=nota,
                comentario=comentario,
                status=status
            )
        except (ValueError, TypeError) as erro:
            return str(erro)

        cadastro = CadastrarAvaliacao()

        return cadastro.registrar_avaliacao(
            self.id_usuario,
            id_midia,
            avaliacao.obter_nota(),
            avaliacao.obter_status(),
            avaliacao.obter_comentario()
        )

    def _notas_por_midia(self):
        """Agrupa notas por identificador de mídia."""
        dados = CadastrarAvaliacao().carregar_dados()
        notas = {}

        if not isinstance(dados, dict):
            return notas

        for avaliacoes_usuario in dados.values():
            if not isinstance(avaliacoes_usuario, dict):
                continue

            for id_midia, avaliacao in avaliacoes_usuario.items():
                if not isinstance(avaliacao, dict):
                    continue

                nota = avaliacao.get("nota")

                if nota is None:
                    continue

                try:
                    nota = float(nota)
                except (TypeError, ValueError):
                    continue

                if 0 <= nota <= 10:
                    # Notas de temporada e episódio usam chaves como
                    # "0001:temporada:..."; contam para a série.
                    id_base = str(id_midia).split(":")[0]
                    notas.setdefault(id_base, []).append(nota)

        return notas

    def Recomendar(self):
        """Recomenda até três mídias que atendem à nota mínima."""
        nota_corte = self.configuracoes.nota_min_recomendacao
        dados = CadastrarMidia().carregar_dados()
        notas = self._notas_por_midia()

        candidatas = []

        for id_midia, midia in dados.items():
            lista_notas = notas.get(str(id_midia), [])

            if not lista_notas:
                continue

            media = sum(lista_notas) / len(lista_notas)

            if media >= nota_corte:
                candidatas.append((id_midia, midia, media))

        if not candidatas:
            print("Não há mídias que atendam à nota mínima.")
            return

        for id_midia, midia, media in random.sample(
            candidatas, min(3, len(candidatas))
        ):
            print(
                f"ID: {id_midia} | {midia.get('titulo')} | "
                f"{midia.get('tipo')} | Média: {media:.1f}"
            )

    def Remover(self):
        """Remove uma mídia do catálogo."""
        cadastro = CadastrarMidia()
        dados = cadastro.carregar_dados()

        id_midia = input("ID da mídia a remover: ").strip().zfill(4)

        if id_midia not in dados:
            print("Mídia não encontrada.")
            return

        confirmacao = input(
            f"Remover '{dados[id_midia].get('titulo')}'? (s/n): "
        ).strip().lower()

        if confirmacao != "s":
            print("Operação cancelada.")
            return

        del dados[id_midia]
        cadastro.salvar_dados(dados)
        print("Mídia removida.")

    def Criar_lista(self):
        print(
            "O gerenciamento de listas personalizadas será integrado "
            "ao módulo de usuários."
        )

    def Gerar_relatorio(self):
        relatorio = Relatório()

        while True:
            print("\n===== RELATÓRIOS =====")
            print("1 - Relatório geral")
            print("2 - Média geral do catálogo")
            print("3 - Média por gênero")
            print("4 - Tempo total por tipo")
            print("5 - Top 10")
            print("6 - Série com mais episódios assistidos")
            print("0 - Voltar")

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
            elif opcao == "0":
                break
            else:
                print("Opção inválida.")

    def Mostrar_config(self):
        """Consulta e altera as configurações do usuário."""
        if self.id_usuario is None:
            print("Não foi possível identificar o usuário logado.")
            return

        while True:
            print("\n===== CONFIGURAÇÕES =====")
            print(
                f"1 - Nota mínima para recomendação: "
                f"{self.configuracoes.nota_min_recomendacao:g}"
            )
            print(
                f"2 - Limite de listas personalizadas: "
                f"{self.configuracoes.limite_listas_personalizadas}"
            )
            print("0 - Voltar")

            opcao = input("Opção: ").strip()

            if opcao == "1":
                resultado = self.configuracoes.Nota_min_recomendado()
            elif opcao == "2":
                resultado = self.configuracoes.Limite_lista()
            elif opcao == "0":
                break
            else:
                print("Opção inválida.")
                continue

            if resultado is not True:
                if resultado is not None:
                    print(resultado)
                continue

            dados_configuracoes = {
                "nota_min_recomendacao":
                    self.configuracoes.nota_min_recomendacao,
                "limite_listas_personalizadas":
                    self.configuracoes.limite_listas_personalizadas
            }

            resultado = (
                self.repositorio_configuracoes.salvar_configuracoes(
                    self.id_usuario,
                    dados_configuracoes
                )
            )

            if resultado is True:
                print("Configurações salvas.")
            else:
                print(resultado)