
from repositories.cadastrar_midia import CadastrarMidia
from repositories.cadastrar_avaliacao import CadastrarAvaliacao


class Relatório:
    """
    Gera relatórios e estatísticas sobre o catálogo de mídias.

    Métodos:
    - Gerar média geral do catálogo
    - Gerar relatório
    - Média por gênero
    - Tempo total por tipo
    - Top 10
    - Série com maior número de episódios assistidos
    """

    def __init__(self):
        self.cadastro_midia = CadastrarMidia()
        self.cadastro_avaliacao = CadastrarAvaliacao()

    def _carregar_midias(self):
        return self.cadastro_midia.carregar_dados()

    def _carregar_avaliacoes(self):
        return self.cadastro_avaliacao.carregar_dados()

    def _obter_nota(self, id_midia):
        return self.cadastro_avaliacao.gerar_media(id_midia)

    def _converter_duracao(self, duracao):
        """Converte durações como '120m' ou '45 minutos' em minutos."""
        if isinstance(duracao, (int, float)):
            return float(duracao)

        if not isinstance(duracao, str):
            return 0

        numero = ""

        for caractere in duracao:
            if caractere.isdigit() or caractere == ".":
                numero += caractere
            elif numero:
                break

        try:
            return float(numero) if numero else 0
        except ValueError:
            return 0

    def _obter_episodios(self, midia):
        """Retorna os episódios registrados em todas as temporadas."""
        episodios = []

        temporadas = midia.get("temporadas", {})

        for temporada in temporadas.values():
            episodios_temporada = temporada.get("episodios", {})

            if isinstance(episodios_temporada, dict):
                episodios.extend(episodios_temporada.values())
            elif isinstance(episodios_temporada, list):
                episodios.extend(episodios_temporada)

        return episodios

    def Gerar_media_geral_catalogo(self):
        """Calcula a média das notas médias das mídias avaliadas."""
        midias = self._carregar_midias()

        if not midias:
            return 0

        notas = [
            self._obter_nota(id_midia)
            for id_midia in midias
            if self._obter_nota(id_midia) > 0
        ]

        if not notas:
            return 0

        return sum(notas) / len(notas)

    def Gerar_relatorio(self):
        """Exibe um resumo geral do catálogo."""
        midias = self._carregar_midias()
        avaliacoes = self._carregar_avaliacoes()

        if not midias:
            print("Nenhuma mídia cadastrada.")
            return

        filmes = 0
        series = 0
        total_avaliacoes = 0

        for midia in midias.values():
            tipo = midia.get("tipo", "").lower()

            if tipo == "filme":
                filmes += 1
            elif tipo in ("serie", "série"):
                series += 1

        for avaliacoes_usuario in avaliacoes.values():
            total_avaliacoes += len(avaliacoes_usuario)

        print("\n===== RELATÓRIO DO CATÁLOGO =====")
        print(f"Total de mídias: {len(midias)}")
        print(f"Filmes cadastrados: {filmes}")
        print(f"Séries cadastradas: {series}")
        print(f"Total de avaliações: {total_avaliacoes}")
        print(
            "Média geral do catálogo: "
            f"{self.Gerar_media_geral_catalogo():.2f}"
        )

        print("\n===== MÉDIA POR MÍDIA =====")

        for id_midia, midia in midias.items():
            media = self._obter_nota(id_midia)

            print(
                f"ID: {id_midia} | "
                f"Título: {midia.get('titulo', 'Sem título')} | "
                f"Média: {media:.2f}"
            )

    def Media_genero(self):
        """Calcula a média das avaliações agrupadas por gênero."""
        midias = self._carregar_midias()
        generos = {}

        for id_midia, midia in midias.items():
            genero = midia.get("genero", "Sem gênero")
            nota = self._obter_nota(id_midia)

            if nota <= 0:
                continue

            if genero not in generos:
                generos[genero] = []

            generos[genero].append(nota)

        print("\n===== MÉDIA POR GÊNERO =====")

        if not generos:
            print("Nenhuma mídia avaliada.")
            return

        for genero, notas in sorted(generos.items()):
            media = sum(notas) / len(notas)
            print(f"{genero}: {media:.2f}")

    def Tempo_total_tipo(self):
        """Calcula o tempo total de filmes e episódios cadastrados."""
        midias = self._carregar_midias()

        minutos_filmes = 0
        minutos_series = 0

        for midia in midias.values():
            tipo = midia.get("tipo", "").lower()

            if tipo == "filme":
                minutos_filmes += self._converter_duracao(
                    midia.get("duracao", 0)
                )

            elif tipo in ("serie", "série"):
                episodios = self._obter_episodios(midia)

                for episodio in episodios:
                    minutos_series += self._converter_duracao(
                        episodio.get("duracao", 0)
                    )

        print("\n===== TEMPO TOTAL DO CATÁLOGO =====")
        print(f"Filmes: {minutos_filmes:g} minutos")
        print(f"Séries: {minutos_series:g} minutos")
        print(
            f"Total: {minutos_filmes + minutos_series:g} minutos"
        )

    def Top_10(self):
        """Exibe as dez mídias com maiores médias de avaliação."""
        midias = self._carregar_midias()
        ranking = []

        for id_midia, midia in midias.items():
            media = self._obter_nota(id_midia)

            if media > 0:
                ranking.append(
                    (media, id_midia, midia.get("titulo", "Sem título"))
                )

        ranking.sort(reverse=True)

        print("\n===== TOP 10 MÍDIAS =====")

        if not ranking:
            print("Nenhuma mídia avaliada.")
            return

        for posicao, (media, id_midia, titulo) in enumerate(
            ranking[:10], start=1
        ):
            print(
                f"{posicao}º - {titulo} | "
                f"ID: {id_midia} | Média: {media:.2f}"
            )

    def Serie_maior_numero_ep_assistidos(self):
        """
        Estima os episódios assistidos a partir do status da série.

        Status 'completo' ou 'assistido': considera todos os episódios
        cadastrados como assistidos.
        """
        midias = self._carregar_midias()
        avaliacoes = self._carregar_avaliacoes()

        ranking_series = []

        for id_midia, midia in midias.items():
            if midia.get("tipo", "").lower() not in ("serie", "série"):
                continue

            episodios = self._obter_episodios(midia)
            total_assistidos = 0

            for avaliacoes_usuario in avaliacoes.values():
                avaliacao = avaliacoes_usuario.get(str(id_midia), {})
                status = avaliacao.get("status", "").strip().lower()

                if status in ("completo", "assistido"):
                    total_assistidos += len(episodios)

            ranking_series.append(
                (
                    total_assistidos,
                    midia.get("titulo", "Sem título")
                )
            )

        print("\n===== SÉRIE COM MAIS EPISÓDIOS ASSISTIDOS =====")

        if not ranking_series:
            print("Nenhuma série cadastrada.")
            return

        ranking_series.sort(reverse=True)
        quantidade, titulo = ranking_series[0]

        print(f"Série: {titulo}")
        print(f"Episódios assistidos (estimativa): {quantidade}")
