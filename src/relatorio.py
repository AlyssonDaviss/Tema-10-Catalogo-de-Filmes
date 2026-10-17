
from repositories.cadastrar_midia import CadastrarMidia
from repositories.cadastrar_avaliacao import CadastrarAvaliacao


class Relatório:
    """Gera relatórios e estatísticas sobre o catálogo de mídias."""

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
        """Converte durações numéricas ou textos para minutos."""
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
        """Retorna os episódios de todas as temporadas."""
        episodios = []

        temporadas = midia.get("temporadas", {})

        for temporada in temporadas.values():
            episodios_temporada = temporada.get("episodios", {})

            if isinstance(episodios_temporada, dict):
                episodios.extend(
                    (id_episodio, episodio)
                    for id_episodio, episodio
                    in episodios_temporada.items()
                )
            elif isinstance(episodios_temporada, list):
                episodios.extend(
                    (str(indice), episodio)
                    for indice, episodio
                    in enumerate(episodios_temporada, start=1)
                )

        return episodios

    def Gerar_media_geral_catalogo(self):
        """Calcula a média das médias das mídias que possuem notas."""
        midias = self._carregar_midias()
        notas = []

        for id_midia in midias:
            media = self._obter_nota(id_midia)

            # Nota zero é válida; verifica se há notas registradas.
            if self._possui_notas(id_midia):
                notas.append(media)

        if not notas:
            return 0

        return sum(notas) / len(notas)

    def _possui_notas(self, id_midia):
        """Verifica se existe ao menos uma nota para a mídia."""
        avaliacoes = self._carregar_avaliacoes()

        for avaliacoes_usuario in avaliacoes.values():
            if not isinstance(avaliacoes_usuario, dict):
                continue

            avaliacao = avaliacoes_usuario.get(str(id_midia))

            if (
                isinstance(avaliacao, dict)
                and avaliacao.get("nota") is not None
            ):
                return True

        return False

    def Gerar_relatorio(self):
        """Exibe um resumo geral do catálogo."""
        midias = self._carregar_midias()
        avaliacoes = self._carregar_avaliacoes()

        if not midias:
            print("Nenhuma mídia cadastrada.")
            return

        filmes = sum(
            1 for midia in midias.values()
            if midia.get("tipo", "").lower() == "filme"
        )

        series = sum(
            1 for midia in midias.values()
            if midia.get("tipo", "").lower() in ("serie", "série")
        )

        total_avaliacoes = sum(
            len(usuario_avaliacoes)
            for usuario_avaliacoes in avaliacoes.values()
            if isinstance(usuario_avaliacoes, dict)
        )

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

            if not self._possui_notas(id_midia):
                print(
                    f"ID: {id_midia} | "
                    f"Título: {midia.get('titulo', 'Sem título')} | "
                    "Sem avaliações com nota"
                )
                continue

            print(
                f"ID: {id_midia} | "
                f"Título: {midia.get('titulo', 'Sem título')} | "
                f"Média: {media:.2f}"
            )

    def Media_genero(self):
        """Calcula a média das mídias avaliadas por gênero."""
        midias = self._carregar_midias()
        generos = {}

        for id_midia, midia in midias.items():
            if not self._possui_notas(id_midia):
                continue

            genero = midia.get("genero", "Sem gênero")
            nota = self._obter_nota(id_midia)

            generos.setdefault(genero, []).append(nota)

        print("\n===== MÉDIA POR GÊNERO =====")

        if not generos:
            print("Nenhuma mídia avaliada com nota.")
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

                for _, episodio in episodios:
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
            if not self._possui_notas(id_midia):
                continue

            media = self._obter_nota(id_midia)

            ranking.append(
                (
                    media,
                    id_midia,
                    midia.get("titulo", "Sem título")
                )
            )

        ranking.sort(key=lambda item: (-item[0], item[2].casefold()))

        print("\n===== TOP 10 MÍDIAS =====")

        if not ranking:
            print("Nenhuma mídia avaliada com nota.")
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
        Conta episódios marcados como ASSISTIDO nas avaliações.

        As avaliações de episódios usam a chave composta:
        série:temporada:episódio.
        """
        midias = self._carregar_midias()
        avaliacoes = self._carregar_avaliacoes()

        ranking_series = []

        for id_serie, midia in midias.items():
            if midia.get("tipo", "").lower() not in ("serie", "série"):
                continue

            episodios = self._obter_episodios(midia)
            total_assistidos = 0

            for id_temporada, temporada in midia.get(
                "temporadas", {}
            ).items():
                episodios_temporada = temporada.get("episodios", {})

                if not isinstance(episodios_temporada, dict):
                    continue

                for id_episodio in episodios_temporada:
                    chave = (
                        f"{id_serie}:temporada:{id_temporada}:"
                        f"episodio:{id_episodio}"
                    )

                    for avaliacoes_usuario in avaliacoes.values():
                        if not isinstance(avaliacoes_usuario, dict):
                            continue

                        avaliacao = avaliacoes_usuario.get(chave, {})

                        if (
                            isinstance(avaliacao, dict)
                            and avaliacao.get("status") == "ASSISTIDO"
                        ):
                            total_assistidos += 1

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

        ranking_series.sort(
            key=lambda item: (-item[0], item[1].casefold())
        )

        quantidade, titulo = ranking_series[0]

        print(f"Série: {titulo}")
        print(f"Episódios assistidos: {quantidade}")
