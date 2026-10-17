
import json
from pathlib import Path


class CadastrarMidia:
    """Gerencia o cadastro e a persistência de mídias em JSON."""

    def __init__(self):
        self.caminho = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "midia_dic.json"
        )

        self.caminho.parent.mkdir(parents=True, exist_ok=True)

        if not self.caminho.exists():
            self.salvar_dados({})

    def carregar_dados(self):
        """Carrega as mídias armazenadas no JSON."""
        with open(self.caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def salvar_dados(self, dados):
        """Salva as mídias no JSON."""
        with open(self.caminho, "w", encoding="utf-8") as arquivo:
            json.dump(
                dados,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

    def gerar_id(self, dados):
        """Gera um identificador numérico sequencial com quatro dígitos."""
        ids = [
            int(chave)
            for chave in dados
            if str(chave).isdigit()
        ]
        return str(max(ids, default=0) + 1).zfill(4)

    def cadastrar_midia(self, midia):
        """Cadastra filme ou série sem armazenar status ou nota."""
        dados = self.carregar_dados()

        tipo = midia.tipo.lower()
        titulo = midia.titulo
        ano = midia.obter_ano()

        for item in dados.values():
            if (
                item.get("titulo", "").casefold() == titulo.casefold()
                and item.get("tipo", "").lower() == tipo
                and str(item.get("ano", "")) == str(ano)
            ):
                return False

        novo_id = self.gerar_id(dados)

        registro = {
            "tipo": tipo,
            "titulo": titulo,
            "genero": midia.genero,
            "ano": ano,
            "classificacao_indicativa":
                midia.obter_classificacao_indicativa(),
            "elenco": midia.obter_elenco()
        }

        if tipo == "filme":
            registro["duracao"] = midia.obter_duracao()

        elif tipo == "serie":
            registro["temporadas"] = {}

        else:
            return False

        dados[novo_id] = registro
        self.salvar_dados(dados)

        return novo_id

    def atualizar_duracao(self, id_midia, duracao):
        """Atualiza a duração de um filme."""
        dados = self.carregar_dados()
        id_midia = str(id_midia).zfill(4)

        if id_midia not in dados:
            return "ID não cadastrado."

        if dados[id_midia].get("tipo", "").lower() != "filme":
            return "A mídia não é um filme."

        try:
            duracao = float(duracao)
        except (TypeError, ValueError):
            return "A duração deve ser numérica."

        if duracao <= 0:
            return "A duração deve ser maior que zero."

        dados[id_midia]["duracao"] = duracao
        self.salvar_dados(dados)

        return True

    def cadastrar_temporada(self, id_serie, temporada):
        """Cadastra uma temporada e seus episódios sem status ou nota."""
        dados = self.carregar_dados()
        id_serie = str(id_serie).zfill(4)

        if id_serie not in dados:
            return "ID não cadastrado."

        if dados[id_serie].get("tipo", "").lower() != "serie":
            return "A mídia informada não é uma série."

        temporadas = dados[id_serie].setdefault("temporadas", {})
        numero_temporada = temporada.obter_numero()

        for item in temporadas.values():
            if int(item.get("numero", 0)) == numero_temporada:
                return "Essa temporada já está cadastrada."

        novo_id = self.gerar_id(temporadas)
        episodios_json = {}

        for episodio in temporada.episodios:
            id_episodio = self.gerar_id(episodios_json)

            episodios_json[id_episodio] = {
                "numero": episodio.numero,
                "titulo": episodio.obter_titulo(),
                "duracao": episodio.obter_duracao(),
                "data_lancamento": episodio.data_lancamento
            }

        temporadas[novo_id] = {
            "numero": numero_temporada,
            "titulo": temporada.obter_titulo(),
            "numero_episodios": temporada.obter_numero_episodios(),
            "duracao_media": temporada.obter_duracao_media(),
            "data_lancamento": temporada.obter_data_lancamento(),
            "episodios": episodios_json
        }

        self.salvar_dados(dados)
        return novo_id
